
from typing import Annotated

from fastapi import APIRouter, Body

from api.dependencies import JWTAuth
from db.crud.products import get_relative_products
from schemas.products import ProductSchema

router = APIRouter(prefix='/products', tags=["products"])


@router.get('/')
async def get_products(user_id: JWTAuth) -> list[ProductSchema]:
    products = await get_relative_products(user_id)
    return products