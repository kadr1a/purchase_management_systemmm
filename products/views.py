from django.shortcuts import render
from django.http import Http404
from db.database import get_connection

def products(request):
    conn = get_connection()
    try:
        items = conn.execute("SELECT id, name, price FROM products ORDER BY name").fetchall()
    finally:
        conn.close()
    return render(request, "products/product_list.html", {"products": items})

def product_detail(request, product_id):
    conn = get_connection()
    try:
        item = conn.execute("SELECT id, name, price FROM products WHERE id = ?", (product_id,)).fetchone()
    finally:
        conn.close()
    if item is None:
        raise Http404("Товар не найден")
    return render(request, "products/product_detail.html", {"product": item})
