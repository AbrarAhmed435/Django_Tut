from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),
    path('products/<int:product_id>/',views.ProductDetailAPIView.as_view()),
    path('user-orders/',views.UserOrderListAPIView.as_view(),name='user-orders'),
    path('products/info',views.ProductInfoAPIView.as_view()),
]
