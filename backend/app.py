import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, send_from_directory, session
from datetime import timedelta
from backend.models.database import init_db
from backend.utils.helpers import from_json_filter
from backend.routes.main_routes import main_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.api_routes import api_bp

def create_app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'frontend', 'html')
    static_dir = os.path.join(base_dir, 'frontend')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')

    app.secret_key = 'ensa_safi_secret_key'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False

    init_db()

    app.template_filter('from_json')(from_json_filter)

    @app.context_processor
    def inject_user():
        return dict(user=session.get('user_name'), logged_in=('user_id' in session), role=session.get('role'))

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        assets_dir = os.path.join(base_dir, 'assets')
        return send_from_directory(assets_dir, filename)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
