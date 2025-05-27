# lib/models/article.py
from lib.db.connection import get_connection

class Article:
    def __init__(self, id=None, title=None, author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        if not self.title or len(self.title) == 0:
            raise ValueError("Article title cannot be empty")
        if not self.author_id:
            raise ValueError("Article must have an author")
        if not self.magazine_id:
            raise ValueError("Article must have a magazine")
            
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author_id, self.magazine_id, self.id)
                )
            conn.commit()

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
            row = cursor.fetchone()
            return cls(**dict(row)) if row else None

    @classmethod
    def find_by_title(cls, title):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
            row = cursor.fetchone()
            return cls(**dict(row)) if row else None

    @classmethod
    def find_by_author(cls, author_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
            return [cls(**dict(row)) for row in cursor.fetchall()]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
            return [cls(**dict(row)) for row in cursor.fetchall()]

    def author(self):
        from lib.models.author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)