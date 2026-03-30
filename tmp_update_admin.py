import sqlite3
import os

db_path = os.path.join('database', 'ensa_orientation.db')
conn = sqlite3.connect(db_path)
conn.execute("UPDATE users SET role = 'admin' WHERE email = 'ahmed@uca.ac.ma'")
conn.commit()
print("Role updated for ahmed@uca.ac.ma")
conn.close()
