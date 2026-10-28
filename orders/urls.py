from django.urls import path
from . import views
app_name = "orders"
urlpatterns = [path("", views.orders, name="list"), path("by-date/", views.orders_by_date, name="by_date")]
