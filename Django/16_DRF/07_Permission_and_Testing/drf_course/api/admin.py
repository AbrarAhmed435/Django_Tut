from django.contrib import admin
from api.models import Order, OrderItem
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model() #returns custom User module if present , else default one
admin.site.register(User, UserAdmin)#Show the User model in the admin panel, and use the built-in UserAdmin interface to manage it.


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model=OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines=[
        OrderItemInline
    ]
    
admin.site.register(Order,OrderAdmin)
