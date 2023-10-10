from django.db import models


class BinanceSymbol(models.Model):
    symbol = models.CharField(max_length=50)
    price = models.FloatField()


def get_binance_symbol(symbol: str):
    BinanceSymbol.objects.get()