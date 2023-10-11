from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from decimal import Decimal
from .models import Order
from .views import update_order_status


class OrderViewSetTest(APITestCase):

    def setUp(self):
        self.order = Order.objects.create(
            symbol="BTCUSDT",
            order_type=Order.BUY,
            price=Decimal("10000"),
            amount=Decimal("1")
        )

    def test_create_order(self):
        data = {
            "symbol": "ETHUSDT",
            "order_type": Order.BUY,
            "price": "2000",
            "amount": "5"
        }

        response = self.client.post("/api/orders/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=2).symbol, "ETHUSDT")

    def test_read_order(self):
        response = self.client.get(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], 'BTCUSDT')

    def test_update_order(self):
        data = {
            "symbol": "BTCUSDT",
            "order_type": Order.SELL,
            "price": "11000",
            "amount": "1.5"
        }

        response = self.client.put(f"/api/orders/{self.order.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_type, Order.SELL)
        self.assertEqual(self.order.price, Decimal("11000"))
        self.assertEqual(self.order.amount, Decimal("1.5"))

    def test_delete_order(self):
        response = self.client.delete(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


class UpdateOrderStatusTest(TestCase):

    def setUp(self):
        self.order_buy = Order.objects.create(
            symbol="BTCUSDT",
            order_type=Order.BUY,
            status='open',
            price=Decimal("10000"),
            amount=Decimal("1")
        )

        self.order_sell = Order.objects.create(
            symbol="BTCUSDT",
            order_type=Order.SELL,
            status='open',
            price=Decimal("15000"),
            amount=Decimal("1")
        )

    def test_update_order_status_buy(self):
        updated_symbols = {"BTCUSDT": "9500"}

        update_order_status(Order.objects.all(), updated_symbols)

        self.order_buy.refresh_from_db()
        self.assertEqual(self.order_buy.status, 'bought')
        self.assertEqual(self.order_buy.current_price, Decimal("9500"))
        self.assertEqual(self.order_buy.total_price, Decimal("9500"))

    def test_update_order_status_sell(self):
        updated_symbols = {"BTCUSDT": "15500"}
        update_order_status(Order.objects.all(), updated_symbols)

        self.order_sell.refresh_from_db()
        self.assertEqual(self.order_sell.status, 'sold')
