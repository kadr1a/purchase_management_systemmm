from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    """Товар, доступный для закупки."""

    id: int
    name: str
    unit: str
    price: Decimal
    is_active: bool = True

    def __str__(self) -> str:
        status = "активен" if self.is_active else "неактивен"
        return (
            f"Товар №{self.id}: {self.name} — "
            f"{self.price:.2f} ₽/{self.unit} ({status})"
        )

    def total_cost(self, quantity: int) -> Decimal:
        """Рассчитать стоимость указанного количества товара."""
        if quantity <= 0:
            raise ValueError("Количество товара должно быть положительным.")
        return self.price * quantity

    @classmethod
    def from_data(cls, data: dict) -> "Product":
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            unit=str(data["unit"]),
            price=Decimal(str(data["price"])),
            is_active=bool(data.get("is_active", True)),
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "price": str(self.price),
            "is_active": self.is_active,
        }


def add_product(products: list[Product], product: Product) -> None:
    products.append(product)


def find_product(products: list[Product], product_id: int) -> Product | None:
    for product in products:
        if product.id == product_id:
            return product
    return None


def show_products(products: list[Product]) -> None:
    for product in products:
        print(product)
