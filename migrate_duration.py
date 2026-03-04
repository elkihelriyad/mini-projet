import sqlite3

DB_PATH = 'ensa_orientation.db'

def migrate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('ALTER TABLE results ADD COLUMN duration INTEGER')
        print("Column 'duration' added to 'results' table.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
