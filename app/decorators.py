from flask import redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from models import UserProfile

def perfil_required(*perfis):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            if current_user.profile not in perfis:
                return redirect(url_for("main.login"))
            return f(*args, **kwargs)
        return decorated
    return decorator