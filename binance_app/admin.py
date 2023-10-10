from django.contrib import admin
from binance_app.models import BinanceSymbol


@admin.register(BinanceSymbol)
class BinanceSymbolAdmin(admin.ModelAdmin):
    list_display = ('id', 'symbol', 'price')  # Здесь вы можете указать поля, которые вы хотите отображать в списке
    search_fields = ['symbol']