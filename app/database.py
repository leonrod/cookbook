"""
Módulo de gerenciamento de banco de dados
"""
import sqlite3
from contextlib import contextmanager
from flask import current_app, g


@contextmanager
def get_db_connection():
    """
    Context manager para conexão com banco de dados.
    Garante que a conexão seja sempre fechada, mesmo em caso de erro.
    """
    conn = sqlite3.connect(current_app.config['DB_PATH'])
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_db():
    """
    Retorna a conexão de banco de dados para a requisição atual.
    Cria uma nova conexão se necessário e a armazena no contexto da aplicação.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DB_PATH'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    Fecha a conexão de banco de dados no final da requisição.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db_connection(app):
    """
    Inicializa o gerenciamento de conexão de banco de dados com a aplicação.
    """
    app.teardown_appcontext(close_db)


def buscar_receitas_otimizado(conn, recipe_hashes):
    """
    Busca FEPs, ingredientes e favoritos de múltiplas receitas em 3 queries.
    Retorna dicionários indexados por recipe_hash.
    
    Args:
        conn: Conexão SQLite
        recipe_hashes: Lista de hashes das receitas
        
    Returns:
        Tupla (feps_dict, ing_dict, fav_set)
    """
    if not recipe_hashes:
        return {}, {}, set()
    
    placeholders = ','.join('?' * len(recipe_hashes))
    
    # Query 1: Buscar todos os FEPs
    feps_dict = {}
    query_feps = f"SELECT recipe_hash, name, value, weight FROM feps WHERE recipe_hash IN ({placeholders})"
    for row in conn.execute(query_feps, recipe_hashes):
        hash_val = row['recipe_hash']
        if hash_val not in feps_dict:
            feps_dict[hash_val] = []
        feps_dict[hash_val].append({
            'name': row['name'],
            'value': row['value'],
            'weight': row['weight']
        })
    
    # Query 2: Buscar todos os ingredientes
    ing_dict = {}
    query_ing = f"SELECT recipe_hash, name, percentage FROM ingredients WHERE recipe_hash IN ({placeholders})"
    for row in conn.execute(query_ing, recipe_hashes):
        hash_val = row['recipe_hash']
        if hash_val not in ing_dict:
            ing_dict[hash_val] = []
        ing_dict[hash_val].append({
            'name': row['name'],
            'percentage': row['percentage']
        })
    
    # Query 3: Buscar favoritos
    query_fav = f"SELECT recipe_hash FROM favorite_recipes WHERE recipe_hash IN ({placeholders})"
    fav_set = set(row['recipe_hash'] for row in conn.execute(query_fav, recipe_hashes))
    
    return feps_dict, ing_dict, fav_set


def verificar_integridade_db(db_path):
    """
    Verifica a integridade do banco de dados.
    
    Returns:
        Tupla (sucesso, mensagem)
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verifica integridade
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()[0]
        
        if result != 'ok':
            return False, f"Integrity check failed: {result}"
        
        # Verifica se as tabelas existem
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        required_tables = {'recipes', 'ingredients', 'feps', 'favorite_recipes'}
        
        missing_tables = required_tables - tables
        if missing_tables:
            return False, f"Missing tables: {', '.join(missing_tables)}"
        
        conn.close()
        return True, "Database integrity OK"
        
    except Exception as e:
        return False, f"Error checking database: {str(e)}"
