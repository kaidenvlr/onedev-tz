from rest_framework import serializers

from apps.order_app.models import OrderImage, Order


class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ["id", "order", "image"]


class OrderSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = OrderImage.objects.filter(order=obj)
        return OrderImageSerializer(images, many=True, read_only=False).data

    class Meta:
        model = Order
        fields = ["id", "user", "status", "images"]
