from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .database import *

__all__ = ['User', 'Property', 'BlogPost', 'PropertyImage', 'PropertyDocument', 'PropertyView', 'UserPreference', 'Inquiry']
