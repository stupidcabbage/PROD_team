from fastapi import APIRouter

from api.dependencies import JWTAuth
from db.crud.products import get_relative_products
from schemas.products import ProductSchema
from metrics import product_counters, product_counter_mapping

router = APIRouter(prefix='/products', tags=["products"])


@router.get('/')
async def get_products(user_id: JWTAuth) -> list[ProductSchema]:
    products = await get_relative_products(user_id)
    return products


@router.post('/{product_id}')
async def post_products(user_id: JWTAuth, product_id: int):
    product_counters[product_counter_mapping[product_id]].inc(1)
