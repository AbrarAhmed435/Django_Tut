from django.db.models import Max
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse  # (Not used here since we're using DRF's Response)
from api.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from api.models import Product,Order,OrderItem
from rest_framework.decorators import api_view  # To define function-based API views
from rest_framework.response import Response  # A DRF response class that renders data as JSON
from rest_framework import generics


# views.py
from rest_framework import generics          # DRF’s generic class-based views
from .models import Product                  # Your Product model
from .serializers import ProductSerializer   # Converts Product objects → JSON

class ProductListAPIView(generics.ListAPIView):
    """
    Returns a paginated list of all Product objects.

    ⬇️  Why ListAPIView?
    • Handles only HTTP GET by default (read-only list)
    • Automatically wires in pagination, filter back-ends, and ordering
      if you’ve configured them in your REST_FRAMEWORK settings
    """

    # 🔍  Which records to fetch from the database?
    #     A lazily-evaluated Django QuerySet.  Change or override get_queryset()
    #     if you ever need user-specific or filtered results.
    queryset=Product.objects.filter(stock__gt=0) # return only if stock >0
    #queryset=Product.objects.exclude(stock__gt=0) #only out of stock product
    # 📦  Which serializer turns each Product instance into JSON?
    #     Also used for validation on write-endpoints (not needed here,
    #     but still required by DRF’s generic view contract).
    serializer_class = ProductSerializer


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
    #permission_classes = 

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
    

    
@api_view(['GET'])
def product_info(request):
    products=Product.objects.all()
    serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)