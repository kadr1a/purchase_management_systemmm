from decimal import Decimal

from models import Application, Product


def test_application_approval_and_total() -> None:
    product = Product(1, "Монитор", "шт.", Decimal("20000"))
    application = Application(1, "Петров П.П.")
    application.add_product(product)

    assert application.total_price() == Decimal("20000")
    assert application.can_approve()

    application.approve()
    assert application.status == Application.APPROVED
