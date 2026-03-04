import sqlite3
import json

conn = sqlite3.connect('ensa_orientation.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
row = cursor.execute("SELECT formation_json FROM filieres WHERE code = 'GIIA'").fetchone()

if row:
    print(json.dumps(json.loads(row['formation_json']), indent=2, ensure_ascii=False))
else:
    print("GIIA not found")

conn.close()
