"""
Módulo de construção de queries SQL dinâmicas
"""
import re
from flask import current_app


# Mapeamento de abreviações de stats para nomes completos
MAPA_STATS = {
    "str": "Strength",
    "agi": "Agility",
    "int": "Intelligence",
    "con": "Constitution",
    "dex": "Dexterity",
    "per": "Perception",
    "wil": "Will",
    "psy": "Psyche",
    "cha": "Charisma"
}

# Whitelist de valores válidos para ordenação
VALID_SORT_KEYS = {
    'name', 'hunger', 'energy', 'total', 'efficiency',
    'str', 'agi', 'int', 'con', 'dex', 'per', 'wil', 'psy', 'cha'
}
VALID_SORT_DIRS = {'ASC', 'DESC'}


def validar_parametros(sort_key, sort_dir):
    """
    Valida parâmetros de ordenação contra whitelist.
    
    Args:
        sort_key: Chave de ordenação
        sort_dir: Direção de ordenação
        
    Returns:
        Tupla (valido, mensagem_erro)
    """
    if sort_key not in VALID_SORT_KEYS:
        return False, f"Invalid sort_key. Allowed: {', '.join(sorted(VALID_SORT_KEYS))}"
    
    if sort_dir not in VALID_SORT_DIRS:
        return False, f"Invalid sort_dir. Allowed: {', '.join(VALID_SORT_DIRS)}"
    
    return True, None


def construir_query(texto, sort_key, sort_dir):
    """
    Constrói uma query SQL dinâmica baseada nos filtros fornecidos.
    
    Args:
        texto: String de filtros (ex: "ing:pumpkin str>20%")
        sort_key: Campo para ordenação
        sort_dir: Direção da ordenação (ASC/DESC)
        
    Returns:
        Tupla (sql, params) onde sql é a query e params são os valores parametrizados
    """
    sql = "SELECT DISTINCT r.* FROM recipes r"
    condicoes = []
    params = []
    
    # Sanitiza e tokeniza o texto de busca
    tokens = texto.lower().replace(';', ' ').split()
    
    for t in tokens:
        # 1. Filtro de INGREDIENTE
        if t.startswith('ing:'):
            val = t.split(':', 1)[1]
            if len(val) > 0:
                condicoes.append(
                    "EXISTS (SELECT 1 FROM ingredients i "
                    "WHERE i.recipe_hash = r.recipe_hash AND i.name LIKE ?)"
                )
                params.append(f"%{val}%")
            continue

        # 2. Filtro de NOME
        if t.startswith('name:'):
            val = t.split(':', 1)[1]
            # Remover aspas se existirem
            val = val.strip('"').strip("'")
            if len(val) > 0:
                condicoes.append("r.item_name LIKE ?")
                params.append(f"%{val}%")
            continue

        # 3. Filtro de FAVORITO
        if t.startswith('fav:'):
            if "fav_join" not in sql:
                sql += " LEFT JOIN favorite_recipes fav ON r.recipe_hash = fav.recipe_hash"
            condicoes.append("fav.recipe_hash IS NOT NULL")
            continue

        # 4. Filtros Numéricos (Stats, Total) via Regex
        # Suporta filtro por nível: str2>10 (Strength +2) ou str>10 (qualquer Strength)
        match = re.match(r"([a-z:]+)(\d*)(>=|<=|>|<|=)([\d\.]+)(%?)", t)
        if match:
            chave, nivel, op, val, perc = match.groups()
            
            try:
                val = float(val)
            except ValueError:
                continue  # Ignora valores inválidos
            
            if chave == 'total':
                condicoes.append(f"r.total_fep {op} ?")
                params.append(val)
            else:
                stat = next((v for k, v in MAPA_STATS.items() if chave.startswith(k)), None)
                if stat:
                    col = "weight" if perc == "%" else "value"
                    if perc == "%":
                        val /= 100.0
                    
                    # Se tiver nível específico (ex: str2), busca exato "Strength +2"
                    if nivel:
                        target_name = f"{stat} +{nivel}"
                        condicoes.append(
                            f"EXISTS (SELECT 1 FROM feps f "
                            f"WHERE f.recipe_hash=r.recipe_hash AND f.name = ? AND f.{col} {op} ?)"
                        )
                        params.append(target_name)
                    # Se não tiver nível, busca genérico "Strength%"
                    else:
                        target_name = f"{stat}%"
                        condicoes.append(
                            f"EXISTS (SELECT 1 FROM feps f "
                            f"WHERE f.recipe_hash=r.recipe_hash AND f.name LIKE ? AND f.{col} {op} ?)"
                        )
                        params.append(target_name)
                    
                    params.append(val)

    # Construir cláusula de ordenação
    order_clause = _construir_order_clause(sort_key, sort_dir, sql, params)
    
    # Montar query final
    if condicoes:
        sql += " WHERE " + " AND ".join(condicoes)
    
    limit = current_app.config.get('API_RESULTS_LIMIT', 50)
    final_sql = sql + order_clause + f" LIMIT {limit}"
    
    return final_sql, params


def _construir_order_clause(sort_key, sort_dir, sql, params):
    """
    Constrói a cláusula ORDER BY de forma segura.
    
    Args:
        sort_key: Campo para ordenação
        sort_dir: Direção da ordenação
        sql: Query SQL atual (modificada por referência se necessário)
        params: Lista de parâmetros (modificada se necessário)
        
    Returns:
        String com a cláusula ORDER BY
    """
    if sort_key in MAPA_STATS:
        stat_full_name = MAPA_STATS[sort_key]
        # Usa parametrização no LIKE para segurança adicional
        # Nota: Como estamos modificando sql, isso precisa ser feito antes do WHERE
        # Por isso, retornamos apenas a cláusula ORDER BY
        params.append(f"{stat_full_name}%")
        return (
            f" LEFT JOIN feps f_sort ON r.recipe_hash = f_sort.recipe_hash "
            f"AND f_sort.name LIKE ? "
            f"ORDER BY COALESCE(f_sort.value, 0) {sort_dir}"
        )
    elif sort_key == 'efficiency':
        return f" ORDER BY (r.total_fep / NULLIF(r.hunger, 0)) {sort_dir}"
    elif sort_key == 'name':
        return f" ORDER BY r.item_name {sort_dir}"
    elif sort_key == 'hunger':
        return f" ORDER BY r.hunger {sort_dir}"
    elif sort_key == 'energy':
        return f" ORDER BY r.energy {sort_dir}"
    else:
        return f" ORDER BY r.total_fep {sort_dir}"
