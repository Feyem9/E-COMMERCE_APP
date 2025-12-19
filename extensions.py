# extensions.py
# Fichier séparé pour éviter les imports circulaires

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialiser limiter (sera configuré dans app.py)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    strategy="fixed-window"
)
