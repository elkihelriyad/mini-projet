from flask import Blueprint, render_template, request, Response
from backend.models.database import get_db_connection
from backend.utils.helpers import admin_required
from backend.utils.config import FILIERE_NAMES
from datetime import datetime
from collections import Counter
import json

admin_bp = Blueprint('admin_routes', __name__)

@admin_bp.route('/admin/analytics')
@admin_required
def admin_analytics():
    conn = get_db_connection()
    days = request.args.get('days')
    date_filter_sql = ""
    params = []
    
    if days:
        try:
            days = int(days)
            date_filter_sql = "WHERE date_test >= datetime('now', ?)"
            params.append(f'-{days} days')
        except ValueError:
            pass 
    
    students_count = conn.execute("SELECT COUNT(*) FROM users WHERE role != 'admin' OR role IS NULL").fetchone()[0]
    
    query_count = f"SELECT COUNT(*) FROM results {date_filter_sql}"
    tests_count = conn.execute(query_count, params).fetchone()[0]
    
    query_avg = f"SELECT AVG(duration) FROM results {date_filter_sql}"
    avg_duration_row = conn.execute(query_avg, params).fetchone()
    avg_duration_sec = avg_duration_row[0] if avg_duration_row and avg_duration_row[0] is not None else 0
    avg_duration_min = round(avg_duration_sec / 60)
    avg_duration_display = f"{avg_duration_min}m"
    
    query_results = f"SELECT result_json, date_test, profile_type FROM results {date_filter_sql}"
    results = conn.execute(query_results, params).fetchall()
    
    recom_counts = Counter()
    profile_counts = Counter()
    dates = []
    
    for row in results:
        try:
            data = json.loads(row['result_json'])
            if data.get('results'):
                top = data['results'][0]['code']
                recom_counts[top] += 1
            
            p_type = row['profile_type']
            if p_type:
                simple_p = p_type.split(' ')[0] 
                profile_counts[simple_p] += 1
                
            if row['date_test']:
                dt = datetime.strptime(row['date_test'].split('.')[0], '%Y-%m-%d %H:%M:%S')
                dates.append(dt)
        except:
            continue
            
    conn.close()
    
    top_filiere = recom_counts.most_common(1)[0][0] if recom_counts else "N/A"
    top_filiere_name = FILIERE_NAMES.get(top_filiere, top_filiere)

    filiere_map = {
        'GIIA': 'Génie Info',
        'GINDUS': 'Génie Industriel',
        'GTR': 'Génie Télécom',
        'GATE': 'Aéronautique',
        'GPMA': 'Génie Procédés',
        'GMSI': 'Mécatronique'
    }
    
    sorted_recom = sorted(recom_counts.items(), key=lambda item: item[1], reverse=True)
    bar_labels = [filiere_map.get(k, k) for k, v in sorted_recom]
    bar_values = [v for k, v in sorted_recom]
    
    clean_profile_counts = Counter()
    for k, v in profile_counts.items():
        if 'Spécialiste' in k: clean_profile_counts['Spécialiste'] += v
        elif 'Hybride' in k: clean_profile_counts['Hybride'] += v
        elif 'Équilibré' in k: clean_profile_counts['Équilibré'] += v
        else: clean_profile_counts['Autre'] += v
        
    donut_labels = list(clean_profile_counts.keys())
    donut_values = list(clean_profile_counts.values())

    date_buckets = {}
    for d in dates:
        key = d.strftime('%b') 
        date_buckets[key] = date_buckets.get(key, 0) + 1
        
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

@admin_bp.route('/admin/export_analytics_csv')
@admin_required
def export_analytics_csv():
    conn = get_db_connection()
    query = """
        SELECT u.nom_complet, u.email, r.date_test, r.profile_type, r.duration
        FROM results r
        JOIN users u ON r.user_id = u.id
        ORDER BY r.date_test DESC
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    
    def generate():
        yield 'Nom,Email,Date,Profil,Duree(s)\n'
        for row in rows:
            nom = row['nom_complet'] or 'N/A'
            email = row['email'] or 'N/A'
            date = row['date_test'] or ''
            profile = row['profile_type'] or ''
            duration = str(row['duration']) if row['duration'] else '0'
            yield f'"{nom}","{email}","{date}","{profile}",{duration}\n'
            
    return Response(generate(), mimetype='text/csv', 
                   headers={"Content-Disposition": "attachment;filename=analytics_export.csv"})

@admin_bp.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db_connection()
    users_rows = conn.execute("SELECT * FROM users WHERE role != 'admin' OR role IS NULL").fetchall()
    
    users_list = []
    for u in users_rows:
        count = conn.execute("SELECT COUNT(*) FROM results WHERE user_id = ?", (u['id'],)).fetchone()[0]
        
        trend = "Indécis"
        trend_bg = "#f1f5f9"
        trend_color = "#64748b"
        trend_icon = "far fa-question-circle"
        avatar_color = "#e2e8f0"
        
        if count > 0:
            last_res = conn.execute("SELECT result_json FROM results WHERE user_id = ? ORDER BY date_test DESC LIMIT 1", (u['id'],)).fetchone()
            if last_res:
                try:
                    d = json.loads(last_res[0])
                    top_code = d['results'][0]['code']
                    trend = top_code
                    
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
