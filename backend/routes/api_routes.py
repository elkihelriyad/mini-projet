from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from backend.models.database import get_db_connection
from backend.utils.helpers import admin_required
from backend.utils.config import DIMENSIONS, WEIGHTS, FILIERE_NAMES
try:
    from backend.services.ai_service import get_mistral_response
except ImportError:
    get_mistral_response = None

from datetime import datetime
import json
import numpy as np

api_bp = Blueprint('api_routes', __name__)

@api_bp.route('/api/toggle_user/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user(user_id):
    conn = get_db_connection()
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

@api_bp.route('/api/add_student', methods=['POST'])
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
    existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'error': 'Cet email est déjà utilisé.'}), 400
    
    hashed_code = generate_password_hash(code)
    try:
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
        return jsonify({'error': 'Erreur base de données.'}), 500

@api_bp.route('/api/update_password', methods=['POST'])
@admin_required
def update_password():
    data = request.json
    user_id = data.get('user_id')
    new_code = data.get('code', '').strip()
    
    if not user_id or not new_code:
        return jsonify({'error': 'Données manquantes.'}), 400
        
    conn = get_db_connection()
    hashed_code = generate_password_hash(new_code)
    try:
        conn.execute('UPDATE users SET access_code = ? WHERE id = ?', (hashed_code, user_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': 'Erreur base de données.'}), 500

@api_bp.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
    if user['role'] == 'admin':
        conn.close()
        return jsonify({'error': 'Impossible de supprimer un administrateur.'}), 403

    try:
        conn.execute('DELETE FROM results WHERE user_id = ?', (user_id,))
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'error': 'Erreur base de données.'}), 500

@api_bp.route('/get_test_details/<int:result_id>')
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
        top_results = data.get('results', [])[:3]
        return jsonify({
            'date': result['date_test'],
            'results': top_results,
            'profile_type': result['profile_type']
        })
    except:
        return jsonify({'error': 'Data parse error'}), 500

@api_bp.route('/api/submit-test', methods=['POST'])
def submit_test():
    data = request.json
    answers = data.get('answers', {})
    
    if not answers:
        return jsonify({'error': 'No answers provided'}), 400

    duration = 0
    start_time_str = session.get('start_time')
    if start_time_str:
        try:
            start_dt = datetime.fromisoformat(start_time_str)
            duration = (datetime.now() - start_dt).seconds
        except:
            pass
    
    responses = []
    q_response_map = {}
    for q_id, val in answers.items():
        score = 8 - int(val) 
        responses.append(score)
        q_response_map[int(q_id)] = score

    mean_user = np.mean(responses)
    std_user = np.std(responses) if np.std(responses) > 0 else 0.1
    z_scores = {q_id: (score - mean_user) / std_user for q_id, score in q_response_map.items()}

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

    profile_type = "Profil Équilibré"
    if results and int(results[0]['compatibility']) > 40:
        profile_type = f"Spécialiste {results[0]['code']}"
    elif len(results) > 1 and int(results[0]['compatibility']) - int(results[1]['compatibility']) < 5:
        profile_type = f"Profil Hybride {results[0]['code']}/{results[1]['code']}"

    response_data = {
        'results': results,
        'profile_type': profile_type,
        'saved': False
    }

    if 'user_id' in session:
        conn = get_db_connection()
        try:
            results_json = json.dumps(response_data)
            conn.execute('INSERT INTO results (user_id, date_test, result_json, profile_type, duration) VALUES (?, ?, ?, ?, ?)', 
                       (session['user_id'], datetime.now(), results_json, profile_type, duration))
            conn.execute('UPDATE users SET last_result_json = ?, date_test = ?, profile_type = ? WHERE id = ?', 
                       (results_json, datetime.now(), profile_type, session['user_id']))
            conn.commit()
            response_data['saved'] = True
        except Exception as e:
            print(f"Save error: {e}")
        finally:
            conn.close()
    else:
        session['temp_results'] = response_data
    
    return jsonify(response_data)

MISTRAL_API_KEY = "8wF32nNAoQasNzG5RzxiJpX95TlkrPBw"

@api_bp.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    if not user_msg:
        return jsonify({'response': 'Comment puis-je vous aider ?'})
        
    if get_mistral_response:
        reply = get_mistral_response(user_msg, MISTRAL_API_KEY)
    else:
        reply = "Le service d'assistance AI est indisponible pour le moment."
    return jsonify({'response': reply})

@api_bp.route('/api/specialties', strict_slashes=False)
def list_specialties():
    conn = get_db_connection()
    specialties = conn.execute('SELECT code, name, description FROM specialties').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in specialties])

@api_bp.route('/api/specialties/<code_filiere>', strict_slashes=False)
def get_specialty(code_filiere):
    conn = get_db_connection()
    filiere = conn.execute('SELECT * FROM specialties WHERE code = ?', (code_filiere,)).fetchone()
    conn.close()
    if filiere:
        data = dict(filiere)
        # Parse additional_info if it's a JSON string
        if data.get('additional_info'):
            try:
                data['additional_info'] = json.loads(data['additional_info'])
            except:
                pass
        return jsonify(data)
    return jsonify({'error': 'Filière non trouvée'}), 404
