from django.shortcuts import render
from db.database import get_connection

def applications(request):
    conn = get_connection()
    try:
        items = conn.execute(
            "SELECT id, requester, description, status FROM requests ORDER BY id"
        ).fetchall()
    finally:
        conn.close()
    return render(request, "applications/application_list.html", {"applications": items})
