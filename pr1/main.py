from datetime import date

product_name = "Ноутбук"
price = 50000
order_date = date(2026, 9, 15)
is_available = True

def get_order_status(available: bool) -> str:
    if available:
        return "Товар доступен для заказа"
    return "Товар отсутствует на складе"

def main() -> None:
    print(f"Товар: {product_name}")
    print(f"Цена: {price} руб.")
    print(f"Дата заказа: {order_date}")
    print(get_order_status(is_available))

if __name__ == "__main__":
    main()
