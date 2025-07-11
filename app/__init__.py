from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='../Frontend/frontend', static_url_path='/')
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set a strong secret key for session management
    from app.routes import main
    from app.options_api import options_api
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(options_api)
    app.register_blueprint(auth)
    return app
