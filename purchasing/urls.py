from django.contrib import admin
from django.urls import include, path
from homepage import views as homepage_views

handler404 = "homepage.views.page_not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("products/", include("products.urls")),
    path("suppliers/", include("suppliers.urls")),
    path("orders/", include("orders.urls")),
    path("applications/", include("applications.urls")),
]
