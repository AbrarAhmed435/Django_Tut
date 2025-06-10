from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse  # (Not used here since we're using DRF's Response)
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.decorators import api_view  # To define function-based API views
from rest_framework.response import Response  # A DRF response class that renders data as JSON

# Function-based views using Django REST Framework

@api_view(['GET'])  # This view only allows GET requests
def product_list(request):
    """
    API endpoint to get the list of all products.
    """
    products = Product.objects.all()  # Query all Product objects from the database
    serializer = ProductSerializer(products, many=True)  # Serialize multiple products
    return Response(serializer.data)  # Return JSON response with serialized product data


@api_view(['GET'])  # This view only allows GET requests
def product_detail(request, pk):
    """
    API endpoint to get the detail of a specific product by primary key (pk).
    """
    product = get_object_or_404(Product, pk=pk)  # Try to get the product or return 404 if not found
    serializer = ProductSerializer(product)  # Serialize the single product
    return Response(serializer.data)  # Return JSON response with the product's data
