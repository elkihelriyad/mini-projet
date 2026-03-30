import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'ensa_orientation.db'

def migrate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Add role column if not exists
    try:
        c.execute('ALTER TABLE users ADD COLUMN role TEXT DEFAULT "student"')
        print("Column 'role' added.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist: {e}")

    # 2. Add or Update Admin User
    admin_email = 'admin@ensas.uca.ma'
    admin_code = generate_password_hash('ADMIN2026')
    
    c.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
    if c.fetchone():
        c.execute('UPDATE users SET role = "admin", access_code = ? WHERE email = ?', (admin_code, admin_email))
        print("Admin user updated.")
    else:
        c.execute('INSERT INTO users (email, access_code, nom_complet, role) VALUES (?, ?, ?, ?)',
                  (admin_email, admin_code, 'Admin Open', 'admin'))
        print("Admin user created.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
