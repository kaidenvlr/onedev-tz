from drf_yasg import openapi

from order_app.schemas import OrderNotFoundResponseSchema
from order_app.serializers import OrderSerializer

orders_response = openapi.Response('Orders Response', OrderSerializer(many=True))
order_response = openapi.Response('Order response', OrderSerializer)
order_not_found_response = openapi.Response('Order not found', OrderNotFoundResponseSchema)
