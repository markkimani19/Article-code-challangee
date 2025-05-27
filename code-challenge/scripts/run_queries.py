from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database
from lib.controllers.author_controller import add_author_with_articles, get_author_stats

def demonstrate_queries():
    """Demonstrate various queries and operations"""
    print("=== Seeding database with sample data ===")
    seed_database()
    print()
    
    print("=== Finding all articles by an author ===")
    author = Author.find_by_name("J.K. Rowling")
    if author:
        print(f"Articles by {author.name}:")
        for article in author.articles():
            print(f"- {article.title} (in {article.magazine().name})")
    print()
    
    print("=== Finding magazines an author has contributed to ===")
    if author:
        print(f"Magazines {author.name} has written for:")
        for magazine in author.magazines():
            print(f"- {magazine.name} ({magazine.category})")
    print()
    
    print("=== Finding authors who have written for a magazine ===")
    magazine = Magazine.find_by_name("Fantasy Today")
    if magazine:
        print(f"Authors who have written for {magazine.name}:")
        for author in magazine.contributors():
            print(f"- {author.name}")
    print()
    
    print("=== Adding a new author with articles in a transaction ===")
    new_author = add_author_with_articles(
        "George R.R. Martin",
        [
            {
                'title': "The Art of Epic Fantasy",
                'magazine_name': "Fantasy Today",
                'magazine_category': "Fantasy"
            },
            {
                'title': "Writing Complex Characters",
                'magazine_name': "Literary Review",
                'magazine_category': "Literature"
            }
        ]
    )
    if new_author:
        print(f"Successfully added {new_author.name} with articles")
        stats = get_author_stats(new_author.id)
        print(f"Stats: {stats}")
    print()
    
    print("=== Finding the magazine with the most articles ===")
    top_magazine = Magazine.top_publisher()
    if top_magazine:
        print(f"Top publisher: {top_magazine.name} with {len(top_magazine.articles())} articles")

if __name__ == "__main__":
    demonstrate_queries()