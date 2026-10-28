from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from .products import Product


@dataclass
class Application:
    """Заявка на закупку товаров."""

    id: int
    requester: str
    comment: str = ""
    status: str = "created"
    products: list[Product] = field(default_factory=list)

    CREATED = "created"
    APPROVED = "approved"
    ORDERED = "ordered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        return f"Заявка №{self.id}: {self.requester} — {self.status}"

    def add_product(self, product: Product) -> None:
        if not product.is_active:
            raise ValueError("Нельзя добавить неактивный товар в заявку.")
        self.products.append(product)

    def total_price(self) -> Decimal:
        return sum((product.price for product in self.products), Decimal("0"))

    def can_approve(self) -> bool:
        return self.status == self.CREATED and bool(self.products)

    def approve(self) -> None:
        if not self.can_approve():
            raise ValueError(
                "Заявку нельзя согласовать в текущем состоянии."
            )
        self.status = self.APPROVED

    def can_cancel(self) -> bool:
        return self.status in {self.CREATED, self.APPROVED}

    def cancel(self) -> None:
        if not self.can_cancel():
            raise ValueError(
                "Заявку нельзя отменить в текущем состоянии."
            )
        self.status = self.CANCELLED

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "requester": self.requester,
            "comment": self.comment,
            "status": self.status,
            "product_ids": [product.id for product in self.products],
        }

    @classmethod
    def from_data(cls, data: dict, products: list[Product]) -> "Application":
        product_map = {product.id: product for product in products}
        application = cls(
            id=int(data["id"]),
            requester=str(data["requester"]),
            comment=str(data.get("comment", "")),
            status=str(data.get("status", cls.CREATED)),
        )
        for product_id in data.get("product_ids", []):
            product = product_map.get(int(product_id))
            if product is not None:
                application.products.append(product)
        return application


def add_application(
    applications: list[Application],
    application: Application,
) -> None:
    applications.append(application)


def find_application(
    applications: list[Application],
    application_id: int,
) -> Application | None:
    for application in applications:
        if application.id == application_id:
            return application
    return None


def show_applications(applications: list[Application]) -> None:
    for application in applications:
        print(f"{application} | сумма: {application.total_price():.2f} ₽")
