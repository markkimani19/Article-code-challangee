import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import setup_database

@pytest.fixture(autouse=True)
def setup_database_before_tests():
    """Fixture to set up the database before each test"""
    setup_database()
    # Create test data
    author = Author(name="Test Author")
    author.save()
    magazine = Magazine(name="Test Magazine", category="Test")
    magazine.save()
    Article(title="Test Article", author_id=author.id, magazine_id=magazine.id).save()

def test_article_creation():
    """Test creating and saving an article"""
    author = Author.find_by_name("Test Author")
    magazine = Magazine.find_by_name("Test Magazine")
    
    article = Article(
        title="New Test Article",
        author_id=author.id,
        magazine_id=magazine.id
    )
    article.save()
    
    assert article.id is not None
    assert article.title == "New Test Article"

def test_article_relationships():
    """Test article relationships with author and magazine"""
    article = Article.find_by_title("Test Article")
    author = article.author()
    magazine = article.magazine()
    
    assert author.name == "Test Author"
    assert magazine.name == "Test Magazine"

def test_find_by_author():
    """Test finding articles by author"""
    author = Author.find_by_name("Test Author")
    articles = Article.find_by_author(author.id)
    
    assert len(articles) >= 1
    assert articles[0].title == "Test Article"

def test_find_by_magazine():
    """Test finding articles by magazine"""
    magazine = Magazine.find_by_name("Test Magazine")
    articles = Article.find_by_magazine(magazine.id)
    
    assert len(articles) >= 1
    assert articles[0].title == "Test Article"

def test_article_validations():
    """Test article validations"""
    with pytest.raises(ValueError):
        Article(title="").save()  # Empty title
        
    with pytest.raises(ValueError):
        Article(title="No Author").save()  # Missing author
        
    with pytest.raises(ValueError):
        Article(title="No Magazine", author_id=1).save()  # Missing magazine