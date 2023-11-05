from django.contrib import admin
from ..models import Quote


@admin.register(Quote)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')
    list_filter = ('user',)
    search_fields = ('user',)
