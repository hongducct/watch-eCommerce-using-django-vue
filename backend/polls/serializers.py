# Trong file serializers.py của ứng dụng của bạn (ví dụ: polls/serializers.py)

from rest_framework import serializers
from .models import Choice, Question
from .models import Product, Category, Customer, UserStatus, Image, Attribute, Address, Order, OrderItem, OrderStatus, Contact

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    # avatar = serializers.ImageField(required=False, allow_null=True)  # Cho phép avatar là null
    def create(self, validated_data):
        # Tạo người dùng mới với is_active=True
        user = Customer.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            password=validated_data['password'],
            email=validated_data['email'],
            avatar=validated_data.get('avatar', None),  # Sử dụng get để lấy avatar từ validated_data
            is_active=True,  # Đặt is_active=True
            # ... các trường khác
        )
        return user
    class Meta:
        model = Customer
        fields = '__all__'
class ChangePasswordSerializer(serializers.ModelSerializer):
    oldPassword = serializers.CharField(required=True, write_only=True)
    newPassword = serializers.CharField(required=True, write_only=True)

    class Meta:
        model  = Customer
        fields = ('oldPassword', 'newPassword')
class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_path']  # Hoặc tên trường chứa đường dẫn ảnh của bạn

class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    # Sử dụng nested serializer cho Category
    attribute = AttributeSerializer(required=False)  # Attribute có thể null, nên đặt required=False
    # images = ImageSerializer(many=True, read_only=True)  # Một sản phẩm có nhiều ảnh
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        if hasattr(obj, 'prefetched_images'):
            return ImageSerializer(obj.prefetched_images, many=True).data
        else:
            return ImageSerializer(obj.image_set.all(), many=True).data

    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'description', 'price', 'stock', 'category', 'attribute', 'images')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)  # Đánh dấu trường 'user' là read_only
    

    
class OrderStatusSerializer(serializers.ModelSerializer): 

    class Meta:
        model = OrderStatus
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer): 
    product_id = serializers.IntegerField()  # Đảm bảo trường product_id tồn tại và không phải read_only
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price']

class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'price', 'product']

class OrderDetailSerializer(serializers.ModelSerializer):
    order_items = OrderItemDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'order_date',
            'total_amount',
            'status',
            'order_items',
            'shipping_name',
            'shipping_phone',
            'shipping_address',
            'shipping_province',
            'shipping_district',
            'shipping_ward',
            # 'shipping_fee'
        ]

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    status = serializers.PrimaryKeyRelatedField(queryset=OrderStatus.objects.all())

    class Meta:
        model = Order
        fields = [
            'id',
            'user', 
            'order_date', 
            'total_amount', 
            'status', 
            'order_items',
            'shipping_name', 
            'shipping_phone', 
            'shipping_address', 
            'shipping_province',
            'shipping_district',
            'shipping_ward'
        ]

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        
        # Lấy thông tin địa chỉ giao hàng
        shipping_name = validated_data.pop('shipping_name')
        shipping_phone = validated_data.pop('shipping_phone')
        shipping_address = validated_data.pop('shipping_address')
        shipping_province = validated_data.pop('shipping_province')
        shipping_district = validated_data.pop('shipping_district')
        shipping_ward = validated_data.pop('shipping_ward')

        # Tạo đơn hàng
        order = Order.objects.create(**validated_data)

        # Tạo các sản phẩm trong đơn hàng
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)

        # Cập nhật thông tin địa chỉ giao hàng cho đơn hàng
        order.shipping_name = shipping_name
        order.shipping_phone = shipping_phone
        order.shipping_address = shipping_address
        order.shipping_province = shipping_province
        order.shipping_district = shipping_district
        order.shipping_ward = shipping_ward
        order.save()

        return order
# class OrderSerializer(serializers.ModelSerializer):
#     order_items = OrderItemSerializer(many=True)
#     status = serializers.PrimaryKeyRelatedField(queryset=OrderStatus.objects.all())

#     class Meta:
#         model = Order
#         fields = ['user', 'order_date', 'total_amount', 'status', 'order_items']

#     def create(self, validated_data):
#         order_items_data = validated_data.pop('order_items')
#         order = Order.objects.create(**validated_data)

#         for order_item_data in order_items_data:
#             OrderItem.objects.create(order=order,  **order_item_data)

#         return order

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'