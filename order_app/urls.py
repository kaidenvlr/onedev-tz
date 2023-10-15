from django.urls import path

from order_app.views import get_orders, add_order, get_order

urlpatterns = [
    path('get-order/', get_order, name='get-order'),
    path('get-orders/', get_orders, name='get-orders'),
    path('add-order/', add_order, name='add-order'),
]
