from rest_framework import serializers
from .models import Product,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','description','price','stock']
    
    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError("price must be greater that or equal to 0")
        return value
