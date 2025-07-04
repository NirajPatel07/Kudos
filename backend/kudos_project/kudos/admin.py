from django.contrib import admin
from .models import Kudo

@admin.register(Kudo)
class KudoAdmin(admin.ModelAdmin):
    list_display = ['giver', 'receiver', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['giver__username', 'receiver__username', 'message']
    readonly_fields = ['created_at']
