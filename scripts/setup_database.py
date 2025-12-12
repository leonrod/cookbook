#!/usr/bin/env python3
"""
Script de setup do banco de dados com melhorias
"""
import sqlite3
import json
import hashlib
import os
import sys
import argparse
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

DB_NAME = 'nurglingdatabase.db'
JSON_FILE = 'food-info2.json'


def gerar_hash(nome, ingredientes):
    """
    Cria uma assinatura única baseada no nome e ingredientes ordenados.
    """
    s = f"{nome}" + "".join([
        f"{i['name']}{i['percentage']}" 
        for i in sorted(ingredientes, key=lambda x: x['name'])
    ])
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def criar_backup(db_path):
    """
    Cria backup do banco de dados existente.
    """
    if os.path.exists(db_path):
        backup_path = f"{db_path}.backup"
        counter = 1
        while os.path.exists(backup_path):
            backup_path = f"{db_path}.backup.{counter}"
            counter += 1
        
        try:
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"✓ Backup criado: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"⚠ Aviso: Não foi possível criar backup: {e}")
            return None
    return None


def criar_banco(force=False, backup=True):
    """
    Cria e popula o banco de dados.
    
    Args:
        force: Se True, remove banco existente sem perguntar
        backup: Se True, cria backup antes de remover
    """
    # Verificar se arquivo JSON existe
    if not os.path.exists(JSON_FILE):
        print(f"❌ ERRO: Arquivo {JSON_FILE} não encontrado.")
        return False
    
    # Lidar com banco existente
    if os.path.exists(DB_NAME):
        if not force:
            resposta = input(f"⚠ Banco {DB_NAME} já existe. Deseja recriá-lo? (s/N): ")
            if resposta.lower() not in ['s', 'sim', 'y', 'yes']:
                print("Operação cancelada.")
                return False
        
        # Criar backup se solicitado
        if backup:
            criar_backup(DB_NAME)
        
        # Remover banco antigo
        try:
            os.remove(DB_NAME)
            print(f"✓ Banco antigo removido")
        except PermissionError:
            print("❌ ERRO: O banco está em uso. Feche todas as conexões e tente novamente.")
            return False
    
    # Criar conexão
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    print("\n📊 Criando tabelas...")
    
    # Criar tabelas
    c.execute('''
        CREATE TABLE recipes (
            recipe_hash TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            resource_name TEXT,
            hunger REAL,
            energy INTEGER,
            total_fep REAL DEFAULT 0
        )
    ''')
    
    c.execute('''
        CREATE TABLE ingredients (
            recipe_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            percentage REAL,
            FOREIGN KEY (recipe_hash) REFERENCES recipes(recipe_hash)
        )
    ''')
    
    c.execute('''
        CREATE TABLE feps (
            recipe_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            value REAL,
            weight REAL,
            FOREIGN KEY (recipe_hash) REFERENCES recipes(recipe_hash)
        )
    ''')
    
    c.execute('''
        CREATE TABLE favorite_recipes (
            recipe_hash TEXT PRIMARY KEY,
            FOREIGN KEY (recipe_hash) REFERENCES recipes(recipe_hash)
        )
    ''')
    
    print("✓ Tabelas criadas")
    
    # Ler JSON
    print(f"\n📖 Lendo {JSON_FILE}...")
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌ ERRO ao ler JSON: {e}")
        conn.close()
        return False
    
    print(f"✓ {len(dados)} receitas encontradas")
    
    # Inserir dados
    print("\n📥 Importando dados...")
    count = 0
    duplicadas = 0
    erros = 0
    
    for idx, item in enumerate(dados, 1):
        try:
            nome = item.get('itemName')
            feps = item.get('feps', [])
            ingredientes = item.get('ingredients', [])
            
            if not nome:
                continue
            
            r_hash = gerar_hash(nome, ingredientes)
            total_fep = sum(f['value'] for f in feps)
            
            # Inserir receita
            c.execute(
                "INSERT INTO recipes VALUES (?, ?, ?, ?, ?, ?)",
                (r_hash, nome, item.get('resourceName'), 
                 item.get('hunger'), item.get('energy'), total_fep)
            )
            
            # Inserir ingredientes
            for ing in ingredientes:
                c.execute(
                    "INSERT INTO ingredients VALUES (?, ?, ?)",
                    (r_hash, ing['name'], ing['percentage'])
                )
            
            # Inserir FEPs
            for fep in feps:
                val = fep['value']
                peso = (val / total_fep) if total_fep > 0 else 0
                c.execute(
                    "INSERT INTO feps VALUES (?, ?, ?, ?)",
                    (r_hash, fep['name'], val, peso)
                )
            
            count += 1
            
            # Progresso
            if count % 1000 == 0:
                print(f"  Processadas: {count}/{len(dados)} ({count/len(dados)*100:.1f}%)")
        
        except sqlite3.IntegrityError:
            duplicadas += 1
        except Exception as e:
            erros += 1
            if erros <= 5:  # Mostrar apenas os primeiros 5 erros
                print(f"  ⚠ Erro na receita {idx}: {e}")
    
    # Commit
    conn.commit()
    
    # Criar índices
    print("\n🔧 Criando índices...")
    indices = [
        ("idx_feps_hash", "feps(recipe_hash)"),
        ("idx_feps_name", "feps(name)"),
        ("idx_ingredients_hash", "ingredients(recipe_hash)"),
        ("idx_ingredients_name", "ingredients(name)"),
        ("idx_recipes_total", "recipes(total_fep)"),
        ("idx_recipes_name", "recipes(item_name)"),
    ]
    
    for idx_name, idx_def in indices:
        c.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")
        print(f"  ✓ {idx_name}")
    
    # Analisar para otimizar query planner
    print("\n📊 Analisando banco de dados...")
    c.execute("ANALYZE")
    
    conn.commit()
    conn.close()
    
    # Resumo
    print("\n" + "="*60)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print(f"📊 Receitas importadas: {count}")
    print(f"⚠️  Duplicatas ignoradas: {duplicadas}")
    if erros > 0:
        print(f"❌ Erros encontrados: {erros}")
    print(f"💾 Banco de dados: {DB_NAME}")
    print(f"📦 Tamanho: {os.path.getsize(DB_NAME) / 1024 / 1024:.2f} MB")
    print("="*60)
    
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup do banco de dados')
    parser.add_argument('--force', action='store_true', 
                       help='Força recriação sem confirmação')
    parser.add_argument('--no-backup', action='store_true',
                       help='Não cria backup do banco existente')
    
    args = parser.parse_args()
    
    sucesso = criar_banco(force=args.force, backup=not args.no_backup)
    sys.exit(0 if sucesso else 1)
