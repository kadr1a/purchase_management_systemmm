from decimal import Decimal
from pathlib import Path

import storage
from models import Application, Product, PurchaseOrder, Supplier


def test_json_roundtrip(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    product = Product(1, "Стул", "шт.", Decimal("2500"))
    supplier = Supplier(
        1, "ООО Мебель", "Анна", "+7 900 000-00-00", "anna@example.com"
    )
    application = Application(1, "Петров")
    application.add_product(product)
    application.approve()
    order = PurchaseOrder(1, application, supplier, [product])

    storage.save_products([product])
    storage.save_suppliers([supplier])
    storage.save_applications([application])
    storage.save_orders([order])

    loaded_products = storage.load_products()
    loaded_suppliers = storage.load_suppliers()
    loaded_applications = storage.load_applications(loaded_products)
    loaded_orders = storage.load_orders(
        loaded_applications, loaded_suppliers, loaded_products
    )

    assert loaded_orders[0].application is loaded_applications[0]
    assert loaded_orders[0].supplier is loaded_suppliers[0]
    assert loaded_orders[0].products[0] is loaded_products[0]
