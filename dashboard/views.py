from django.shortcuts import render
from order_api.models import Order


def orders_view(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})
