# scripts/setup_db.py
from lib.db.connection import setup_database

if __name__ == '__main__':
    setup_database()
    print("Database setup complete!")