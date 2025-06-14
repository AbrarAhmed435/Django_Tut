"""
serializers.py
---------------
DRF serializers for the e‑commerce app.

• ProductSerializer  – expose basic product info and price validation
• OrderItemSerializer – represent a single product‑quantity pair inside an order
• OrderSerializer    – wrap an order’s metadata plus its items
"""

from rest_framework import serializers
from .models import Product, Order, OrderItem,User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Exposes a subset of fields and validates that price is positive.
    """

    class Meta:
        model = Product
        # Explicit list keeps the API surface predictable
        fields = ['id',"description", "name", "description", "price", "stock"]

    # ---- Field‑level validation ------------------------------------------------
    def validate_price(self, value):
        """
        Ensure price is strictly greater than 0.

        DRF automatically calls any method named `validate_<fieldname>`
        when validating that field.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for an individual line item inside an order.
    """
    product_name=serializers.CharField(source='product.name')
    product_price=serializers.DecimalField(source='product.price',max_digits=10,decimal_places=2)
    #product=ProductSerializer()
    class Meta:
        model = OrderItem
        # Only the foreign key to Product and the quantity are needed here
        fields = ['product_name','product_price', "quantity",'item_subtotal'] #removing order_id because it  is same as order_id of order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    Includes nested, read‑only list of its OrderItem objects.
    """
  
    # Nest all related items; `many=True` -> list, `read_only=True` -> cannot
    # create/update items from this serializer (handled elsewhere or via view logic)
    items = OrderItemSerializer(many=True, read_only=True) #without this pk's will be listed, as we are not mentioning how to serialize items
    total_price=serializers.SerializerMethodField() #or we can pass method_name if we don't use get<field_name> as function name
    user=UserSerializer(read_only=True)
    def get_total_price(self,obj):
        order_items = obj.items.all()
        return round(sum(order_item.item_subtotal for order_item in order_items), 2)


    class Meta:
        model = Order
        fields = ["order_id", "created_at", "user", "status", "items",'total_price']


class ProductInfoSerializer(serializers.Serializer):
    #get all products, count of products , max price
    products=ProductSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.FloatField()