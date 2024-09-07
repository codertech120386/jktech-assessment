from fastapi import FastAPI
from dotenv import load_dotenv
from icecream import ic

from routes import router

from src.utils import exception_handler_function, cors_middleware

from models import create_db_tables_from_models

app = FastAPI()

load_dotenv()
cors_middleware(app)
exception_handler_function(app)

app.include_router(router)

create_db_tables_from_models()


@app.get('/status')
def health_check():
    return "success"
