from django.urls import path, include
from . import views
from rest_framework import routers
from .views import ProductViewSet
from rest_framework.authtoken.views import ObtainAuthToken

router = routers.DefaultRouter()
from rest_framework.routers import DefaultRouter
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'orders', views.OrderViewSet)
# router.register(r'order-items', views.OrderItemViewSet)

app_name = "polls"
urlpatterns = [
    path('', include(router.urls)),
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # lấy products theo category
    path('products/category/<int:category_id>/', views.ProductViewSet.as_view({'get': 'list'}), name='product-list-by-category'),
    path('product/<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
    path('products/', views.ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    # path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),  # Use ObtainAuthToken trực tiếp
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('register/', views.CustomerRegisterView.as_view(), name='register'),
    path('logout/', views.CustomerLogoutView.as_view(), name='logout'),
    path('customers/<int:pk>/change-password/', views.CustomerChangePasswordView.as_view(), name='customer-change-password'),
    path('customers/<int:pk>/', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('upload-images/', views.ImageUploadView.as_view(), name='upload-images'),
    # path('addresses/', views.AddressListView.as_view(), name='address-list'),
    # path('address/<int:user_id>/', views.CustomerAddressList.as_view(), name='customer-address-list'),
    path('customers/addresses/', views.CustomerAddressList.as_view(), name='customer-address-list'),
    path('address/create/', views.CreateAddressView.as_view(), name='create-address'), 
    path('address/update/<int:address_id>/', views.UpdateAddressView.as_view(), name='update-address'),
    path('address/delete/<int:address_id>/', views.DeleteAddressView.as_view(), name='delete-address'),
    # create order
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),
    path('customer-orders/', views.CustomerOrdersView.as_view(), name='customer-orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    # category
    # path('products/category/<int:category_id>/', views.ProductListByCategory.as_view(), name='product-list-by-category'),
    # contact
    path('contact/', views.ContactView.as_view(), name='contact'),
]