from typing import List
from fastapi import Path, Query, APIRouter
from fastapi.responses import JSONResponse
from src.models.movie_model import Movie, MovieCreate, MovieUpdate

movies: List[Movie] = []

movie_router = APIRouter()

@movie_router.get("/", tags=['Movies'])
async def get_movies() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)


# Utilizando parametros de ruta
@movie_router.get("/{id}", tags=['Movies'])
async def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(content=movie.model_dump()) 
        
    return JSONResponse(content={})


# Utilizando parametros query (se utiliza el par clave-valor seguido de '?' => '/?category=comedia') y se añaden dentro de la función, no en la ruta, a diferencia de los 'parametros de ruta'
@movie_router.get("/by_category", tags=['Movies'])
async def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(content=movie.model_dump()) 
        
    return JSONResponse(content={})


# Utilizando el método POST
@movie_router.post("/", tags=['Movies'])
async def create_movie(movie: MovieCreate) -> List[Movie]:
    # Utilizamos model_dump para convertir lo que nos llega a un dict y poder insertarlo en la lista de peliculas
    movies.append(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)
    # RedirectResponse('/movies', status_code=303) // Ejemplo de redireccion dentro de nuestra web


# Utilizando el método PUT
@movie_router.put("/{id}", tags=['Movies'])
async def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)     


# Utilizando el método DELETE
@movie_router.delete("/{id}", tags=['Movies'])
async def delete_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)   