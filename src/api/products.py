from fastapi import APIRouter

from api.dependencies import JWTAuth
from db.crud.products import get_relative_products
from schemas.products import ProductSchema
import prometheus_client

router = APIRouter(prefix='/products', tags=["products"])


comapny_card_count = prometheus_client.Counter(
    'buisness_card', 'Clicked Buisness Card for organizations'
)
individual_card_count = prometheus_client.Counter(
    'individual_card_count', 'Clicked Buisness Card for organizations'
)
comapny_card_count = prometheus_client.Counter(
    'buisness_card', 'Clicked Buisness Card for organizations'
)
comapny_card_count = prometheus_client.Counter(
    'buisness_card', 'Clicked Buisness Card for organizations'
)
# {"name": "Бизнес карта для компаний", "description": "Обслуживание — 0 ₽. Привязана к расчетному счету. Для бизнес-расходов и личных трат", "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Бизнес карта для ИП", "description": "Обслуживание — 0 ₽. Привязана к расчетному счету. Для бизнес-расходов и личных трат", "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Онлайн банк для малого бизнеса", "description": "Без очередей и ожидания на линии. Удобное приложение и личный кабинет. Поддержка 24/7 в чате", "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Онлайн банк для малого бизнеса", "description": "Без очередей и ожидания на линии. Удобное приложение и личный кабинет. Поддержка 24/7 в чате", "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Кредит на развитие бизнеса", "description": "Получите деньги на развитие бизнеса: до 10 млн рублей. Вы можете узнать сумму без открытия счета.", "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Кредит на развитие бизнеса", "description": "Получите деньги на развитие бизнеса: до 10 млн рублей. Вы можете узнать сумму без открытия счета.", "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Бесплатная онлайн бухгалтерия для ИП", "description": "Легко сдавать отчетность и платить налоги самостоятельно.", "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Удобный прием платежей для вашего бизнеса", "description": "Принимайте платежи от клиентов на сайте, в приложении, соцсетях, месседжерах, по e-mail и СМС", "is_organisation": False, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
# {"name": "Удобный прием платежей для вашего бизнеса", "description": "Принимайте платежи от клиентов на сайте, в приложении, соцсетях, месседжерах, по e-mail и СМС", "is_organisation": True, "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
#


@router.get('/')
async def get_products(user_id: JWTAuth) -> list[ProductSchema]:
    products = await get_relative_products(user_id)
    return products


@router.post('/{product_id}')
async def post_products(user_id: JWTAuth):
