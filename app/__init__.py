from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='../Frontend/frontend', static_url_path='/')
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set a strong secret key for session management
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    from app.routes import main
    from app.options_api import options_api
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(options_api)
    app.register_blueprint(auth)
    
    # Add routes to serve frontend pages
    @app.route('/')
    def index():
        try:
            return send_from_directory(app.static_folder, 'index.html')
        except:
            return "<h1>Welcome to AgriPredict</h1><p><a href='/login'>Login</a> | <a href='/register'>Register</a></p>"
    
    @app.route('/login')
    @app.route('/login.html')
    def login():
        return send_from_directory(app.static_folder, 'login_new.html')
    
    @app.route('/register')
    @app.route('/register.html')
    def register():
        return send_from_directory(app.static_folder, 'register_new.html')
    
    @app.route('/predict.html')
    def predict():
        return send_from_directory(app.static_folder, 'predict.html')
    
    @app.route('/profile.html')
    def profile():
        return send_from_directory(app.static_folder, 'profile.html')
    
    @app.route('/help.html')
    def help():
        return send_from_directory(app.static_folder, 'help.html')
    
    return app
