# Makes models a package
from .author import Author
from .article import Article
from .magazine import Magazine

__all__ = ['Author', 'Article', 'Magazine']