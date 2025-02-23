from django.contrib import admin
from .models import Investment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'initiative', 'amount', 'date_invested')
    list_filter = ('initiative', 'date_invested')
    search_fields = ('user__username', 'initiative__title')