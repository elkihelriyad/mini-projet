import json
import os

files = [
    'update_gate.py',
    'update_giia.py',
    'update_gindus.py',
    'update_gmsi.py',
    'update_gpma.py',
    'update_gtr.py'
]

# Extract data for each file
data = {}

for filename in files:
    path = os.path.join(r'c:\Users\Riyad_Uks\Desktop\mini-projet', filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    namespace = {}
    try:
        exec(content, namespace)
    except Exception as e:
        print(f"Error executing {filename}: {e}")
        continue
    
    code = filename.replace('update_', '').replace('.py', '').upper()
    
    # Extract fields based on what's available in the namespace
    # Note: update_giia.py only has formation_data
    description = namespace.get('description', '')
    subjects = json.dumps(namespace.get('formation_data', []), ensure_ascii=False)
    career_paths = namespace.get('debouches', '')
    additional_info = namespace.get('mots_cles', '')
    
    data[code] = {
        'name': code,
        'description': description,
        'subjects': subjects,
        'career_paths': career_paths,
        'additional_info': additional_info
    }

# Generate SQL
sql_statements = []
for code, info in data.items():
    # Escape single quotes for SQL
    def escape(s):
        if not s: return 'NULL'
        if isinstance(s, str):
            return "'" + s.replace("'", "''") + "'"
        return s

    stmt = f"INSERT INTO specialties (code, name, description, subjects, career_paths, additional_info) VALUES (" \
           f"{escape(code)}, {escape(info['name'])}, {escape(info['description'])}, " \
           f"{escape(info['subjects'])}, {escape(info['career_paths'])}, {escape(info['additional_info'])});"
    sql_statements.append(stmt)

with open(r'c:\Users\Riyad_Uks\Desktop\mini-projet\generated_specialties.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_statements))
    f.write(f"\n\n-- Total specialties inserted: {len(sql_statements)}")

print(f"Success: {len(sql_statements)} specialties processed.")
