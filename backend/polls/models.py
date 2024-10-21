# Create your models here.
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

from django.contrib.auth.models import AbstractUser  # Để tùy chỉnh mô hình User

# users
# class User(AbstractUser):
#     avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Giả sử bạn muốn lưu trữ hình ảnh avatar
#     name = models.CharField(max_length=255)
#     login_at = models.DateTimeField(null=True, blank=True)
#     change_password_at = models.DateTimeField(null=True, blank=True)

#     # ... các trường khác từ AbstractUser (username, email, password, etc.)
#     groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
#     user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)
class Customer(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    name = models.CharField(max_length=255)
    login_at = models.DateTimeField(auto_now=True)
    change_password_at = models.DateTimeField(null=True, blank=True)
    status = models.ForeignKey('UserStatus', on_delete=models.CASCADE, null=True, blank=True)  # Thêm trường status

    def __str__(self):
        return self.username
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_customer_email')
        ]

# users_status
class UserStatus(models.Model):
    name = models.CharField(max_length=255)

# categories
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

# products
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Product #{self.id}"
  # Liên kết với Category

# product_categories (không cần thiết trong Django, đã có mối quan hệ ở trên)

# attributes
class Attribute(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)  # Mỗi sản phẩm có một Attribute
    movement = models.CharField(max_length=255)
    case = models.CharField(max_length=255)
    strap = models.CharField(max_length=255)
    water_resistance = models.CharField(max_length=255)

# reviews
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    comment = models.TextField()


# orders
class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    # Thông tin địa chỉ giao hàng (bắt buộc)
    shipping_name = models.CharField(max_length=255, blank=False)
    shipping_phone = models.CharField(max_length=20, blank=False)
    shipping_address = models.TextField(blank=False)
    shipping_province = models.CharField(max_length=100, blank=False)
    shipping_district = models.CharField(max_length=100, blank=False)
    shipping_ward = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"Order #{self.id}"
# order_items
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items') # mới phải sửa, thêm related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id}"

# admins (tương tự như User, có thể kế thừa từ AbstractUser hoặc tạo một mô hình riêng)
class Admin(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    name = models.CharField(max_length=255)

    # ... các trường khác từ AbstractUser
    groups = models.ManyToManyField('auth.Group', related_name='admin_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='admin_user_permissions', blank=True)

# orders_status
class OrderStatus(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

# images
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image_set')
    image_path = models.ImageField(upload_to='product_images/')  # Giả sử bạn muốn lưu trữ hình ảnh sản phẩm

# addresses
class Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    address = models.TextField()

class Contact(models.Model):
    name = models.CharField(max_length=100)  # Changed to 'name'
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email