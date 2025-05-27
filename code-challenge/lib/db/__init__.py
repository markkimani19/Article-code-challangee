# Makes db a package
from .connection import get_connection, setup_database

__all__ = ['get_connection', 'setup_database']