from sqlalchemy.orm import Mapped, mapped_column

from db.db import Model
from schemas.meetings import AgentSchema


class Agent(Model):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column(default="HelloWorld")

    def __repr__(self) -> str:
        return f"Agent(id: {self.id!r}, name: {self.name!r})"

    def to_read_model(self) -> AgentSchema:
        return AgentSchema(
            id=self.id,
            name=self.name,
            description=self.description,
            phone_number=self.phone_number,
            photo=self.photo
        )
