from django.contrib import admin
from .models import Investment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'initiative', 'amount', 'created_at')
    list_filter = ('created_at',)