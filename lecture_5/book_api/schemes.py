"""
Scheme module for data validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    """Base book scheme"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Book title"
    )
    author: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Book author name"
    )
    year: Optional[int] = Field(
        None,
        le=date.today().year,
        description="Publication year"
    )

    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty_or_whitespace(cls, v: str) -> str:
        """Strings cannot be empty or whitespace"""
        if not v or not v.strip():
            raise ValueError(
                'Field cannot be empty or whitespace'
            )
        return v.strip()


class BookCreate(BookBase):
    """Scheme to create a new book"""
    pass


class BookUpdate(BaseModel):
    """Scheme to update a book (all fields are optional)"""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="New book name"
    )
    author: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="New book author name"
    )
    year: Optional[int] = Field(
        None,
        le=date.today().year,
        description="New publication year"
    )

    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty_or_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """If string is not None, it cannot be empty or whitespace"""
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError(
                    'Field cannot be empty or whitespace'
                )
            return stripped
        return v


class BookResponse(BookBase):
    """Response scheme (includes id)"""
    id: int

    class Config:
        # Integration with SQLAlchemy models
        from_attributes = True