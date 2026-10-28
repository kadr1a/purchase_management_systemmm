from __future__ import annotations

import json
from pathlib import Path

from models import Application, Product, PurchaseOrder, Supplier

DATA_DIR = Path(__file__).resolve().parent / "data"


def _load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_products() -> list[Product]:
    return [Product.from_data(item) for item in _load(DATA_DIR / "products.json")]


def load_suppliers() -> list[Supplier]:
    return [Supplier.from_data(item) for item in _load(DATA_DIR / "suppliers.json")]


def load_applications(products: list[Product]) -> list[Application]:
    return [
        Application.from_data(item, products)
        for item in _load(DATA_DIR / "applications.json")
    ]


def load_orders(
    applications: list[Application],
    suppliers: list[Supplier],
    products: list[Product],
) -> list[PurchaseOrder]:
    return [
        PurchaseOrder.from_data(item, applications, suppliers, products)
        for item in _load(DATA_DIR / "orders.json")
    ]


def save_products(products: list[Product]) -> None:
    _save(DATA_DIR / "products.json", [product.to_data() for product in products])


def save_suppliers(suppliers: list[Supplier]) -> None:
    _save(DATA_DIR / "suppliers.json", [supplier.to_data() for supplier in suppliers])


def save_applications(applications: list[Application]) -> None:
    _save(
        DATA_DIR / "applications.json",
        [application.to_data() for application in applications],
    )


def save_orders(orders: list[PurchaseOrder]) -> None:
    _save(DATA_DIR / "orders.json", [order.to_data() for order in orders])
