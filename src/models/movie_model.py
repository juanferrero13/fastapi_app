# Creamos un Schema
import datetime
from pydantic import BaseModel, Field, field_validator


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


# Validaciones
class MovieCreate(BaseModel):
    id: int
    title: str 
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=datetime.date.today().year, ge=1950)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=15)   
    
    # Otra manera de agregar valores por defecto
    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 1,
                'title': 'My Movie',
                'overview': 'Esta pelicula trata acerca de...',
                'year': 2024,
                'rating': 5,
                'category': 'Categoría'
            }
        }
    }
    
    # Validaciones personalizadas
    @field_validator('title')
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError('Title field must have a minimun length of 5 characters')
        if len(value) > 15:
            raise ValueError('Title field must have a maximun length of 5 characters')
        return value
        
        
class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str    