import sqlite3
import os

def get_db_path():
    return os.environ.get('APP_STORE_DB', os.path.join(os.path.dirname(__file__), 'app_store.db'))

def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force=False):
    db_path = get_db_path()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    if force or not os.path.exists(db_path):
        if os.path.exists(db_path):
            os.remove(db_path)
        with get_db_connection() as conn:
            with open(schema_path, mode='r') as f:
                conn.executescript(f.read())
        print(f"Database initialized/reset at {db_path}.")
    else:
        print(f"Database already exists at {db_path}.")

if __name__ == '__main__':
    init_db()
