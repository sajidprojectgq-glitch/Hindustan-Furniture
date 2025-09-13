from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("products/", views.products, name="products"),  # Products page

    # Admin dashboard
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("admin-log/", views.admin_log, name="admin_log"),

    # Furniture management (superuser only)
    path("upload/", views.upload_furniture, name="upload_furniture"),
    path("edit/<int:pk>/", views.edit_furniture, name="edit_furniture"),
    path("delete/<int:pk>/", views.delete_furniture, name="delete_furniture"),

    # About & Contact
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),

   # details
   path('details/<int:pk>/', views.details, name='details'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
