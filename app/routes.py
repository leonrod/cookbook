"""
Rotas da API
"""
from flask import Blueprint, request, jsonify, render_template, current_app
import sqlite3
from app.database import get_db_connection, buscar_receitas_otimizado
from app.query_builder import construir_query, validar_parametros

# Blueprint para as rotas
bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    """Serve a página principal"""
    return render_template('index.html')


@bp.route('/api/ingredients')
def get_ingredients():
    """Retorna lista única de todos os ingredientes"""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute("""
                SELECT DISTINCT name 
                FROM ingredients 
                ORDER BY name
            """)
            ingredients = [row[0] for row in cursor.fetchall()]
        
        return jsonify({
            'ingredients': ingredients,
            'count': len(ingredients)
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching ingredients: {str(e)}")
        return jsonify({'error': 'Failed to fetch ingredients'}), 500


@bp.route('/api/recipes/names')
def get_recipe_names():
    """Retorna lista de nomes de todas as receitas"""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute("""
                SELECT DISTINCT item_name 
                FROM recipes 
                ORDER BY item_name
            """)
            recipes = [row[0] for row in cursor.fetchall()]
        
        return jsonify({
            'recipes': recipes,
            'count': len(recipes)
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching recipe names: {str(e)}")
        return jsonify({'error': 'Failed to fetch recipe names'}), 500


@bp.route('/health')
def health():
    """Endpoint de health check para monitoramento"""
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1").fetchone()
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': 'Database connection failed'
        }), 503


@bp.route('/api/search')
def search():
    """
    Endpoint de busca de receitas com filtros.
    
    Query Parameters:
        q (str): String de filtros (ex: "ing:pumpkin str>20%")
        sort (str): Campo para ordenação (default: efficiency)
        dir (str): Direção da ordenação - ASC ou DESC (default: DESC)
        
    Returns:
        JSON com lista de receitas encontradas
    """
    try:
        # Obter e validar parâmetros
        q = request.args.get('q', '')
        sort_key = request.args.get('sort', 'efficiency')
        sort_dir = request.args.get('dir', 'DESC').upper()
        
        # Validar tamanho da query
        max_query_length = current_app.config.get('API_MAX_QUERY_LENGTH', 500)
        if len(q) > max_query_length:
            return jsonify({
                'error': f'Query too long. Maximum length: {max_query_length}'
            }), 400
        
        # Validar parâmetros de ordenação
        valido, erro = validar_parametros(sort_key, sort_dir)
        if not valido:
            return jsonify({'error': erro}), 400
        
        # Construir query SQL
        sql, params = construir_query(q, sort_key, sort_dir)
        
        # Executar query e buscar dados relacionados
        with get_db_connection() as conn:
            # Query principal
            rows = conn.execute(sql, params).fetchall()
            
            # Buscar dados relacionados em lote (otimizado)
            recipe_hashes = [row['recipe_hash'] for row in rows]
            feps_dict, ing_dict, fav_set = buscar_receitas_otimizado(conn, recipe_hashes)
            
            # Montar resultado
            res = []
            for row in rows:
                r = dict(row)
                hash_val = r['recipe_hash']
                
                r['feps'] = feps_dict.get(hash_val, [])
                r['ingredients'] = ing_dict.get(hash_val, [])
                r['is_favorite'] = hash_val in fav_set
                
                res.append(r)
        
        return jsonify({'results': res})
    
    except ValueError as e:
        # Erro de validação ou parsing
        current_app.logger.warning(f"Validation error: {str(e)}")
        return jsonify({'error': 'Invalid request parameters'}), 400
    
    except sqlite3.Error as e:
        # Erro de banco de dados (não expõe detalhes)
        current_app.logger.error(f"Database error in search: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    
    except Exception as e:
        # Erro genérico (não expõe detalhes)
        current_app.logger.error(f"Unexpected error in search: {str(e)}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500


@bp.route('/api/stats')
def stats():
    """
    Retorna estatísticas gerais do banco de dados.
    
    Returns:
        JSON com estatísticas
    """
    try:
        with get_db_connection() as conn:
            stats_data = {
                'total_recipes': conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0],
                'total_ingredients': conn.execute("SELECT COUNT(DISTINCT name) FROM ingredients").fetchone()[0],
                'total_feps': conn.execute("SELECT COUNT(*) FROM feps").fetchone()[0],
                'total_favorites': conn.execute("SELECT COUNT(*) FROM favorite_recipes").fetchone()[0],
            }
        
        return jsonify(stats_data)
    
    except Exception as e:
        current_app.logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500


@bp.errorhandler(404)
def not_found(error):
    """Handler para erro 404"""
    return jsonify({'error': 'Resource not found'}), 404


@bp.errorhandler(500)
def internal_error(error):
    """Handler para erro 500"""
    current_app.logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500
