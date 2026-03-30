from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from backend.models.database import get_db_connection
import json
from datetime import datetime
import numpy as np

main_bp = Blueprint('main_routes', __name__)

@main_bp.route('/')
def index():
    session.pop('test_seed', None)
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        code = request.form.get('password', '').strip()
        temp_results = session.get('temp_results')

        if not email.endswith('@uca.ac.ma') and not email.endswith('ensas.uca.ma'):
            return render_template('login.html', error="Email académique requis (@uca.ac.ma)", next=next_page)
            
        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        except:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        valid_user = False
        if user:
            try:
                if check_password_hash(user['access_code'], code):
                    valid_user = True
            except:
                if user['access_code'] == code:
                    valid_user = True
        
        if valid_user:
            is_active = user['is_active'] if 'is_active' in user.keys() else 1
            if is_active == 0:
                flash('Ce compte a été désactivé par l\'administrateur.', 'error')
                conn.close()
                return render_template('login.html')

            session.clear() 
            session['user_id'] = user['id']
            session['user_name'] = user['nom_complet'] if user['nom_complet'] else email.split('@')[0]
            session['role'] = user['role'] if 'role' in user.keys() and user['role'] else 'student'
            session.permanent = True
            
            if session['role'] == 'admin':
                conn.close()
                return redirect(url_for('admin_routes.admin_analytics'))
            
            fusion_occurred = False
            if temp_results:
                try:
                    results_json = json.dumps(temp_results)
                    conn.execute('INSERT INTO results (user_id, date_test, result_json, profile_type) VALUES (?, ?, ?, ?)', 
                               (user['id'], datetime.now(), results_json, temp_results.get('profile_type')))
                    conn.execute('UPDATE users SET last_result_json = ?, date_test = ?, profile_type = ? WHERE id = ?', 
                               (results_json, datetime.now(), temp_results.get('profile_type'), user['id']))
                    conn.commit()
                    fusion_occurred = True
                except Exception as e:
                    print(f"Merge Error: {e}")
            
            conn.close()
            target = request.args.get('next')
            if not target and fusion_occurred:
                target = url_for('main_routes.dashboard')
            
            return redirect(target or url_for('main_routes.index'))
            
        else:
            conn.close()
            return render_template('login.html', error="Adresse e-mail ou code incorrect. Veuillez réessayer.", next=next_page)

    return render_template('login.html', next=next_page)

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_routes.index'))

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main_routes.login'))
        
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    history_rows = conn.execute('SELECT * FROM results WHERE user_id = ? ORDER BY date_test DESC', (session['user_id'],)).fetchall()
    conn.close()
    
    if not user_data:
        session.clear()
        return redirect(url_for('main_routes.login'))

    history = []
    for row in history_rows:
        try:
            data = json.loads(row['result_json'])
            top_filiere = data['results'][0] if data.get('results') else None
            
            history.append({
                'id': row['id'],
                'date': row['date_test'],
                'profile_type': row['profile_type'],
                'top_filiere': top_filiere,
                'top_3': data.get('results', []), 
                'full_data': data['results']
            })
        except:
            continue

    test_count = len(history)
    global_profile = "Profil Non Défini"
    
    if test_count > 0:
        if test_count == 1:
            global_profile = history[0]['profile_type']
        else:
            filiere_sums = {}
            for test in history:
                full_data = test.get('full_data')
                if not full_data:
                    continue
                for res in full_data:
                    code = res['code']
                    score = res['compatibility']
                    filiere_sums[code] = filiere_sums.get(code, 0) + score
            
            avg_results = []
            for code, total in filiere_sums.items():
                avg = total / test_count
                avg_results.append({'code': code, 'compatibility': avg})
            
            avg_results.sort(key=lambda x: x['compatibility'], reverse=True)
            
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

@main_bp.route('/filiere/<code_filiere>')
def filiere_detail(code_filiere):
    conn = get_db_connection()
    # Changed from filieres to specialties
    filiere = conn.execute('SELECT * FROM specialties WHERE code = ?', (code_filiere,)).fetchone()
    conn.close()
    if filiere:
        # Pass fields as they were requested by HTML. 
        # HTML uses filiere.nom, filiere.description, filiere.debouches, filiere.mots_cles, filiere.formation_json
        # Since I used the english schema (name, description, career_paths, subjects, additional_info), 
        # I map them to a dict with the old names so the template works exactly as before.
        mapped_filiere = {
            'code': filiere['code'],
            'nom': filiere['name'],
            'description': filiere['description'],
            'debouches': filiere['career_paths'],
            'mots_cles': filiere['subjects'],
            'formation_json': filiere['additional_info']
        }
        return render_template('filiere_detail.html', filiere=mapped_filiere)
    return "Filière non trouvée", 404

@main_bp.route('/test-orientation')
def questionnaire():
    if 'test_seed' not in session:
        session['test_seed'] = np.random.randint(1, 1000000)
    
    session['start_time'] = datetime.now().isoformat()
    
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    
    questions_list = [dict(q) for q in questions]
    import random
    random.seed(session['test_seed'])
    random.shuffle(questions_list)
    
    return render_template('questionnaire.html', questions=questions_list, user=session.get('user_name'))
