from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from order_app.models import Order
from order_app.responses import order_not_found_response, order_response, orders_response
from order_app.serializers import OrderSerializer, OrderImageSerializer


@swagger_auto_schema(
    methods=['get'],
    responses={
        200: orders_response
    }
)
@api_view(('GET',))
@permission_classes((AllowAny,))
def get_orders(request: Request):
    if hasattr(request.user, 'user'):
        user = request.user.user
        queryset = Order.objects.filter(Q(user_id=user.id) | Q(user__isnull=True))
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    queryset = Order.objects.filter(user_id=None)
    serializer = OrderSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['get'],
    manual_parameters=[
        openapi.Parameter("order_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                          description="Order ID to fetch")
    ],
    responses={
        200: order_response,
        404: order_not_found_response
    }
)
@api_view(('GET',))
@permission_classes((AllowAny,))
def get_order(request: Request):
    user = None
    if hasattr(request.user, 'user'):
        user = request.user.user
    order_id = request.query_params.get("order_id")
    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return Response({'status': 'error', 'description': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    if user != order.user:
        return Response({'status': 'error', 'description': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['post'],
    manual_parameters=[
        openapi.Parameter("images", openapi.IN_FORM, type=openapi.TYPE_ARRAY,
                          items=openapi.Items(type=openapi.TYPE_FILE),
                          description="Image")
    ],
    responses={
        201: order_response
    }
)
@api_view(('POST',))
@permission_classes((AllowAny,))
@parser_classes((MultiPartParser,))
def add_order(request: Request):
    user = None
    data = dict()
    if hasattr(request.user, 'user'):
        user = request.user.user
        data["user"] = user.id
    order_serializer = OrderSerializer(data=data)
    order_serializer.is_valid(raise_exception=True)
    order = order_serializer.save()

    if request.FILES:
        images = dict(request.FILES.lists()).get("images", None)
        if images:
            for image in images:
                image_data = dict()
                image_data["order"] = order.id
                image_data["image"] = image
                image_serializer = OrderImageSerializer(data=image_data)
                image_serializer.is_valid(raise_exception=True)
                image_serializer.save()

        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
