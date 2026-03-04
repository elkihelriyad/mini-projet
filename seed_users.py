import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'ensa_orientation.db'

def seed_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop table if exists to ensure clean slate or alter it? 
    # For this mini-project, let's just make sure the users table has what we need.
    # We will assume the schema exists, but we might need to update passwords to hashes.
    
    # 1. Check if we need to migrate existing plain text codes? 
    # Actually, the requirement says "accounts pre-existing". 
    # Let's just update the specific test accounts with hashed passwords.

    users = [
        ('o.elmessaoudi@uca.ac.ma', 'ENSA-8F3K'),
        ('r.elkihel@uca.ac.ma', 'ENSA-4M9Q'),
        ('a.haloubi@uca.ac.ma', 'ENSA-2X7P')
    ]

    print("Seeding/Updating users with hashed access codes...")

    for email, code in users:
        hashed_code = generate_password_hash(code)
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Update existing user
            cursor.execute("UPDATE users SET access_code = ? WHERE email = ?", (hashed_code, email))
            print(f"Updated {email}")
        else:
            # Insert new user (assuming other fields might be null or default)
            cursor.execute("INSERT INTO users (email, access_code, nom_complet) VALUES (?, ?, ?)", 
                           (email, hashed_code, email.split('@')[0]))
            print(f"Created {email}")

    conn.commit()
    conn.close()
    print("Seeding complete.")

if __name__ == "__main__":
    seed_users()
