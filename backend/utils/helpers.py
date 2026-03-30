from functools import wraps
from flask import session, flash, redirect, url_for
import json

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash("Accès refusé. Droits d'administrateur requis.", "danger")
            return redirect(url_for('main_routes.login'))
        return f(*args, **kwargs)
    return decorated_function

def from_json_filter(value):
    if not value:
        return None
    try:
        return json.loads(value)
    except:
        return None
