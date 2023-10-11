from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from decimal import Decimal


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def update_order_status(active_orders, updated_symbols):
    to_update = []

    for order in active_orders:
        current_price = updated_symbols.get(order.symbol)
        if not current_price:
            continue

        current_price_decimal = Decimal(str(current_price))
        order.current_price = current_price_decimal
        order.total_price = order.current_price * order.amount

        if order.order_type == Order.BUY:
            if current_price_decimal <= order.price:
                order.status = 'bought'

            if order.status == 'bought':
                if order.current_price is not None:
                    order.profit = order.total_price - order.price * order.amount
                if order.stop_loss and current_price_decimal <= order.stop_loss:
                    order.status = 'stopped'
                elif order.take_profit and current_price_decimal >= order.take_profit:
                    order.status = 'profited'

        elif order.order_type == Order.SELL:
            if current_price_decimal >= order.price:
                order.status = 'sold'

        to_update.append(order)

    Order.objects.bulk_update(to_update, ['status', 'profit', 'total_price', 'current_price'])
