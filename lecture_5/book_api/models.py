"""
Data models module.
Contains SQLAlchemy models of data representation.
"""


from sqlalchemy import Column, Integer, String
from database import Base


class Book(Base):
    """SQLAlchemy book model."""
    __tablename__ = "books"

    # Creating columns and indices for 'id' and 'title'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)  # optional
    
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}')"