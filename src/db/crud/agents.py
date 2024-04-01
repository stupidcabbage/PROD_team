from random import randint

from sqlalchemy import select

from db.db import new_session
from db.models.agents import Agent
from schemas.meetings import AgentSchema


async def get_agent_by_id(id: int) -> AgentSchema | None:
    async with new_session.begin() as session:
        stmt = select(Agent).where(Agent.id == id)
        result = await session.scalar(stmt)
        if result:
            result = result.to_read_model()
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
        Agent(name="Мустафин Карим Фаридович", description="Мобильный",
              phone_number="+79250000000", photo="https://i.imgur.com/SnwWK4H.jpeg"),
        Agent(name="Суханов Данил Валерьевич", description="Ненавижу слеши.",
              phone_number="+79851187385", photo="https://i.imgur.com/Q9ZidbP.jpeg"),
        Agent(name="Шамаев Александр Петрович", description="Специалист по возврату просроченных задолжностей.",
              phone_number="+79800553535", photo="https://i.imgur.com/7I88bCD.jpeg"),
        Agent(name="Гутче Иван Дмитриевич", description="Статусный мужчина",
              phone_number="+79800503535", photo="https://i.imgur.com/rAHxpuP.jpeg"),
        Agent(name="Мустафин Карим Фаридович", description="Мобильный",
              phone_number="+79250000000", photo="https://i.imgur.com/SnwWK4H.jpeg"),
        Agent(name="Суханов Данил Валерьевич", description="Ненавижу слеши.",
              phone_number="+79851187385", photo="https://i.imgur.com/Q9ZidbP.jpeg"),
        Agent(name="Шамаев Александр Петрович", description="Специалист по возврату просроченных задолжностей.",
              phone_number="+79800553535", photo="https://i.imgur.com/7I88bCD.jpeg"),
        Agent(name="Гутче Иван Дмитриевич", description="Статусный мужчина",
              phone_number="+79800503535", photo="https://i.imgur.com/rAHxpuP.jpeg"),
    ]
    async with new_session.begin() as session:
        existing_rows_count = await session.scalar(select(Agent).limit(1))

        if not existing_rows_count:
            for agent in agents:
                session.add(agent)

        await session.commit()
        await session.flush()
