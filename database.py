import sqlite3
import json
from datetime import datetime

DB_NAME = "newsletter_test.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    
    # Tabla de campañas
    c.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        newsletter_url TEXT,
        opens_desktop INTEGER,
        opens_mobile INTEGER,
        clicks_desktop INTEGER,
        clicks_mobile INTEGER,
        daily INTEGER DEFAULT 1,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Migración automática si la tabla ya existía sin la columna newsletter_url
    c.execute("PRAGMA table_info(campaigns)")
    columns = [col[1] for col in c.fetchall()]
    if "newsletter_url" not in columns:
        c.execute("ALTER TABLE campaigns ADD COLUMN newsletter_url TEXT")

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

def save_execution(campaign_id, results):
    """Guarda el resultado de una prueba en la tabla executions."""
    conn = get_connection()
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details_str = json.dumps(results.get("details", []), ensure_ascii=False)
    
    c.execute("""
        INSERT INTO executions (
            campaign_id, date, opens_success, opens_fail, 
            clicks_success, clicks_fail, details
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        campaign_id,
        date_str,
        results.get("opens_success", 0),
        results.get("opens_fail", 0),
        results.get("clicks_success", 0),
        results.get("clicks_fail", 0),
        details_str
    ))
    conn.commit()
    conn.close()