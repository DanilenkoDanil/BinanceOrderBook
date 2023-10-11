import websocket
import json
import logging
import time

from order_api.views import update_order_status
from order_api.models import Order
from binance_order_book import settings
from binance_app.models import BinanceSymbol

logger = logging.getLogger(__name__)


class BinanceWebSocket:

    MAX_RETRIES = 5
    RETRY_INTERVAL_BASE = 5

    def __init__(self):
        self.retries = 0

    @staticmethod
    def update_symbols(data):
        existing_symbols = BinanceSymbol.objects.filter(symbol__in=[item['s'] for item in data]).all()
        existing_symbols_map = {symbol.symbol: symbol for symbol in existing_symbols}

        to_update = []
        to_create = []

        for item in data:
            symbol_name = item['s']
            current_price = item['c']

            if symbol_name in existing_symbols_map:
                symbol = existing_symbols_map[symbol_name]
                symbol.price = current_price
                to_update.append(symbol)
            else:
                to_create.append(BinanceSymbol(symbol=symbol_name, price=current_price))

        BinanceSymbol.objects.bulk_update(to_update, ['price'])
        BinanceSymbol.objects.bulk_create(to_create)

    def on_message(self, ws, message):
        try:
            data = json.loads(message)

            updated_symbols = {item['s']: float(item['c']) for item in data}
            active_orders = Order.objects.filter(symbol__in=updated_symbols.keys(), status__in=['open', 'bought'])

            self.update_symbols(data)
            update_order_status(active_orders, updated_symbols)

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)

    def on_close(self, ws, *args):
        self.retries += 1
        if self.retries <= self.MAX_RETRIES:
            retry_interval = self.RETRY_INTERVAL_BASE * self.retries
            logger.warning(f"WebSocket connection closed. Reconnecting in {retry_interval} seconds... Attempt "
                           f"{self.retries}/{self.MAX_RETRIES}")
            time.sleep(retry_interval)
            self.start_connection()
        else:
            logger.error("Max retries reached. Exiting...")

    def start_connection(self):
        try:
            socket_url = settings.BINANCE_WEBSOCKET_URL
            ws = websocket.WebSocketApp(socket_url, on_message=self.on_message, on_close=self.on_close)
            ws.run_forever()
            logger.info("WebSocket connection started")
            self.retries = 0
        except Exception as e:
            logger.error(f"Error starting WebSocket connection: {e}", exc_info=True)
