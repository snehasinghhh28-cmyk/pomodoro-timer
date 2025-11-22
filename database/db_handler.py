import sqlite3
import pandas as pd
from datetime import datetime
from config.settings import DB_NAME

class DatabaseHandler:
    def __init__(self):
        self.db_name = DB_NAME
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def _init_db(self):
        """Initialize the database table if it doesn't exist."""
        try:
            conn = self._get_connection()
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_type TEXT,
                    duration_minutes INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
        finally:
            conn.close()

    def save_session(self, session_type, duration_seconds):
        """Insert a new completed session."""
        try:
            conn = self._get_connection()
            c = conn.cursor()
            c.execute('INSERT INTO sessions (session_type, duration_minutes, timestamp) VALUES (?, ?, ?)', 
                      (session_type, int(duration_seconds/60), datetime.now()))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving session: {e}")
        finally:
            conn.close()

    def fetch_all_sessions(self):
        """Retrieve all sessions for analytics."""
        try:
            conn = self._get_connection()
            df = pd.read_sql_query("SELECT * FROM sessions", conn)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            return pd.DataFrame() # Return empty DF on failure
        finally:
            conn.close()
            
    def delete_latest_session(self):
        """Example of CRUD Delete operation."""
        try:
            conn = self._get_connection()
            c = conn.cursor()
            c.execute("DELETE FROM sessions WHERE id = (SELECT MAX(id) FROM sessions)")
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting: {e}")
        finally:
            conn.close()