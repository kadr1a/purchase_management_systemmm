from decimal import Decimal

from models import Application, Product, PurchaseOrder, Supplier
from models.orders import create_order


def test_order_links_application_supplier_and_products() -> None:
    product = Product(1, "Клавиатура", "шт.", Decimal("3000"))
    application = Application(1, "Сидоров С.С.")
    application.add_product(product)
    application.approve()
    supplier = Supplier(
        1, "ООО Поставка", "Иванов И.И.", "+7 900 000-00-00", "mail@example.com"
    )
    order = PurchaseOrder(1, application, supplier, [product])
    orders: list[PurchaseOrder] = []

    create_order(orders, order)

    assert orders[0].application is application
    assert orders[0].supplier is supplier
    assert orders[0].products[0] is product
    assert order.total_price() == Decimal("3000")
    assert application.status == Application.ORDERED


def test_order_cancel() -> None:
    product = Product(1, "Мышь", "шт.", Decimal("1500"))
    application = Application(1, "Сидоров С.С.")
    application.add_product(product)
    application.approve()
    supplier = Supplier(
        1, "ООО Поставка", "Иванов И.И.", "+7 900 000-00-00", "mail@example.com"
    )
    order = PurchaseOrder(1, application, supplier, [product])

    order.cancel()

    assert order.status == PurchaseOrder.CANCELLED
