from django.contrib import admin
from .models import SecAuth_Model

@admin.register(SecAuth_Model)
class AuthAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']