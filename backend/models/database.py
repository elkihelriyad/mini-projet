import sqlite3
import os

# Now located in backend/models/database.py, so DB is at ../../database/ensa_orientation.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'ensa_orientation.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        print("Initializing database...")
        conn = get_db_connection()
        try:
            schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            
            data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'data.sql')
            if os.path.exists(data_path):
                with open(data_path, 'r', encoding='utf-8') as f:
                    conn.executescript(f.read())
        except Exception as e:
            print(f"Schema error: {e}")
        finally:
            conn.close()
        print("Database initialized.")
