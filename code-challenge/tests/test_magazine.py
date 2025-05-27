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
    author1 = Author(name="Author 1")
    author1.save()
    author2 = Author(name="Author 2")
    author2.save()
    magazine = Magazine(name="Test Magazine", category="Test")
    magazine.save()
    Article(title="Article 1", author_id=author1.id, magazine_id=magazine.id).save()
    Article(title="Article 2", author_id=author1.id, magazine_id=magazine.id).save()
    Article(title="Article 3", author_id=author2.id, magazine_id=magazine.id).save()

def test_magazine_creation():
    """Test creating and saving a magazine"""
    magazine = Magazine(
        name="New Test Magazine",
        category="New Category"
    )
    magazine.save()
    
    assert magazine.id is not None
    assert magazine.name == "New Test Magazine"

def test_magazine_articles():
    """Test retrieving articles for a magazine"""
    magazine = Magazine.find_by_name("Test Magazine")
    articles = magazine.articles()
    
    assert len(articles) == 3
    titles = {article.title for article in articles}
    assert "Article 1" in titles
    assert "Article 2" in titles
    assert "Article 3" in titles

def test_magazine_contributors():
    """Test retrieving contributors for a magazine"""
    magazine = Magazine.find_by_name("Test Magazine")
    contributors = magazine.contributors()
    
    assert len(contributors) == 2
    names = {contributor.name for contributor in contributors}
    assert "Author 1" in names
    assert "Author 2" in names

def test_magazine_article_titles():
    """Test retrieving article titles for a magazine"""
    magazine = Magazine.find_by_name("Test Magazine")
    titles = magazine.article_titles()
    
    assert len(titles) == 3
    assert "Article 1" in titles
    assert "Article 2" in titles
    assert "Article 3" in titles

def test_contributing_authors():
    """Test finding contributing authors with >2 articles"""
    magazine = Magazine.find_by_name("Test Magazine")
    # Author 1 has 2 articles, Author 2 has 1
    contributors = magazine.contributing_authors()
    
    assert len(contributors) == 0  # No one has >2 articles
    
    # Add one more article for Author 1
    Article(title="Article 4", author_id=1, magazine_id=magazine.id).save()
    contributors = magazine.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "Author 1"

def test_top_publisher():
    """Test finding the top publisher"""
    # Create another magazine with fewer articles
    magazine2 = Magazine(name="Other Magazine", category="Other")
    magazine2.save()
    Article(title="Other Article", author_id=1, magazine_id=magazine2.id).save()
    
    top = Magazine.top_publisher()
    assert top.name == "Test Magazine"