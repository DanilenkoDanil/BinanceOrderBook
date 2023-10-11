from django.contrib import admin
from order_api.models import Order


@admin.register(Order)
class BinanceSymbolAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol')  # Здесь вы можете указать поля, которые вы хотите отображать в списке
    search_fields = ['symbol']
