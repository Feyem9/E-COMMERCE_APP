"""
Routes d'administration pour le tableau de bord admin
"""
from flask import Blueprint
from controllers.admin_controller import (
    get_dashboard_stats,
    get_all_users,
    get_user_by_id,
    update_user_status,
    delete_user,
    get_all_products_admin,
    create_product,
    update_product,
    delete_product,
    get_all_orders_admin,
    update_order_status,
    get_all_transactions_admin,
    get_revenue_stats,
    get_recent_activity,
    # Nouvelles fonctionnalités
    export_users_csv,
    export_orders_csv,
    export_transactions_csv,
    get_charts_data,
    get_admin_notifications
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ============================================
# DASHBOARD STATISTICS
# ============================================
admin_bp.route('/stats', methods=['GET'])(get_dashboard_stats)
admin_bp.route('/stats/revenue', methods=['GET'])(get_revenue_stats)
admin_bp.route('/activity/recent', methods=['GET'])(get_recent_activity)

# ============================================
# USER MANAGEMENT
# ============================================
admin_bp.route('/users', methods=['GET'])(get_all_users)
admin_bp.route('/users/<int:user_id>', methods=['GET'])(get_user_by_id)
admin_bp.route('/users/<int:user_id>/status', methods=['PATCH'])(update_user_status)
admin_bp.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)

# ============================================
# PRODUCT MANAGEMENT
# ============================================
admin_bp.route('/products', methods=['GET'])(get_all_products_admin)
admin_bp.route('/products', methods=['POST'])(create_product)
admin_bp.route('/products/<int:product_id>', methods=['PUT'])(update_product)
admin_bp.route('/products/<int:product_id>', methods=['DELETE'])(delete_product)

# ============================================
# ORDER MANAGEMENT
# ============================================
admin_bp.route('/orders', methods=['GET'])(get_all_orders_admin)
admin_bp.route('/orders/<int:order_id>/status', methods=['PATCH'])(update_order_status)

# ============================================
# TRANSACTION MANAGEMENT
# ============================================
admin_bp.route('/transactions', methods=['GET'])(get_all_transactions_admin)

# ============================================
# EXPORT CSV
# ============================================
admin_bp.route('/export/users', methods=['GET'])(export_users_csv)
admin_bp.route('/export/orders', methods=['GET'])(export_orders_csv)
admin_bp.route('/export/transactions', methods=['GET'])(export_transactions_csv)

# ============================================
# ADVANCED CHARTS & NOTIFICATIONS
# ============================================
admin_bp.route('/charts', methods=['GET'])(get_charts_data)
admin_bp.route('/notifications', methods=['GET'])(get_admin_notifications)

# ============================================
# HEALTH CHECK & MONITORING
# ============================================
@admin_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check (public)"""
    from flask import jsonify
    try:
        from utils.logging_service import get_health_status
        status = get_health_status()
        return jsonify(status), 200 if status['status'] == 'healthy' else 503
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

@admin_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Endpoint de métriques (protégé)"""
    from flask import jsonify
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    try:
        from utils.logging_service import stats
        return jsonify({
            'status': 'ok',
            'stats': stats.get_stats()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
