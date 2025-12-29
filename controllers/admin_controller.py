"""
Contrôleur d'administration pour le tableau de bord admin
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from config import db
from models.customer_model import Customers
from models.product_model import Products
from models.order_model import Orders
from models.transaction_model import Transactions
from models.cart_model import Carts
from sqlalchemy import func, desc
from datetime import datetime, timedelta


def admin_required(f):
    """Décorateur pour vérifier que l'utilisateur est admin"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            customer_id = get_jwt_identity()
            customer = Customers.query.get(customer_id)
            
            if not customer:
                return jsonify({'error': 'Utilisateur non trouvé'}), 404
            
            if not customer.is_admin():
                return jsonify({'error': 'Accès refusé. Droits administrateur requis.'}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Admin check error: {str(e)}")
            return jsonify({'error': 'Erreur d\'authentification'}), 401
    
    return decorated_function


# ============================================
# DASHBOARD STATISTICS
# ============================================
@admin_required
def get_dashboard_stats():
    """Récupère les statistiques principales du dashboard"""
    try:
        # Nombre total d'utilisateurs
        total_users = Customers.query.count()
        new_users_today = Customers.query.filter(
            func.date(Customers.created_at) == datetime.utcnow().date()
        ).count()
        
        # Nombre total de produits
        total_products = Products.query.count()
        low_stock_products = Products.query.filter(Products.quantity < 10).count()
        
        # Nombre total de commandes
        total_orders = Orders.query.count()
        pending_orders = Orders.query.filter(Orders.status == 'pending').count()
        
        # Nombre total de transactions
        total_transactions = Transactions.query.count()
        completed_transactions = Transactions.query.filter(
            Transactions.status == 'completed'
        ).count()
        
        # Revenus totaux
        total_revenue = db.session.query(
            func.sum(Transactions.total_amount)
        ).filter(Transactions.status == 'completed').scalar() or 0
        
        # Revenus du jour
        today_revenue = db.session.query(
            func.sum(Transactions.total_amount)
        ).filter(
            Transactions.status == 'completed',
            func.date(Transactions.created_at) == datetime.utcnow().date()
        ).scalar() or 0
        
        # Revenus du mois
        first_day_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_revenue = db.session.query(
            func.sum(Transactions.total_amount)
        ).filter(
            Transactions.status == 'completed',
            Transactions.created_at >= first_day_of_month
        ).scalar() or 0
        
        return jsonify({
            'users': {
                'total': total_users,
                'new_today': new_users_today
            },
            'products': {
                'total': total_products,
                'low_stock': low_stock_products
            },
            'orders': {
                'total': total_orders,
                'pending': pending_orders
            },
            'transactions': {
                'total': total_transactions,
                'completed': completed_transactions
            },
            'revenue': {
                'total': total_revenue,
                'today': today_revenue,
                'monthly': monthly_revenue
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Dashboard stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def get_revenue_stats():
    """Récupère les statistiques de revenus sur les 30 derniers jours"""
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        # Revenus par jour sur les 30 derniers jours
        daily_revenue = db.session.query(
            func.date(Transactions.created_at).label('date'),
            func.sum(Transactions.total_amount).label('amount'),
            func.count(Transactions.transaction_id).label('count')
        ).filter(
            Transactions.status == 'completed',
            Transactions.created_at >= start_date
        ).group_by(
            func.date(Transactions.created_at)
        ).order_by(
            func.date(Transactions.created_at)
        ).all()
        
        # Formater les données pour le graphique
        chart_data = []
        for record in daily_revenue:
            chart_data.append({
                'date': str(record.date),
                'amount': float(record.amount or 0),
                'count': record.count
            })
        
        return jsonify({
            'daily_revenue': chart_data,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Revenue stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def get_recent_activity():
    """Récupère les activités récentes"""
    try:
        # Dernières transactions
        recent_transactions = Transactions.query.order_by(
            desc(Transactions.created_at)
        ).limit(10).all()
        
        # Derniers utilisateurs inscrits
        recent_users = Customers.query.order_by(
            desc(Customers.created_at)
        ).limit(5).all()
        
        # Dernières commandes
        recent_orders = Orders.query.order_by(
            desc(Orders.created_at)
        ).limit(5).all()
        
        return jsonify({
            'recent_transactions': [t.serialize() for t in recent_transactions],
            'recent_users': [{
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'created_at': u.created_at.isoformat() if u.created_at else None
            } for u in recent_users],
            'recent_orders': [o.serialize() for o in recent_orders]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Recent activity error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================
# USER MANAGEMENT
# ============================================
@admin_required
def get_all_users():
    """Récupère tous les utilisateurs avec pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        role_filter = request.args.get('role', '', type=str)
        
        query = Customers.query
        
        # Filtrer par recherche
        if search:
            query = query.filter(
                (Customers.name.ilike(f'%{search}%')) |
                (Customers.email.ilike(f'%{search}%'))
            )
        
        # Filtrer par rôle
        if role_filter:
            query = query.filter(Customers.role == role_filter)
        
        # Pagination
        pagination = query.order_by(desc(Customers.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        users = [{
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'contact': u.contact,
            'address': u.address,
            'role': u.role,
            'confirmed': u.confirmed,
            'is_active': u.is_active,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in pagination.items]
        
        return jsonify({
            'users': users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get users error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def get_user_by_id(user_id):
    """Récupère un utilisateur par son ID"""
    try:
        user = Customers.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'contact': user.contact,
            'address': user.address,
            'role': user.role,
            'confirmed': user.confirmed,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def update_user_status(user_id):
    """Met à jour le statut d'un utilisateur (actif/inactif, rôle)"""
    try:
        user = Customers.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        if 'role' in data:
            if data['role'] in ['user', 'admin']:
                user.role = data['role']
            else:
                return jsonify({'error': 'Rôle invalide'}), 400
        
        if 'confirmed' in data:
            user.confirmed = data['confirmed']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Utilisateur mis à jour avec succès',
            'user': {
                'id': user.id,
                'name': user.name,
                'role': user.role,
                'is_active': user.is_active,
                'confirmed': user.confirmed
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update user error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def delete_user(user_id):
    """Supprime un utilisateur"""
    try:
        user = Customers.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Empêcher la suppression d'un admin
        if user.is_admin():
            return jsonify({'error': 'Impossible de supprimer un administrateur'}), 403
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete user error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================
# PRODUCT MANAGEMENT
# ============================================
@admin_required
def get_all_products_admin():
    """Récupère tous les produits avec pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        
        query = Products.query
        
        if search:
            query = query.filter(
                (Products.name.ilike(f'%{search}%')) |
                (Products.description.ilike(f'%{search}%'))
            )
        
        pagination = query.order_by(desc(Products.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        products = [p.serialize() for p in pagination.items]
        
        return jsonify({
            'products': products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get products error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def create_product():
    """Crée un nouveau produit"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'description', 'current_price', 'discount_price', 'quantity', 'picture']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        new_product = Products(
            name=data['name'],
            description=data['description'],
            current_price=float(data['current_price']),
            discount_price=float(data['discount_price']),
            quantity=int(data['quantity']),
            picture=data['picture']
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            'message': 'Produit créé avec succès',
            'product': new_product.serialize()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create product error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def update_product(product_id):
    """Met à jour un produit"""
    try:
        product = Products.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Produit non trouvé'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'current_price' in data:
            product.current_price = float(data['current_price'])
        if 'discount_price' in data:
            product.discount_price = float(data['discount_price'])
        if 'quantity' in data:
            product.quantity = int(data['quantity'])
        if 'picture' in data:
            product.picture = data['picture']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Produit mis à jour avec succès',
            'product': product.serialize()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update product error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def delete_product(product_id):
    """Supprime un produit"""
    try:
        product = Products.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Produit non trouvé'}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Produit supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete product error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================
# ORDER MANAGEMENT
# ============================================
@admin_required
def get_all_orders_admin():
    """Récupère toutes les commandes avec pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status', '', type=str)
        
        query = Orders.query
        
        if status_filter:
            query = query.filter(Orders.status == status_filter)
        
        pagination = query.order_by(desc(Orders.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        orders = [o.serialize() for o in pagination.items]
        
        return jsonify({
            'orders': orders,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get orders error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def update_order_status(order_id):
    """Met à jour le statut d'une commande"""
    try:
        order = Orders.query.get(order_id)
        
        if not order:
            return jsonify({'error': 'Commande non trouvée'}), 404
        
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Statut requis'}), 400
        
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Statut invalide. Valeurs acceptées: {valid_statuses}'}), 400
        
        order.status = data['status']
        db.session.commit()
        
        return jsonify({
            'message': 'Statut mis à jour avec succès',
            'order': order.serialize()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update order error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================
# TRANSACTION MANAGEMENT
# ============================================
@admin_required
def get_all_transactions_admin():
    """Récupère toutes les transactions avec pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status', '', type=str)
        
        query = Transactions.query
        
        if status_filter:
            query = query.filter(Transactions.status == status_filter)
        
        pagination = query.order_by(desc(Transactions.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        transactions = [t.serialize() for t in pagination.items]
        
        return jsonify({
            'transactions': transactions,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get transactions error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================
# EXPORT FUNCTIONS (CSV)
# ============================================
@admin_required
def export_users_csv():
    """Exporte les utilisateurs en CSV"""
    try:
        import csv
        from io import StringIO
        from flask import Response
        
        users = Customers.query.all()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # En-têtes
        writer.writerow(['ID', 'Nom', 'Email', 'Contact', 'Adresse', 'Rôle', 'Confirmé', 'Actif', 'Date inscription'])
        
        # Données
        for u in users:
            writer.writerow([
                u.id, u.name, u.email, u.contact, u.address, 
                u.role, u.confirmed, u.is_active,
                u.created_at.strftime('%Y-%m-%d %H:%M') if u.created_at else ''
            ])
        
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=users_export.csv',
                'Access-Control-Expose-Headers': 'Content-Disposition'
            }
        )
        
    except Exception as e:
        current_app.logger.error(f"Export users error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def export_orders_csv():
    """Exporte les commandes en CSV"""
    try:
        import csv
        from io import StringIO
        from flask import Response
        
        orders = Orders.query.all()
        
        output = StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['ID', 'Quantité', 'Prix', 'Statut', 'Cart ID', 'Date création'])
        
        for o in orders:
            writer.writerow([
                o.id, o.quantity, o.price, o.status, o.cart_id,
                o.created_at.strftime('%Y-%m-%d %H:%M') if o.created_at else ''
            ])
        
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=orders_export.csv',
                'Access-Control-Expose-Headers': 'Content-Disposition'
            }
        )
        
    except Exception as e:
        current_app.logger.error(f"Export orders error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@admin_required
def export_transactions_csv():
    """Exporte les transactions en CSV"""
    try:
        import csv
        from io import StringIO
        from flask import Response
        
        transactions = Transactions.query.all()
        
        output = StringIO()
        writer = csv.writer(output)
        
        writer.writerow(['Transaction ID', 'Statut', 'Montant', 'Devise', 'Reference', 'Date création'])
        
        for t in transactions:
            writer.writerow([
                t.transaction_id, t.status, t.total_amount, t.currency,
                getattr(t, 'reference', ''),
                t.created_at.strftime('%Y-%m-%d %H:%M') if t.created_at else ''
            ])
        
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=transactions_export.csv',
                'Access-Control-Expose-Headers': 'Content-Disposition'
            }
        )
        
    except Exception as e:
        current_app.logger.error(f"Export transactions error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================
# ADVANCED CHARTS DATA
# ============================================
@admin_required
def get_charts_data():
    """Récupère les données pour les graphiques avancés"""
    try:
        # Répartition des statuts de commandes
        orders_by_status = db.session.query(
            Orders.status,
            func.count(Orders.id).label('count')
        ).group_by(Orders.status).all()
        
        # Répartition des utilisateurs par rôle
        users_by_role = db.session.query(
            Customers.role,
            func.count(Customers.id).label('count')
        ).group_by(Customers.role).all()
        
        # Top 5 produits les plus vendus
        try:
            top_products = db.session.query(
                Products.name,
                func.sum(Orders.quantity).label('total_sold')
            ).join(Orders, Orders.product_id == Products.id) \
             .group_by(Products.id, Products.name) \
             .order_by(func.sum(Orders.quantity).desc()) \
             .limit(5).all()
        except Exception:
            top_products = []
        
        # Pour les requêtes avec dates, on simplifie pour compatibilité SQLite/PostgreSQL
        # On retourne juste les données agrégées sans groupement par date
        monthly_revenue = []
        weekly_signups = []
        
        # Revenus totaux des 6 derniers mois (simplifié)
        try:
            six_months_ago = datetime.utcnow() - timedelta(days=180)
            total_revenue_6m = db.session.query(
                func.sum(Transactions.total_amount)
            ).filter(
                Transactions.status == 'completed',
                Transactions.created_at >= six_months_ago
            ).scalar() or 0
            
            if total_revenue_6m > 0:
                monthly_revenue = [{'month': 'Total 6 mois', 'amount': float(total_revenue_6m)}]
        except Exception:
            pass
        
        # Inscriptions des 4 dernières semaines (simplifié)
        try:
            four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)
            total_signups_4w = db.session.query(
                func.count(Customers.id)
            ).filter(
                Customers.created_at >= four_weeks_ago
            ).scalar() or 0
            
            if total_signups_4w > 0:
                weekly_signups = [{'week': 'Total 4 semaines', 'count': total_signups_4w}]
        except Exception:
            pass
        
        return jsonify({
            'orders_by_status': [{'status': s or 'unknown', 'count': c} for s, c in orders_by_status],
            'users_by_role': [{'role': r or 'user', 'count': c} for r, c in users_by_role],
            'top_products': [{'name': n, 'total_sold': int(ts or 0)} for n, ts in top_products],
            'monthly_revenue': monthly_revenue,
            'weekly_signups': weekly_signups
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Charts data error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================
# NOTIFICATIONS / ALERTS
# ============================================
@admin_required
def get_admin_notifications():
    """Récupère les notifications/alertes pour l'admin"""
    try:
        notifications = []
        
        # Alerte: Produits en stock faible
        low_stock_count = Products.query.filter(Products.quantity < 10).count()
        if low_stock_count > 0:
            notifications.append({
                'type': 'warning',
                'icon': '📦',
                'title': 'Stock faible',
                'message': f'{low_stock_count} produit(s) ont un stock inférieur à 10',
                'action': '/admin/products',
                'priority': 'high'
            })
        
        # Alerte: Commandes en attente
        pending_orders = Orders.query.filter(Orders.status == 'pending').count()
        if pending_orders > 0:
            notifications.append({
                'type': 'info',
                'icon': '🛒',
                'title': 'Commandes en attente',
                'message': f'{pending_orders} commande(s) en attente de traitement',
                'action': '/admin/orders',
                'priority': 'medium'
            })
        
        # Alerte: Nouveaux utilisateurs aujourd'hui
        new_users_today = Customers.query.filter(
            func.date(Customers.created_at) == datetime.utcnow().date()
        ).count()
        if new_users_today > 0:
            notifications.append({
                'type': 'success',
                'icon': '👥',
                'title': 'Nouveaux utilisateurs',
                'message': f'{new_users_today} nouveau(x) utilisateur(s) inscrit(s) aujourd\'hui',
                'action': '/admin/users',
                'priority': 'low'
            })
        
        # Alerte: Transactions échouées récemment
        failed_transactions_24h = Transactions.query.filter(
            Transactions.status == 'failed',
            Transactions.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        if failed_transactions_24h > 0:
            notifications.append({
                'type': 'danger',
                'icon': '❌',
                'title': 'Transactions échouées',
                'message': f'{failed_transactions_24h} transaction(s) échouée(s) dans les dernières 24h',
                'action': '/admin/transactions',
                'priority': 'high'
            })
        
        # Alerte: Revenus du jour
        today_revenue = db.session.query(
            func.sum(Transactions.total_amount)
        ).filter(
            Transactions.status == 'completed',
            func.date(Transactions.created_at) == datetime.utcnow().date()
        ).scalar() or 0
        
        if today_revenue > 0:
            notifications.append({
                'type': 'success',
                'icon': '💰',
                'title': 'Revenus du jour',
                'message': f'{today_revenue:,.0f} XAF générés aujourd\'hui',
                'action': '/admin',
                'priority': 'low'
            })
        
        # Trier par priorité
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        notifications.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return jsonify({
            'notifications': notifications,
            'count': len(notifications)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Notifications error: {str(e)}")
        return jsonify({'error': str(e)}), 500

