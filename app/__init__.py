import os
from flask import Flask
from .database import init_db


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32).hex())
    app.config['DATABASE'] = os.path.join(app.instance_path, 'vaultkey.db')
    app.config['WTF_CSRF_ENABLED'] = True

    os.makedirs(app.instance_path, exist_ok=True)

    with app.app_context():
        init_db(app)

    from .routes import auth, vault
    app.register_blueprint(auth.bp)
    app.register_blueprint(vault.bp)

    return app
