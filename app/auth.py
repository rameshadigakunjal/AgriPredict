from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import datetime

DATABASE = 'users.db'

auth = Blueprint('auth', __name__)

def init_db():
    """Initialize the database with users and predictions tables"""
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        
        # Create users table
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Create predictions table
        cur.execute('''CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            district TEXT,
            year INTEGER,
            area REAL,
            production REAL,
            temperature REAL,
            rainfall REAL,
            humidity REAL,
            predicted_yield REAL,
            predicted_n REAL,
            predicted_p REAL,
            predicted_k REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@auth.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        
        # Validate input
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        if len(username) < 3:
            return jsonify({'success': False, 'message': 'Username must be at least 3 characters long'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters long'}), 400
        
        # Check if username already exists
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cur.fetchone():
            db.close()
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        # Hash password and create user
        hashed_password = generate_password_hash(password)
        cur.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                   (username, hashed_password, email))
        db.commit()
        user_id = cur.lastrowid
        db.close()
        
        print(f"✅ User registered: {username} (ID: {user_id})")
        return jsonify({'success': True, 'message': 'Registration successful'}), 201
        
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@auth.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validate input
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400
        
        # Check user credentials
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            # Login successful
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['logged_in'] = True
            
            print(f"✅ User logged in: {username} (ID: {user['id']})")
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'username': user['username']
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@auth.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        username = session.get('username', 'Unknown')
        session.clear()
        print(f"✅ User logged out: {username}")
        return jsonify({'success': True, 'message': 'Logout successful'}), 200
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return jsonify({'success': False, 'message': 'Logout failed'}), 500

@auth.route('/profile', methods=['GET'])
def profile():
    """Get user profile"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'Not logged in'}), 401
        
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT id, username, email, created_at FROM users WHERE id = ?', (user_id,))
        user = cur.fetchone()
        db.close()
        
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'created_at': user['created_at']
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
            
    except Exception as e:
        print(f"❌ Profile error: {e}")
        return jsonify({'success': False, 'message': 'Failed to get profile'}), 500

@auth.route('/check_session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    try:
        user_id = session.get('user_id')
        username = session.get('username')
        logged_in = session.get('logged_in', False)
        
        if user_id and logged_in:
            return jsonify({
                'success': True,
                'logged_in': True,
                'user': {
                    'id': user_id,
                    'username': username
                }
            }), 200
        else:
            return jsonify({'success': True, 'logged_in': False}), 200
            
    except Exception as e:
        print(f"❌ Session check error: {e}")
        return jsonify({'success': False, 'message': 'Session check failed'}), 500

# Initialize database when module is imported
init_db()
