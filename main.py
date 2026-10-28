from __future__ import annotations

from models import Application, Product, PurchaseOrder, Supplier
from models.applications import (
    find_application,
    show_applications,
)
from models.orders import find_order, show_orders
from models.products import show_products
from models.suppliers import show_suppliers
from storage import (
    load_applications,
    load_orders,
    load_products,
    load_suppliers,
    save_applications,
    save_orders,
    save_products,
    save_suppliers,
)
from utils import input_int


def show_menu() -> None:
    print("\n=== Система управления закупками ===")
    print("1. Показать товары")
    print("2. Показать поставщиков")
    print("3. Показать заявки")
    print("4. Согласовать заявку")
    print("5. Создать заказ по заявке")
    print("6. Показать заказы")
    print("7. Отменить заказ")
    print("0. Выход")


def approve_application(applications: list[Application]) -> None:
    application_id = input_int("ID заявки: ")
    application = find_application(applications, application_id)
    if application is None:
        print("Заявка не найдена.")
        return
    try:
        application.approve()
        print(f"Заявка №{application.id} согласована.")
    except ValueError as error:
        print(error)


def create_order_from_application(
    applications: list[Application],
    suppliers: list[Supplier],
    orders: list[PurchaseOrder],
) -> None:
    application_id = input_int("ID заявки: ")
    supplier_id = input_int("ID поставщика: ")
    application = find_application(applications, application_id)
    supplier = next((item for item in suppliers if item.id == supplier_id), None)
    if application is None or supplier is None:
        print("Заявка или поставщик не найдены.")
        return
    order_id = max((order.id for order in orders), default=0) + 1
    order = PurchaseOrder(
        id=order_id,
        application=application,
        supplier=supplier,
        products=list(application.products),
    )
    try:
        from models.orders import create_order

        create_order(orders, order)
        print(f"Создан {order}.")
    except ValueError as error:
        print(error)


def cancel_order(orders: list[PurchaseOrder]) -> None:
    order_id = input_int("ID заказа: ")
    order = find_order(orders, order_id)
    if order is None:
        print("Заказ не найден.")
        return
    try:
        order.cancel()
        print(f"Заказ №{order.id} отменён.")
    except ValueError as error:
        print(error)


def main() -> None:
    products = load_products()
    suppliers = load_suppliers()
    applications = load_applications(products)
    orders = load_orders(applications, suppliers, products)

    while True:
        show_menu()
        choice = input_int("Выберите действие: ")
        if choice == 1:
            show_products(products)
        elif choice == 2:
            show_suppliers(suppliers)
        elif choice == 3:
            show_applications(applications)
        elif choice == 4:
            approve_application(applications)
        elif choice == 5:
            create_order_from_application(applications, suppliers, orders)
        elif choice == 6:
            show_orders(orders)
        elif choice == 7:
            cancel_order(orders)
        elif choice == 0:
            save_products(products)
            save_suppliers(suppliers)
            save_applications(applications)
            save_orders(orders)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Такого пункта меню нет.")


if __name__ == "__main__":
    main()
