from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.utils import verify_token

from .schema import CreateLlamaSummarySchema
from .controller import generate_summary_using_llama3

auth_scheme = HTTPBearer()

home_router = APIRouter(
    prefix="",
    tags=["Home"],
    responses={404: {"description": "Home routes Not found"}},
)


@home_router.post('/generate-summary')
async def generate_summary(create_llama_summary_schema: CreateLlamaSummarySchema, token=Depends(auth_scheme),
                           user_data=Depends(verify_token)):
    return generate_summary_using_llama3(content=create_llama_summary_schema.content)
