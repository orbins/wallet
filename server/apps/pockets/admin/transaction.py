from django.contrib import admin

from ..models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'category', 'user', 'transaction_date')
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('transaction_type', 'amount', 'category', 'user', 'transaction_date')
