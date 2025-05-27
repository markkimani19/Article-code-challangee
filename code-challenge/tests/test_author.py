# tests/test_author.py
import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import setup_database

@pytest.fixture(autouse=True)
def setup_database_before_tests():
    setup_database()

def test_author_save_and_find():
    author = Author(name="John Doe")
    author.save()
    
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "John Doe"

def test_author_articles():
    author = Author(name="Jane Smith")
    author.save()
    
    magazine = Magazine(name="Tech Today", category="Technology")
    magazine.save()
    
    article = Article(title="Python Programming", author_id=author.id, magazine_id=magazine.id)
    article.save()
    
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Python Programming"

def test_author_magazines():
    author = Author(name="Bob Writer")
    author.save()
    
    magazine1 = Magazine(name="Science Weekly", category="Science")
    magazine1.save()
    
    magazine2 = Magazine(name="Tech News", category="Technology")
    magazine2.save()
    
    Article(title="AI Breakthrough", author_id=author.id, magazine_id=magazine1.id).save()
    Article(title="New Python Features", author_id=author.id, magazine_id=magazine2.id).save()
    
    magazines = author.magazines()
    assert len(magazines) == 2
    assert {m.name for m in magazines} == {"Science Weekly", "Tech News"}