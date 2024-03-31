from random import randint
from sqlalchemy import select
from schemas.meetings import AgentSchema
from db.db import new_session
from db.models.agents import Agent


async def get_agent_by_id(id: int) -> AgentSchema | None:
    async with new_session.begin() as session:
        stmt = select(Agent).where(Agent.id == id)
        result = await session.scalar(stmt)
        if result:
            result = result.to_read_schema()
        return result


async def get_best_agent() -> AgentSchema | None:
    async with new_session.begin() as session:
        stmt = select(Agent).where(Agent.id == randint(0, 7))
        model = await session.scalar(stmt)
        if model:
            model = model.to_read_model()
        return model


async def fill_defaults() -> None:
    agents = [
        Agent(name="Дмитрий Евгеньевич", description="Пунктуальный",
              phone_number="+79250000000", photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-bVGuJki3XUfvsL7dlKbuI18B7Wk6QdFbteXjf3W8vA&s"),
        Agent(name="Иван Петрович", description="Добрый мужчина в расвете сил",
              phone_number="+79851187385", photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfKeo1e6nU1DKJLPazvI_Ktezx16osGylBJ79O5UC-Aw&s"),
        Agent(name="Виолетта Андреевна", description="Добрая леди",
              phone_number="+79800553535", photo="https://st3.depositphotos.com/3811801/18613/i/450/depositphotos_186133820-stock-photo-bearded-man-on-a-gray.jpg"),
        Agent(name="Петр Александрович", description="Статусный мужчина",
              phone_number="+79800503535", photo="https://st3.depositphotos.com/3811801/18613/i/450/depositphotos_186133820-stock-photo-bearded-man-on-a-gray.jpg"),
        Agent(name="Александр Анатольевич", description="Строгий человек",
              phone_number="+79250001800", photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-bVGuJki3XUfvsL7dlKbuI18B7Wk6QdFbteXjf3W8vA&s"),
        Agent(name="Василиса Александровна", description="Никогда не опаздывает",
              phone_number="+79752187185", photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfKeo1e6nU1DKJLPazvI_Ktezx16osGylBJ79O5UC-Aw&s"),
        Agent(name="София Андреевна", description="Всего вовремя!",
              phone_number="+79890573535", photo="https://st3.depositphotos.com/3811801/18613/i/450/depositphotos_186133820-stock-photo-bearded-man-on-a-gray.jpg"),
        Agent(name="Дмитрий Витальевич", description="Крайне пунктуален",
              phone_number="+79899503535", photo="https://st3.depositphotos.com/3811801/18613/i/450/depositphotos_186133820-stock-photo-bearded-man-on-a-gray.jpg"),

    ]
    async with new_session.begin() as session:
        existing_rows_count = await session.scalar(select(Agent).limit(1))

        if not existing_rows_count:
            for agent in agents:
                session.add(agent)

        await session.commit()
        await session.flush()
