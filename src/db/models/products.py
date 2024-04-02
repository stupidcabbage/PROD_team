from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Model
from schemas.products import ProductSchema


class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    is_organisation: Mapped[bool] = mapped_column()
    image: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Product(id: {self.id!r}, name: {self.name!r})"

    def to_read_model(self) -> ProductSchema:
        return ProductSchema(id=self.id,
                             name=self.name,
                             description=self.description,
                             url=self.url,
                             image=self.image)
