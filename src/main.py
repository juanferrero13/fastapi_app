from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response, JSONResponse
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.add_middleware(HTTPErrorHandler)

# Configurando el motor de plantillas jinja2
static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

app.mount('/static', StaticFiles(directory=static_path), 'static')
templates = Jinja2Templates(directory=templates_path)


# @app.middleware('http')
# async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
#     print('Middleware is running')
#     return await call_next(request)


# Utilizando el método GET
@app.get("/", tags=['Home'])
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'message': 'Welcome to FastAPI'})


# Generando dependencias por medio de una función
# def common_params(start_date: str, end_date: str):
#     return {"start_date": start_date, "end_date": end_date}

# CommonDep = Annotated[dict, Depends(common_params)]

# Generando dependencias por medio de una clase
class CommonDep:
    def __init__(self, start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date

@app.get('/users')
async def get_users(commons: CommonDep = Depends()):
    return f"Users created between {commons.start_date} and {commons.end_date}"

@app.get('/customers')
async def get_customers(commons: CommonDep = Depends()):
    return f"Customers created between {commons.start_date} and {commons.end_date}"


app.include_router(prefix='/movies',  router=movie_router)



