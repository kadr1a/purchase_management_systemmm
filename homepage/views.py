from django.http import HttpResponse
from django.shortcuts import render
from db.database import get_connection

def index(request):
    conn = get_connection()
    try:
        counts = {
            "products_count": conn.execute("SELECT COUNT(*) FROM products").fetchone()[0],
            "suppliers_count": conn.execute("SELECT COUNT(*) FROM suppliers").fetchone()[0],
            "orders_count": conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0],
            "applications_count": conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0],
        }
    finally:
        conn.close()
    return render(request, "homepage/index.html", counts)

def page_not_found(request, exception):
    return render(request, "404.html", status=404)
