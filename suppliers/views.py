from django.shortcuts import render
from db.database import get_connection

def suppliers(request):
    conn = get_connection()
    try:
        items = conn.execute("SELECT id, name, contact_person, phone, email, address FROM suppliers ORDER BY name").fetchall()
    finally:
        conn.close()
    return render(request, "suppliers/supplier_list.html", {"suppliers": items})
