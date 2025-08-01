from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_restx import abort

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user or not current_user.get('is_admin', False):
            abort(403, "Admin privileges required")
        return f(*args, **kwargs)
    return decorated_function
