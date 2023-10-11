from django.db import models


class Order(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    ORDER_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    symbol = models.CharField(max_length=10)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default=BUY)
    status = models.CharField(max_length=10,
                              default='open')

    price = models.DecimalField(max_digits=30, decimal_places=15)
    amount = models.DecimalField(max_digits=30, decimal_places=15)
    stop_loss = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    profit = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)

    def __str__(self):
        return f"{self.order_type} order for {self.symbol} - Status: {self.status}"

    def save(self, *args, **kwargs):
        if self.current_price is not None:
            self.total_price = self.current_price * self.amount

            if self.status == 'bought':
                self.profit = self.total_price - self.price * self.amount

        super(Order, self).save(*args, **kwargs)
