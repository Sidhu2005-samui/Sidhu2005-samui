import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, url_for, session, render_template, redirect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ICON_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'icons')
ALLOWED_EXTENSIONS = {'apk', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ICON_FOLDER'] = ICON_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ICON_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"

# --- User Authentication ---
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    password_hash = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                (username, password_hash, email)
            )
            conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'message': 'Logged in successfully'}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# --- User Features (Reviews) ---
@app.route('/api/apps/<int:app_id>/reviews', methods=['POST'])
def add_review(app_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401

    data = request.json
    rating = data.get('rating')
    comment = data.get('comment')

    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({'error': 'Valid rating (1-5) required'}), 400

    try:
        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO reviews (app_id, user_id, rating, comment) VALUES (?, ?, ?, ?)',
                (app_id, session['user_id'], rating, comment)
            )
            conn.commit()
        return jsonify({'message': 'Review added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- App Management ---
@app.route('/api/apps', methods=['POST'])
def upload_app():
    if 'apk' not in request.files:
        return jsonify({'error': 'No APK file provided'}), 400

    apk_file = request.files['apk']
    icon_file = request.files.get('icon')

    if apk_file.filename == '':
        return jsonify({'error': 'No selected APK file'}), 400

    name = request.form.get('name')
    package_name = request.form.get('package_name')
    description = request.form.get('description')
    version = request.form.get('version')
    category = request.form.get('category')

    if not all([name, package_name, version]):
        return jsonify({'error': 'Missing required metadata (name, package_name, version)'}), 400

    if apk_file and allowed_file(apk_file.filename):
        apk_filename = generate_unique_filename(secure_filename(apk_file.filename))
        apk_file.save(os.path.join(app.config['UPLOAD_FOLDER'], apk_filename))

        icon_filename = None
        if icon_file and allowed_file(icon_file.filename):
            icon_filename = generate_unique_filename(secure_filename(icon_file.filename))
            icon_file.save(os.path.join(app.config['ICON_FOLDER'], icon_filename))

        try:
            with get_db_connection() as conn:
                conn.execute(
                    'INSERT INTO apps (name, package_name, description, version, category, apk_filename, icon_filename) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (name, package_name, description, version, category, apk_filename, icon_filename)
                )
                conn.commit()
            return jsonify({'message': 'App uploaded successfully'}), 201
        except Exception as e:
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], apk_filename)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], apk_filename))
            if icon_filename and os.path.exists(os.path.join(app.config['ICON_FOLDER'], icon_filename)):
                os.remove(os.path.join(app.config['ICON_FOLDER'], icon_filename))
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/apps', methods=['GET'])
def list_apps():
    category = request.args.get('category')
    search = request.args.get('search')

    query = 'SELECT * FROM apps WHERE 1=1'
    params = []

    if category:
        query += ' AND category = ?'
        params.append(category)

    if search:
        query += ' AND (name LIKE ? OR description LIKE ?)'
        params.append(f'%{search}%')
        params.append(f'%{search}%')

    conn = get_db_connection()
    apps = conn.execute(query, params).fetchall()
    conn.close()

    result = []
    for app_row in apps:
        app_data = dict(app_row)
        app_data['download_url'] = url_for('download_apk', filename=app_row['apk_filename'], _external=True)
        if app_row['icon_filename']:
            app_data['icon_url'] = url_for('static', filename=f'icons/{app_row["icon_filename"]}', _external=True)
        result.append(app_data)

    return jsonify(result)

@app.route('/api/apps/<int:app_id>', methods=['GET'])
def get_app(app_id):
    conn = get_db_connection()
    app_row = conn.execute('SELECT * FROM apps WHERE id = ?', (app_id,)).fetchone()

    if app_row is None:
        conn.close()
        return jsonify({'error': 'App not found'}), 404

    reviews = conn.execute('SELECT r.*, u.username FROM reviews r JOIN users u ON r.user_id = u.id WHERE r.app_id = ? ORDER BY r.created_at DESC', (app_id,)).fetchall()
    conn.close()

    app_data = dict(app_row)
    app_data['download_url'] = url_for('download_apk', filename=app_row['apk_filename'], _external=True)
    if app_row['icon_filename']:
        app_data['icon_url'] = url_for('static', filename=f'icons/{app_row["icon_filename"]}', _external=True)

    app_data['reviews'] = [dict(r) for r in reviews]

    return jsonify(app_data)

@app.route('/api/download/<filename>', methods=['GET'])
def download_apk(filename):
    # Track download
    try:
        conn = get_db_connection()
        app_row = conn.execute('SELECT id FROM apps WHERE apk_filename = ?', (filename,)).fetchone()
        if app_row:
            app_id = app_row['id']
            user_id = session.get('user_id')
            conn.execute('INSERT INTO downloads (app_id, user_id) VALUES (?, ?)', (app_id, user_id))
            conn.execute('UPDATE apps SET downloads_count = downloads_count + 1 WHERE id = ?', (app_id,))
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error tracking download: {e}")

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Frontend Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/apps/<int:app_id>')
def app_details_page(app_id):
    return render_template('app_details.html', app_id=app_id)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5002)
