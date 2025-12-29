"""
📊 Service de Logging et Monitoring
Centralise les logs de l'application avec différents niveaux
"""

import logging
import os
import json
from datetime import datetime
from functools import wraps
from flask import request, g, current_app


# ============================================
# CONFIGURATION DU LOGGER
# ============================================

def setup_logging(app):
    """Configure le logging pour l'application Flask"""
    
    # Niveau de log basé sur l'environnement
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    # Format de log
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, log_level))
    
    # Configurer le logger de l'application
    app.logger.handlers = []
    app.logger.addHandler(console_handler)
    app.logger.setLevel(getattr(logging, log_level))
    
    # Log de démarrage
    app.logger.info(f"📊 Logging configuré - Niveau: {log_level}")
    
    return app.logger


# ============================================
# LOGGER PERSONNALISÉ
# ============================================

class AppLogger:
    """Logger personnalisé avec méthodes métier"""
    
    def __init__(self, name='theck_market'):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '[%(asctime)s] %(levelname)s: %(message)s'
            ))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _format_message(self, message, extra=None):
        """Formate le message avec des données supplémentaires"""
        if extra:
            return f"{message} | {json.dumps(extra, default=str)}"
        return message
    
    # Méthodes de base
    def info(self, message, extra=None):
        self.logger.info(self._format_message(message, extra))
    
    def warning(self, message, extra=None):
        self.logger.warning(self._format_message(message, extra))
    
    def error(self, message, extra=None):
        self.logger.error(self._format_message(message, extra))
    
    def debug(self, message, extra=None):
        self.logger.debug(self._format_message(message, extra))
    
    # Méthodes métier
    def log_request(self, endpoint, method, user_id=None):
        """Log une requête API"""
        self.info(f"📥 {method} {endpoint}", {
            'user_id': user_id,
            'ip': request.remote_addr if request else None,
            'user_agent': request.headers.get('User-Agent', '')[:50] if request else None
        })
    
    def log_response(self, endpoint, status_code, duration_ms):
        """Log une réponse API"""
        emoji = "✅" if status_code < 400 else "❌"
        self.info(f"{emoji} Response {status_code} in {duration_ms:.2f}ms", {
            'endpoint': endpoint,
            'status': status_code,
            'duration_ms': duration_ms
        })
    
    def log_user_action(self, action, user_id, details=None):
        """Log une action utilisateur"""
        self.info(f"👤 User action: {action}", {
            'user_id': user_id,
            'action': action,
            'details': details
        })
    
    def log_payment(self, transaction_id, amount, status, user_id=None):
        """Log une transaction de paiement"""
        emoji = "💳" if status == 'success' else "⚠️"
        self.info(f"{emoji} Payment {status}: {amount} XAF", {
            'transaction_id': transaction_id,
            'amount': amount,
            'status': status,
            'user_id': user_id
        })
    
    def log_order(self, order_id, status, user_id=None):
        """Log un changement de statut de commande"""
        self.info(f"📦 Order {order_id}: {status}", {
            'order_id': order_id,
            'status': status,
            'user_id': user_id
        })
    
    def log_security_event(self, event_type, details):
        """Log un événement de sécurité"""
        self.warning(f"🔐 Security: {event_type}", {
            'type': event_type,
            'details': details,
            'ip': request.remote_addr if request else None
        })
    
    def log_error(self, error, context=None):
        """Log une erreur avec contexte"""
        self.error(f"❌ Error: {str(error)}", {
            'error_type': type(error).__name__,
            'context': context,
            'ip': request.remote_addr if request else None
        })


# Instance globale
logger = AppLogger()


# ============================================
# DÉCORATEUR DE LOGGING
# ============================================

def log_endpoint(func):
    """Décorateur pour logger automatiquement les endpoints"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        
        # Log de la requête
        endpoint = request.path if request else 'unknown'
        method = request.method if request else 'unknown'
        
        try:
            result = func(*args, **kwargs)
            
            # Calculer la durée
            duration_ms = (time.time() - start_time) * 1000
            
            # Log de la réponse
            status_code = result[1] if isinstance(result, tuple) else 200
            logger.log_response(endpoint, status_code, duration_ms)
            
            return result
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            logger.log_error(e, {'endpoint': endpoint, 'method': method})
            raise
    
    return wrapper


# ============================================
# STATISTIQUES EN TEMPS RÉEL
# ============================================

class StatsCollector:
    """Collecteur de statistiques en mémoire"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Réinitialise les compteurs"""
        self._stats = {
            'requests_total': 0,
            'requests_success': 0,
            'requests_error': 0,
            'requests_by_endpoint': {},
            'users_active': set(),
            'orders_today': 0,
            'revenue_today': 0,
            'last_reset': datetime.utcnow().isoformat()
        }
    
    def increment_request(self, endpoint, success=True):
        """Incrémente les compteurs de requêtes"""
        self._stats['requests_total'] += 1
        if success:
            self._stats['requests_success'] += 1
        else:
            self._stats['requests_error'] += 1
        
        if endpoint not in self._stats['requests_by_endpoint']:
            self._stats['requests_by_endpoint'][endpoint] = 0
        self._stats['requests_by_endpoint'][endpoint] += 1
    
    def track_user(self, user_id):
        """Marque un utilisateur comme actif"""
        if user_id:
            self._stats['users_active'].add(user_id)
    
    def add_order(self, amount):
        """Ajoute une commande aux stats"""
        self._stats['orders_today'] += 1
        self._stats['revenue_today'] += amount
    
    def get_stats(self):
        """Retourne les statistiques actuelles"""
        return {
            **self._stats,
            'users_active': len(self._stats['users_active'])
        }


# Instance globale
stats = StatsCollector()


# ============================================
# ENDPOINT DE HEALTH CHECK
# ============================================

def get_health_status():
    """Retourne le status de santé de l'application"""
    from config import db
    
    status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'checks': {}
    }
    
    # Check database
    try:
        db.session.execute('SELECT 1')
        status['checks']['database'] = {'status': 'ok'}
    except Exception as e:
        status['checks']['database'] = {'status': 'error', 'message': str(e)}
        status['status'] = 'unhealthy'
    
    # Check memory (optionnel)
    try:
        import psutil
        memory = psutil.virtual_memory()
        status['checks']['memory'] = {
            'status': 'ok' if memory.percent < 90 else 'warning',
            'used_percent': memory.percent
        }
    except:
        pass
    
    return status
