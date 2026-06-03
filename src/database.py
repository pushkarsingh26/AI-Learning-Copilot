import sqlite3
import logging
from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initializes the database schema if it doesn't already exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing DB: {e}")
        raise
    finally:
        conn.close()

# Initialize upon import
init_db()
