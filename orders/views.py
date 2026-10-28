from django.shortcuts import render
from db.database import get_connection

def orders(request):
    conn = get_connection()
    try:
        items = conn.execute("""
            SELECT o.id, o.order_date, o.status, p.name AS product_name,
                   s.name AS supplier_name, o.is_cancelled
            FROM orders o
            JOIN products p ON p.id = o.product_id
            JOIN suppliers s ON s.id = o.supplier_id
            ORDER BY o.order_date DESC, o.id DESC
        """).fetchall()
    finally:
        conn.close()
    return render(request, "orders/order_list.html", {"orders": items, "search_date": ""})

def orders_by_date(request):
    order_date = request.GET.get("date", "").strip()
    items = []
    if order_date:
        conn = get_connection()
        try:
            items = conn.execute("""
                SELECT o.id, o.order_date, o.status, p.name AS product_name,
                       s.name AS supplier_name, o.is_cancelled
                FROM orders o
                JOIN products p ON p.id = o.product_id
                JOIN suppliers s ON s.id = o.supplier_id
                WHERE o.order_date = ?
                ORDER BY o.id
            """, (order_date,)).fetchall()
        finally:
            conn.close()
    return render(request, "orders/order_list.html", {"orders": items, "search_date": order_date})
