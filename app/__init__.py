from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__, static_folder='../Frontend/frontend', static_url_path='/')
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set a strong secret key for session management
    
    # Route to serve HTML files
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory(app.static_folder, filename)
    
    from app.routes import main
    from app.options_api import options_api
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(options_api)
    app.register_blueprint(auth)
    return app
