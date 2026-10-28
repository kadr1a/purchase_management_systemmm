import json
from pathlib import Path
from db.database import BASE_DIR, get_connection, initialize_database

DATA_DIR = BASE_DIR / "data"

def read_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))

def import_all():
    initialize_database()
    products = read_json("products.json")
    suppliers = read_json("suppliers.json")
    applications = read_json("applications.json")
    orders = read_json("orders.json")
    with get_connection() as conn:
        # Идемпотентный импорт: повторный запуск не создаёт дубликаты.
        conn.execute("DELETE FROM orders")
        conn.execute("DELETE FROM requests")
        conn.execute("DELETE FROM products")
        conn.execute("DELETE FROM suppliers")
        conn.executemany(
            "INSERT INTO products (id, name, price, unit, is_active) VALUES (?, ?, ?, ?, ?)",
            [(p["id"], p["name"], float(p["price"]), p.get("unit", "шт."), int(p.get("is_active", True))) for p in products],
        )
        conn.executemany(
            "INSERT INTO suppliers (id, name, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?, ?)",
            [(s["id"], s["name"], s.get("contact_person", s.get("name", "")), s.get("phone", ""), s.get("email", ""), s.get("address", "")) for s in suppliers],
        )
        # JSON-заявки импортируются как requests. order_id допускает NULL,
        # поскольку исходные заявки могут ещё не иметь оформленного заказа.
        conn.executemany(
            "INSERT INTO requests (id, requester, description, status, order_id) VALUES (?, ?, ?, ?, NULL)",
            [(a["id"], a.get("requester", "Не указан"), a.get("comment", ""), a.get("status", "created")) for a in applications],
        )
        for order in orders:
            application_id = order.get("application_id")
            supplier_id = order.get("supplier_id")
            product_ids = order.get("product_ids", [])
            if not product_ids or supplier_id not in {s["id"] for s in suppliers}:
                continue
            for product_id in product_ids:
                conn.execute(
                    "INSERT INTO orders (id, product_id, supplier_id, order_date, status, is_cancelled, request_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (order["id"], product_id, supplier_id, order.get("delivery_date") or "2026-01-01", order.get("status", "new"), int(order.get("status") == "cancelled"), application_id),
                )
        # Связь заявки с заказом (если заказ существует).
        conn.execute("UPDATE requests SET order_id = (SELECT MIN(orders.id) FROM orders WHERE orders.request_id = requests.id) WHERE EXISTS (SELECT 1 FROM orders WHERE orders.request_id = requests.id)")

if __name__ == "__main__":
    import_all()
    print(f"Данные импортированы в {BASE_DIR / 'data' / 'purchases.sqlite'}")
