from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, Mock
from binance_app.models import BinanceSymbol
from binance_app.binance_websocket import BinanceWebSocket
import json


class BinanceFetcherTests(TestCase):

    @patch('binance_app.binance_websocket.websocket.WebSocketApp')
    def test_command_runs(self, MockWebSocket):
        mock_ws = Mock()
        mock_ws.run_forever.return_value = None

        MockWebSocket.return_value = mock_ws

        call_command('fetch_binance')
        mock_ws.run_forever.assert_called_once()

    @patch('binance_app.binance_websocket.websocket.WebSocketApp')
    def test_on_message_creates_new_symbol(self, MockWebSocket):
        test_message = json.dumps([{"s": "BTCUSDT", "c": "50000"}])

        mock_ws = Mock()
        mock_ws.run_forever.return_value = None
        MockWebSocket.return_value = mock_ws

        binance_ws = BinanceWebSocket()
        binance_ws.on_message(mock_ws, test_message)

        symbol = BinanceSymbol.objects.get(symbol="BTCUSDT")
        self.assertEqual(symbol.price, 50000)

    @patch('binance_app.binance_websocket.websocket.WebSocketApp')
    def test_on_message_updates_existing_symbol(self, MockWebSocket):
        BinanceSymbol.objects.create(symbol="BTCUSDT", price=49000)
        test_message = json.dumps([{"s": "BTCUSDT", "c": "50000"}])

        mock_ws = Mock()
        mock_ws.run_forever.return_value = None

        MockWebSocket.return_value = mock_ws

        binance_ws = BinanceWebSocket()
        binance_ws.on_message(mock_ws, test_message)

        symbol = BinanceSymbol.objects.get(symbol="BTCUSDT")
        self.assertEqual(symbol.price, 50000)
