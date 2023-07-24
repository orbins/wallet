from django.contrib import admin

from ..models import TransactionCategory


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user')
