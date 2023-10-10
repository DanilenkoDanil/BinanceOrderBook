from django.core.management.base import BaseCommand
from binance_app.binance_websocket import BinanceWebSocket


class Command(BaseCommand):
    help = 'Fetches data from Binance via WebSocket'

    def handle(self, *args, **options):
        connection = BinanceWebSocket()
        connection.start_connection()
