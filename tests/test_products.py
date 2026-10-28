from decimal import Decimal

from models import Product


def test_product_creation_and_total_cost() -> None:
    product = Product(1, "Бумага А4", "пачка", Decimal("500.00"))
    assert product.id == 1
    assert product.name == "Бумага А4"
    assert product.total_cost(3) == Decimal("1500.00")


def test_inactive_product_cannot_be_used_in_application() -> None:
    from models import Application

    product = Product(1, "Старый товар", "шт.", Decimal("100"), False)
    application = Application(1, "Иванов И.И.")
    try:
        application.add_product(product)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Ожидалась ошибка для неактивного товара"
        )
