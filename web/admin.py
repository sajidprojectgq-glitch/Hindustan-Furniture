from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CategorizePost

@admin.register(CategorizePost)
class CategorizePostAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "price", "date")
    search_fields = ("title", "type")
