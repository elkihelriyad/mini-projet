import sqlite3

def update_users():
    conn = sqlite3.connect('ensa_orientation.db')
    cursor = conn.cursor()
    
    updates = [
        ('ENSA-8F3K', 'o.elmessaoudi@uca.ac.ma'),
        ('ENSA-4M9Q', 'r.elkihel@uca.ac.ma'),
        ('ENSA-2X7P', 'a.haloubi@uca.ac.ma')
    ]
    
    for code, email in updates:
        cursor.execute("UPDATE users SET access_code = ? WHERE email = ?", (code, email))
        
    conn.commit()
    print("Users updated successfully.")
    conn.close()

if __name__ == "__main__":
    update_users()
