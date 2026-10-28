from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from .applications import Application
from .products import Product
from .suppliers import Supplier


@dataclass
class PurchaseOrder:
    """Заказ поставщику на основании согласованной заявки."""

    id: int
    application: Application
    supplier: Supplier
    products: list[Product] = field(default_factory=list)
    status: str = "new"
    delivery_date: str | None = None
    comment: str = ""

    NEW = "new"
    SENT = "sent"
    CONFIRMED = "confirmed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        return f"Заказ №{self.id}: {self.supplier.name} — {self.status}"

    def total_price(self) -> Decimal:
        return sum((product.price for product in self.products), Decimal("0"))

    def can_cancel(self) -> bool:
        return self.status in {self.NEW, self.SENT}

    def cancel(self) -> None:
        if not self.can_cancel():
            raise ValueError(
                "Заказ нельзя отменить в текущем состоянии."
            )
        self.status = self.CANCELLED

    def is_delivery_date_valid(self) -> bool:
        if not self.delivery_date:
            return True
        return date.fromisoformat(self.delivery_date) >= date.today()

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "application_id": self.application.id,
            "supplier_id": self.supplier.id,
            "product_ids": [product.id for product in self.products],
            "status": self.status,
            "delivery_date": self.delivery_date,
            "comment": self.comment,
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        applications: list[Application],
        suppliers: list[Supplier],
        products: list[Product],
    ) -> "PurchaseOrder":
        application_map = {item.id: item for item in applications}
        supplier_map = {item.id: item for item in suppliers}
        product_map = {item.id: item for item in products}

        application = application_map.get(int(data["application_id"]))
        supplier = supplier_map.get(int(data["supplier_id"]))
        if application is None or supplier is None:
            raise ValueError(
                "Для заказа не найдена заявка или поставщик."
            )

        order = cls(
            id=int(data["id"]),
            application=application,
            supplier=supplier,
            status=str(data.get("status", cls.NEW)),
            delivery_date=data.get("delivery_date"),
            comment=str(data.get("comment", "")),
        )
        for product_id in data.get("product_ids", []):
            product = product_map.get(int(product_id))
            if product is not None:
                order.products.append(product)
        return order


def create_order(
    orders: list[PurchaseOrder],
    order: PurchaseOrder,
) -> None:
    if order.application.status != Application.APPROVED:
        raise ValueError(
            "Заказ можно создать только по согласованной заявке."
        )
    orders.append(order)
    order.application.status = Application.ORDERED


def find_order(orders: list[PurchaseOrder], order_id: int) -> PurchaseOrder | None:
    for order in orders:
        if order.id == order_id:
            return order
    return None


def show_orders(orders: list[PurchaseOrder]) -> None:
    for order in orders:
        print(f"{order} | сумма: {order.total_price():.2f} ₽")
