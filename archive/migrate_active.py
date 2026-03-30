import sqlite3

DB_PATH = 'ensa_orientation.db'

def migrate_users_active():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Add is_active column, default to 1 (True/Active)
        c.execute('ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1')
        print("Column 'is_active' added to 'users' table.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate_users_active()
