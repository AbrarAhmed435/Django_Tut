from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.ProductListAPIView.as_view()),
    path('products/<int:product_id>/',views.ProductDetailAPIView.as_view()),
    path('orders/',views.UserOrderListAPIView.as_view()),
    path('products/info',views.product_info),
]
