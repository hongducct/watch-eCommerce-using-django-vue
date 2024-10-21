from django.contrib import admin
from .models import Choice, Question
from .models import Product, Category, Customer, Address, Image, Attribute, Order, OrderItem, OrderStatus, Contact

class AttributeInline(admin.StackedInline):
    model = Attribute

class ImageInline(admin.TabularInline):  # Hoặc StackedInline nếu bạn muốn
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [AttributeInline, ImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatus)
admin.site.register(Contact)