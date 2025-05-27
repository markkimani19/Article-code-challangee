# lib/debug.py
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import setup_database

def reset_database():
    setup_database()
    print("Database reset complete!")

if __name__ == '__main__':
    reset_database()
    print("Debug console ready!")
    print("You can now create and interact with Author, Magazine, and Article objects.")