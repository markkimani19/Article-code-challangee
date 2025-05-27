from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    # Clear existing data
    with get_connection() as conn:
        conn.execute("DELETE FROM articles")
        conn.execute("DELETE FROM authors")
        conn.execute("DELETE FROM magazines")
        conn.commit()

    # Create sample data
    author1 = Author(name="John Doe")
    author1.save()

    author2 = Author(name="Jane Smith")
    author2.save()

    magazine1 = Magazine(name="Tech Today", category="Technology")
    magazine1.save()

    magazine2 = Magazine(name="Science Weekly", category="Science")
    magazine2.save()

    Article(title="Python Programming", author_id=author1.id, magazine_id=magazine1.id).save()
    Article(title="AI Breakthrough", author_id=author1.id, magazine_id=magazine2.id).save()
    Article(title="New Python Features", author_id=author2.id, magazine_id=magazine1.id).save()

if __name__ == "__main__":
    from lib.db.connection import setup_database
    setup_database()
    seed_database()
    print("Database seeded with sample data!")