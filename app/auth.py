from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

DATABASE = 'anaconda_projects/db/project_filebrowser.db'

# Add prediction table
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        cur.execute('''CREATE TABLE predictions (
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

auth = Blueprint('auth', __name__)

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'message': 'Username and password required.'}), 400
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cur.fetchone():
        db.close()
        return jsonify({'message': 'Username already exists.'}), 400
    hashed_pw = generate_password_hash(password)
    cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
    db.commit()
    db.close()
    return jsonify({'message': 'Registration successful.'}), 200

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'message': 'Username and password required.'}), 400
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
    user = cur.fetchone()
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        db.close()
        return jsonify({
            'message': 'Login successful.',
            'username': user['username'],
            'user_id': user['id']
        }), 200
    db.close()
    return jsonify({'message': 'Invalid credentials.'}), 401

@auth.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Not logged in.'}), 401
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user = cur.fetchone()
    if user:
        return jsonify({'username': user['username']})
    return jsonify({'message': 'User not found.'}), 404

# Call init_db() at startup
init_db()
