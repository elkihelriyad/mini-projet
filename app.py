from flask import Flask, render_template, request, jsonify, session, g, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from functools import wraps
import sqlite3
import os
import json
import numpy as np
from datetime import datetime
from collections import Counter

app = Flask(__name__)
app.secret_key = 'ensa_safi_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False # Set to True in production

DB_PATH = 'ensa_orientation.db'

# --- Database Helper ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Init DB ---
def init_db():
    if not os.path.exists(DB_PATH):
        print("Initializing database...")
        conn = get_db_connection()
        try:
            with open('schema.sql', 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        except Exception as e:
            print(f"Schema error: {e}")
        conn.close()
        print("Database initialized.")

# --- Filters ---
@app.template_filter('from_json')
def from_json(value):
    if not value:
        return None
    try:
        return json.loads(value)
    except:
        return None

# --- Context Processors ---
@app.context_processor
def inject_user():
    return dict(user=session.get('user_name'), logged_in=('user_id' in session), role=session.get('role'))

@app.before_request
def make_session_permanent():
    session.permanent = True

# --- Decorators ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash("Accès refusé. Droits d'administrateur requis.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    session.pop('test_seed', None) 
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Pass 'next' arg to template if GET so form can include it
    next_page = request.args.get('next')

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        code = request.form.get('password', '').strip() 
        
        # 0. Capture Temp Results BEFORE any session clearing
        temp_results = session.get('temp_results')

        if not email.endswith('@uca.ac.ma') and not email.endswith('ensas.uca.ma'):
            return render_template('login.html', error="Email académique requis (@uca.ac.ma)", next=next_page)
            
        conn = get_db_connection()
        try:
            # Check if role column exists (handling migration implicitly if simple select fails, but assume migration ran)
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        except:
             user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        valid_user = False
        if user:
            # Check hash
            try:
                if check_password_hash(user['access_code'], code):
                    valid_user = True
            except:
                # Fallback for plain text
                if user['access_code'] == code:
                    valid_user = True
        
        if valid_user:
            # Check Active Status
            # We assume is_active is 1 by default, but if it is explicitly 0, deny.
            is_active = user['is_active'] if 'is_active' in user.keys() else 1
            if is_active == 0:
                flash('Ce compte a été désactivé par l\'administrateur.', 'error')
                conn.close()
                return render_template('login.html')

            # 1. Establish Session
            session.clear() 
            session['user_id'] = user['id']
            # Only store user name if it is available, otherwise user empty string
            session['user_name'] = user['nom_complet'] if user['nom_complet'] else email.split('@')[0]
            # Handle role safely (default to student if column missing/null)
            session['role'] = user['role'] if 'role' in user.keys() and user['role'] else 'student'
            session.permanent = True
            
            # Admin Redirect
            if session['role'] == 'admin':
                conn.close()
                return redirect(url_for('admin_analytics'))
            
            # 2. The Fusion (Merge Logic)
            fusion_occurred = False
            if temp_results:
                try:
                    results_json = json.dumps(temp_results)
                    # Insert into results table to persist history
                    conn.execute('INSERT INTO results (user_id, date_test, result_json, profile_type) VALUES (?, ?, ?, ?)', 
                               (user['id'], datetime.now(), results_json, temp_results.get('profile_type')))
                    
                    # Update user profile
                    conn.execute('UPDATE users SET last_result_json = ?, date_test = ?, profile_type = ? WHERE id = ?', 
                               (results_json, datetime.now(), temp_results.get('profile_type'), user['id']))
                    conn.commit()
                    fusion_occurred = True
                except Exception as e:
                    print(f"Merge Error: {e}")
            
            conn.close()
            
            # 3. Redirection Logic targeting students
            target = request.args.get('next')
            if not target and fusion_occurred:
                target = url_for('dashboard')
            
            return redirect(target or url_for('index'))
            
        else:
            conn.close()
            return render_template('login.html', error="Adresse e-mail ou code incorrect. Veuillez réessayer.", next=next_page)

    return render_template('login.html', next=next_page)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    # Fetch full history
    history_rows = conn.execute('SELECT * FROM results WHERE user_id = ? ORDER BY date_test DESC', (session['user_id'],)).fetchall()
    conn.close()
    
    if not user_data:
        session.clear()
        return redirect(url_for('login'))

    # Parse History
    history = []
    for row in history_rows:
        try:
            data = json.loads(row['result_json'])
            # Extract top result for summary
            top_filiere = data['results'][0] if data.get('results') else None
            
            history.append({
                'id': row['id'],
                'date': row['date_test'],
                'profile_type': row['profile_type'],
                'top_filiere': top_filiere,
                'top_3': data.get('results', []), # No limit, display all available
                'full_data': data['results']
            })
        except:
            continue

    # Calculate Global Profile
    test_count = len(history)
    global_profile = "Profil Non Défini"
    
    if test_count > 0:
        if test_count == 1:
            global_profile = history[0]['profile_type']
        else:
            # Aggregate scores
            filiere_sums = {}
            for test in history:
                for res in test['full_data']:
                    code = res['code']
                    score = res['compatibility']
                    filiere_sums[code] = filiere_sums.get(code, 0) + score
            
            # Calculate averages
            avg_results = []
            for code, total in filiere_sums.items():
                avg = total / test_count
                avg_results.append({'code': code, 'compatibility': avg})
            
            avg_results.sort(key=lambda x: x['compatibility'], reverse=True)
            
            # Determine Global Profile Type
            if avg_results and avg_results[0]['compatibility'] > 40:
                global_profile = f"Spécialiste {avg_results[0]['code']}"
            elif avg_results and len(avg_results) > 1 and (avg_results[0]['compatibility'] - avg_results[1]['compatibility'] < 5):
                global_profile = f"Profil Hybride {avg_results[0]['code']}/{avg_results[1]['code']}"
            else:
                global_profile = "Profil Équilibré"

    return render_template('dashboard.html', 
                         user=session.get('user_name'), 
                         user_data=user_data, 
                         history=history,
                         global_profile=global_profile,
                         test_count=test_count)

# --- Admin Routes ---

@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    conn = get_db_connection()
    
    # Date Filtering
    days = request.args.get('days')
    date_filter_sql = ""
    params = []
    
    if days:
        try:
            days = int(days)
            date_filter_sql = "WHERE date_test >= datetime('now', ?)"
            params.append(f'-{days} days')
        except ValueError:
            pass # Ignore invalid days
    
    # 1. KPIs
    # Total students is usually absolute, but let's keep it absolute for now
    students_count = conn.execute("SELECT COUNT(*) FROM users WHERE role != 'admin' OR role IS NULL").fetchone()[0]
    
    # Filtered Tests Count
    query_count = f"SELECT COUNT(*) FROM results {date_filter_sql}"
    tests_count = conn.execute(query_count, params).fetchone()[0]
    
    # Average Duration (Filtered)
    query_avg = f"SELECT AVG(duration) FROM results {date_filter_sql}"
    avg_duration_row = conn.execute(query_avg, params).fetchone()
    avg_duration_sec = avg_duration_row[0] if avg_duration_row and avg_duration_row[0] is not None else 0
    avg_duration_min = round(avg_duration_sec / 60)
    avg_duration_display = f"{avg_duration_min}m"
    
    # Filiere Tendance (Most recommended #1)
    # We need to parse JSON for this usually, but let's try to extract from string if possible or fetch all
    query_results = f"SELECT result_json, date_test, profile_type FROM results {date_filter_sql}"
    results = conn.execute(query_results, params).fetchall()
    
    recom_counts = Counter()
    profile_counts = Counter()
    dates = []
    
    # Process Data
    for row in results:
        try:
            data = json.loads(row['result_json'])
            if data.get('results'):
                top = data['results'][0]['code']
                recom_counts[top] += 1
            
            p_type = row['profile_type']
            if p_type:
                # Simplify profile string for chart (take first word)
                simple_p = p_type.split(' ')[0] 
                profile_counts[simple_p] += 1
                
            if row['date_test']:
                # Parse date "YYYY-MM-DD HH:MM:SS..."
                dt = datetime.strptime(row['date_test'].split('.')[0], '%Y-%m-%d %H:%M:%S')
                dates.append(dt)
        except:
            continue
            
    conn.close()
    
    top_filiere = recom_counts.most_common(1)[0][0] if recom_counts else "N/A"
    
    # Intitulé Complet for the Card (using global FILIERE_NAMES)
    top_filiere_name = FILIERE_NAMES.get(top_filiere, top_filiere)

    # Helpers for Filiere Names (Short for Charts)
    filiere_map = {
        'GIIA': 'Génie Info',
        'GINDUS': 'Génie Industriel',
        'GTR': 'Génie Télécom',
        'GATE': 'Aéronautique',
        'GPMA': 'Génie Procédés',
        'GMSI': 'Mécatronique'
    }
    
    # Prepare Chart Data
    
    # Bar Chart (Recommandations) - Sorted Descending
    sorted_recom = sorted(recom_counts.items(), key=lambda item: item[1], reverse=True)
    bar_labels = [filiere_map.get(k, k) for k, v in sorted_recom]
    bar_values = [v for k, v in sorted_recom]
    
    # Donut Chart (Profils)
    # Normalize keys
    clean_profile_counts = Counter()
    for k, v in profile_counts.items():
        if 'Spécialiste' in k: clean_profile_counts['Spécialiste'] += v
        elif 'Hybride' in k: clean_profile_counts['Hybride'] += v
        elif 'Équilibré' in k: clean_profile_counts['Équilibré'] += v
        else: clean_profile_counts['Autre'] += v
        
    donut_labels = list(clean_profile_counts.keys())
    donut_values = list(clean_profile_counts.values())

    # Line Chart (Trend last 6 months)
    # Group dates by Month-Year
    from collections import defaultdict
    date_buckets = defaultdict(int)
    current_month = datetime.now().month
    
    # Bucketize
    for d in dates:
        key = d.strftime('%b') # Jan, Feb...
        date_buckets[key] += 1
        
    # Sort roughly (just simple for now, relying on insertion order or explicit list)
    # Ideally should generate last 6 months keys dynamically.
    trend_labels = list(date_buckets.keys())
    trend_values = list(date_buckets.values())

    return render_template('admin_analytics.html', 
                           stats={
                               'tests_count': tests_count,
                               'students_count': students_count,
                               'avg_duration': avg_duration_display
                           },
                           top_filiere_code=top_filiere,
                           top_filiere_nom=top_filiere_name,
                           chart_data={
                               'repartition_labels': bar_labels,
                               'repartition_values': bar_values,
                               'profile_labels': donut_labels,
                               'profile_values': donut_values,
                               'trend_labels': trend_labels,
                               'trend_values': trend_values
                           },
                           active_page='analytics',
                           current_days=days)

@app.route('/admin/export_analytics_csv')
@admin_required
def export_analytics_csv():
    conn = get_db_connection()
    # Fetch all results with user details
    query = """
        SELECT u.nom_complet, u.email, r.date_test, r.profile_type, r.duration
        FROM results r
        JOIN users u ON r.user_id = u.id
        ORDER BY r.date_test DESC
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    
    # Generate CSV
    def generate():
        yield 'Nom,Email,Date,Profil,Duree(s)\n'
        for row in rows:
            # Handle None values
            nom = row['nom_complet'] or 'N/A'
            email = row['email'] or 'N/A'
            date = row['date_test'] or ''
            profile = row['profile_type'] or ''
            duration = str(row['duration']) if row['duration'] else '0'
            
            # Simple CSV escaping
            yield f'"{nom}","{email}","{date}","{profile}",{duration}\n'
            
    from flask import Response
    return Response(generate(), mimetype='text/csv', 
                   headers={"Content-Disposition": "attachment;filename=analytics_export.csv"})

@app.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db_connection()
    # Get users and their test counts
    users_rows = conn.execute("SELECT * FROM users WHERE role != 'admin' OR role IS NULL").fetchall()
    
    users_list = []
    for u in users_rows:
        # Get test count for this user
        count = conn.execute("SELECT COUNT(*) FROM results WHERE user_id = ?", (u['id'],)).fetchone()[0]
        
        # Determine Trend
        trend = "Indécis"
        trend_bg = "#f1f5f9"
        trend_color = "#64748b"
        trend_icon = "far fa-question-circle"
        avatar_color = "#e2e8f0"
        
        if count > 0:
            # Get latest result for trend
            last_res = conn.execute("SELECT result_json FROM results WHERE user_id = ? ORDER BY date_test DESC LIMIT 1", (u['id'],)).fetchone()
            if last_res:
                try:
                    d = json.loads(last_res[0])
                    top_code = d['results'][0]['code']
                    trend = top_code
                    
                    # Style logic
                    if top_code == 'GIIA': 
                        trend_bg = "#e0e7ff"; trend_color = "#4338ca"; trend_icon = "fas fa-laptop-code"; avatar_color="#c7d2fe"
                    elif top_code == 'GINDUS': 
                        trend_bg = "#ffedd5"; trend_color = "#c2410c"; trend_icon = "fas fa-industry"; avatar_color="#fed7aa"
                    elif top_code == 'GATE': 
                        trend_bg = "#e0f2fe"; trend_color = "#0369a1"; trend_icon = "fas fa-plane"; avatar_color="#bae6fd"
                    elif top_code == 'GTR': 
                        trend_bg = "#ccfbf1"; trend_color = "#0f766e"; trend_icon = "fas fa-network-wired"; avatar_color="#99f6e4"
                except:
                    pass
        
        # Initials
        name_parts = u['nom_complet'].split(' ') if u['nom_complet'] else u['email'].split('@')[0].split('.')
        initials = (name_parts[0][0] + name_parts[1][0]).upper() if len(name_parts) > 1 else name_parts[0][:2].upper()
        
        users_list.append({
            'id': u['id'],
            'name': u['nom_complet'] or u['email'],
            'email': u['email'],
            'initials': initials,
            'test_count': count,
            'active': bool(u['is_active']) if 'is_active' in u.keys() else True,
            'trend_filiere': trend,
            'trend_bg': trend_bg,
            'trend_color': trend_color,
            'trend_icon': trend_icon,
            'avatar_color': avatar_color
        })
        
    conn.close()
    return render_template('admin_users.html', users_list=users_list, active_page='users')

@app.route('/api/toggle_user/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user(user_id):
    conn = get_db_connection()
    # Check current status
    user = conn.execute('SELECT is_active FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
        
    current_status = user['is_active'] if 'is_active' in user.keys() else 1
    new_status = 0 if current_status else 1
    
    conn.execute('UPDATE users SET is_active = ? WHERE id = ?', (new_status, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'new_status': new_status})

@app.route('/api/add_student', methods=['POST'])
@admin_required
def add_student():
    data = request.json
    email = data.get('email', '').strip().lower()
    code = data.get('code', '').strip()

    if not email or not code:
        return jsonify({'error': 'Tous les champs sont requis.'}), 400
    
    if not email.endswith('@uca.ac.ma'):
        return jsonify({'error': 'Email invalide. Doit se terminer par @uca.ac.ma'}), 400

    conn = get_db_connection()
    
    # Check if user exists
    existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'error': 'Cet email est déjà utilisé.'}), 400
    
    hashed_code = generate_password_hash(code)
    try:
        # Use provided name or fallback to part of email before @
        final_name = data.get('name', '').strip()
        if not final_name:
            final_name = email.split('@')[0]
        
        conn.execute('INSERT INTO users (email, access_code, nom_complet, role, is_active) VALUES (?, ?, ?, ?, ?)',
                     (email, hashed_code, final_name, 'student', 1))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        print(f"Error adding student: {e}")
        return jsonify({'error': 'Erreur base de données.'}), 500

@app.route('/api/update_password', methods=['POST'])
@admin_required
def update_password():
    data = request.json
    user_id = data.get('user_id')
    new_code = data.get('code', '').strip()
    
    if not user_id or not new_code:
        return jsonify({'error': 'Données manquantes.'}), 400
        
    conn = get_db_connection()
    
    # Optional: Prevent changing admin passwords here if you only want student management
    # For now, let's allow admins to change anyone's password (including other admins if needed)
    
    hashed_code = generate_password_hash(new_code)
    try:
        conn.execute('UPDATE users SET access_code = ? WHERE id = ?', (hashed_code, user_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        print(f"Error updating password: {e}")
        return jsonify({'error': 'Erreur base de données.'}), 500

@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    conn = get_db_connection()
    
    # Check user role - prevent deleting admins
    user = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
    if user['role'] == 'admin':
        conn.close()
        return jsonify({'error': 'Impossible de supprimer un administrateur.'}), 403

    try:
        # Delete associated results first (referential integrity usually handles this depending on schema, but safe to do manual)
        conn.execute('DELETE FROM results WHERE user_id = ?', (user_id,))
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        print(f"Error deleting user: {e}")
        return jsonify({'error': 'Erreur base de données.'}), 500


@app.route('/get_test_details/<int:result_id>')
def get_test_details(result_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM results WHERE id = ? AND user_id = ?', 
                         (result_id, session['user_id'])).fetchone()
    conn.close()
    
    if not result:
        return jsonify({'error': 'Not found'}), 404
        
    try:
        data = json.loads(result['result_json'])
        # Return top 3 filieres for the modal
        top_results = data.get('results', [])[:3]
        return jsonify({
            'date': result['date_test'],
            'results': top_results,
            'profile_type': result['profile_type']
        })
    except:
        return jsonify({'error': 'Data parse error'}), 500

# --- Questionnaire Logic (Unchanged but included for completeness) ---

DIMENSIONS = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8']
WEIGHTS = {
    'GATE':   {'D1': 0.6, 'D2': 0.3, 'D3': 0.2, 'D4': 1.2, 'D5': 0.5, 'D6': 0.3, 'D7': 0.8, 'D8': 1.5},
    'GMSI':   {'D1': 0.8, 'D2': 0.5, 'D3': 0.4, 'D4': 1.5, 'D5': 0.3, 'D6': 0.2, 'D7': 0.4, 'D8': 0.5},
    'GPMA':   {'D1': 0.4, 'D2': 0.2, 'D3': 0.1, 'D4': 0.3, 'D5': 1.2, 'D6': 0.4, 'D7': 1.5, 'D8': 0.6},
    'GTR':    {'D1': 0.5, 'D2': 0.8, 'D3': 1.5, 'D4': 0.2, 'D5': 0.1, 'D6': 0.2, 'D7': 0.4, 'D8': 0.6},
    'GINDUS': {'D1': 0.3, 'D2': 0.4, 'D3': 0.1, 'D4': 0.5, 'D5': 1.5, 'D6': 1.2, 'D7': 0.3, 'D8': 0.6},
    'GIIA':   {'D1': 1.0, 'D2': 1.5, 'D3': 0.2, 'D4': 0.3, 'D5': 0.1, 'D6': 0.2, 'D7': 0.5, 'D8': 0.4}
}
FILIERE_NAMES = {
    'GATE': 'Génie Aéronautique et Technologies de l’Espace',
    'GMSI': 'Génie Mécatronique et Systèmes Intelligents',
    'GPMA': 'Génie des Procédés et Matériaux Avancés',
    'GTR': 'Génie des Télécommunications et Réseaux',
    'GINDUS': 'Génie Industriel',
    'GIIA': 'Génie Informatique et Intelligence Artificielle'
}

@app.route('/test-orientation')
def questionnaire():
    if 'test_seed' not in session:
        session['test_seed'] = np.random.randint(1, 1000000)
    
    # Start Timer
    session['start_time'] = datetime.now().isoformat()
    
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    
    questions_list = [dict(q) for q in questions]
    import random
    random.seed(session['test_seed'])
    random.shuffle(questions_list)
    
    return render_template('questionnaire.html', questions=questions_list, user=session.get('user_name'))

@app.route('/api/submit-test', methods=['POST'])
def submit_test():
    data = request.json
    answers = data.get('answers', {})
    
    if not answers:
        return jsonify({'error': 'No answers provided'}), 400

    # Calculate Duration
    duration = 0
    start_time_str = session.get('start_time')
    if start_time_str:
        try:
            start_dt = datetime.fromisoformat(start_time_str)
            duration = (datetime.now() - start_dt).seconds
        except:
            pass
    
    # 1. Calculate Results
    responses = []
    q_response_map = {}
    for q_id, val in answers.items():
        score = 8 - int(val) 
        responses.append(score)
        q_response_map[int(q_id)] = score

    # Z-Score Normalization
    mean_user = np.mean(responses)
    std_user = np.std(responses) if np.std(responses) > 0 else 0.1
    z_scores = {q_id: (score - mean_user) / std_user for q_id, score in q_response_map.items()}

    # Dimension Scores
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()

    dim_data = {d: [] for d in DIMENSIONS}
    for q in questions:
        if q['id'] in z_scores:
            dims = q['dimensions'].split(',')
            for d in dims:
                if d.strip() in dim_data:
                    dim_data[d.strip()].append(z_scores[q['id']])
    
    dim_scores = {d: (np.mean(vals) if vals else 0) for d, vals in dim_data.items()}

    # Latent Scores & Softmax
    filiere_scores = {}
    for f_code, weights in WEIGHTS.items():
        score = sum(weights.get(d, 0) * dim_scores[d] for d in DIMENSIONS)
        filiere_scores[f_code] = score

    exp_scores = {f: np.exp(s) for f, s in filiere_scores.items()}
    sum_exp = sum(exp_scores.values())
    probabilities = {f: (exp_scores[f] / sum_exp) * 100 for f in exp_scores}

    results = []
    for f_code, prob in probabilities.items():
        results.append({
            'filiere': FILIERE_NAMES[f_code],
            'compatibility': round(float(prob)),
            'code': f_code
        })
    results.sort(key=lambda x: x['compatibility'], reverse=True)

    # Profile Type
    profile_type = "Profil Équilibré"
    if results[0]['compatibility'] > 40:
        profile_type = f"Spécialiste {results[0]['code']}"
    elif results[0]['compatibility'] - results[1]['compatibility'] < 5:
        profile_type = f"Profil Hybride {results[0]['code']}/{results[1]['code']}"

    response_data = {
        'results': results,
        'profile_type': profile_type,
        'saved': False
    }

    # 2. Logic: Save to DB or Session
    if 'user_id' in session:
        conn = get_db_connection()
        try:
            results_json = json.dumps(response_data)
            # Insert new record into results table with duration
            conn.execute('INSERT INTO results (user_id, date_test, result_json, profile_type, duration) VALUES (?, ?, ?, ?, ?)', 
                       (session['user_id'], datetime.now(), results_json, profile_type, duration))
            
            # Update user's latest stats for quick access if needed (optional, keeping for backward compatibility)
            conn.execute('UPDATE users SET last_result_json = ?, date_test = ?, profile_type = ? WHERE id = ?', 
                       (results_json, datetime.now(), profile_type, session['user_id']))
            
            conn.commit()
            response_data['saved'] = True
        except Exception as e:
            print(f"Save error: {e}")
        finally:
            conn.close()
    else:
        # Save to temporary session for later fusion
        session['temp_results'] = response_data
    
    return jsonify(response_data)

@app.route('/filiere/<code_filiere>')
def filiere_detail(code_filiere):
    conn = get_db_connection()
    filiere = conn.execute('SELECT * FROM filieres WHERE code = ?', (code_filiere,)).fetchone()
    conn.close()
    if filiere:
        return render_template('filiere_detail.html', filiere=filiere)
    return "Filière non trouvée", 404

# Chatbot Stub
from chatbot import SimpleChatbot
MISTRAL_API_KEY = "8wF32nNAoQasNzG5RzxiJpX95TlkrPBw"
bot = SimpleChatbot(api_key=MISTRAL_API_KEY)
@app.route('/api/chat', methods=['POST'])
def chat():
    return jsonify({'response': bot.get_response(request.json.get('message', ''))})

if __name__ == '__main__':
    app.run(debug=True)
