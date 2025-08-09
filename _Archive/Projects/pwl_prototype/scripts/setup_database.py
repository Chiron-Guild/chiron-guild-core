import sqlite3
from pathlib import Path

def setup_database():
    """
    Sets up the initial project database and 'events' table.
    The database file will be created in the project root directory.
    """
    # Define the project root as the parent directory of the 'scripts' folder
    project_root = Path(__file__).parent.parent
    db_path = project_root / 'pwl_ledger.db'
    
    # SQL statement to create the 'events' table
    # Using 'IF NOT EXISTS' makes the script idempotent
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        app_name TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_details TEXT
    );
    """

    try:
        # Connect to the SQLite database.
        # This will create the database file if it does not exist.
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Execute the SQL statement to create the table
            cursor.execute(create_table_sql)
            
            # Commit the changes
            conn.commit()
            
            print(f"Database successfully created/verified at: {db_path}")
            print("Table 'events' is ready.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    print("Running database setup script...")
    setup_database()