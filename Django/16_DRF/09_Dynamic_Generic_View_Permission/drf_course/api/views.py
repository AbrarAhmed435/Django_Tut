from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse  # (Not used here since we're using DRF's Response)
from api.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from api.models import Product,Order,OrderItem
from rest_framework.decorators import api_view  # To define function-based API views
from rest_framework.response import Response  # A DRF response class that renders data as JSON
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.views import APIView


# views.py
from rest_framework import generics          # DRF’s generic class-based views
from .models import Product                  # Your Product model
from .serializers import ProductSerializer   # Converts Product objects → JSON


""" 
=================================
= Post request to create product =
==================================
"""
""" class PoductCreateAPIView(generics.CreateAPIView):
    model=Product
    serializer_class=ProductSerializer #reusing Product serilizer as it is similary 
    
    def create(self,request,*args,**kwargs):
        print(request.data)
        return super().create(request,*args,**kwargs) #calls actual creat method https://www.cdrf.co/
         """
    
class ProductListCreateAPIView(generics.ListCreateAPIView): #create and Read with same class
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
    def get_permissions(self):
       self.permission_classes=[AllowAny] #default permission class
       if self.request.method=='POST':
           self.permission_classes=[IsAdminUser]
       return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_url_kwarg='product_id'


""" class OrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product').all()
    serializer_class=OrderSerializer """
class UserOrderListAPIView(generics.ListAPIView):
    """
    Returns a list of Order objects that belong to the **currently
    authenticated user**.

    Why a dedicated view?
    ─────────────────────
    • Keeps the endpoint simple—no need for the client to supply
      `?user=id` every time.
    • Prevents accidental data leaks by enforcing user-level filtering
      on the server side.
    """
    # ------------------------------------------------------------------
    # Base queryset
    # ------------------------------------------------------------------
    # 1. `prefetch_related('items__product')` grabs all OrderItems and
    #    their associated Product objects in one additional query,
    #    eliminating the N+1 problem when the serializer dereferences
    #    `order.items` and `item.product`.
    # 2. `.all()` materializes the QuerySet so we can start chaining
    #    further filters safely.
    queryset = (
        Order.objects
             .prefetch_related('items__product')
             .all()
    )

    # Serializer that converts Order instances → JSON
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] 

    # ------------------------------------------------------------------
    # Custom queryset logic
    # ------------------------------------------------------------------
    def get_queryset(self):
        """
        Override the default `get_queryset()` to scope results to the
        request’s user while preserving all optimizations defined in
        the base queryset.
        """
        user = self.request.user                 # The logged-in user
        qs   = super().get_queryset()            # Reuse base queryset
        return qs.filter(user=user)              # Apply user filter
    

    """ Generic views like ListAPIView are great when you're returning just a list of model instances, 
    If your output is not just a flat list but a custom structure (dicts, summaries, aggregations, mixes of multiple models), then APIView or @api_view gives you full control over the response structure.
    
    ListAPIView:	You want to return a list of a single model’s objects
    APIView: You want to return a custom structure, aggregate values, or mix data
    """

class ProductInfoAPIView(APIView):
  def get(self,request):
    products=Product.objects.all()
    serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
    
    
""" @api_view(['GET'])
def product_info(request):
    products=Product.objects.all()
    serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data) """