import sqlite3

def get_connection():
    conn = sqlite3.connect("newsletter_test.db")
    return conn

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    
    # Tabla de campañas
    c.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        opens_desktop INTEGER,
        opens_mobile INTEGER,
        clicks_desktop INTEGER,
        clicks_mobile INTEGER,
        daily INTEGER DEFAULT 1,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tabla de ejecuciones (reportes)
    c.execute("""
    CREATE TABLE IF NOT EXISTS executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER,
        date TEXT,
        opens_success INTEGER,
        opens_fail INTEGER,
        clicks_success INTEGER,
        clicks_fail INTEGER,
        details TEXT,
        FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
    )
    """)
    conn.commit()
    conn.close()