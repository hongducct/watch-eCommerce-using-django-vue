from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
from .models import Product, Category, Customer, UserStatus, Image, Attribute, Address, Order, OrderStatus, OrderItem, Contact
from .serializers import QuestionSerializer, AddressSerializer, OrderItemSerializer, OrderSerializer, OrderStatusSerializer, OrderDetailSerializer
from .serializers import ProductSerializer, CategorySerializer, CustomerSerializer, ImageSerializer, ChangePasswordSerializer, ContactSerializer

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Prefetch
from rest_framework import status, generics

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']  # Lấy ID danh mục từ URL
        return Product.objects.filter(category_id=category_id)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category', 'attribute').prefetch_related('image_set')
        category_id = self.kwargs.get('category_id')  # Get category_id from kwargs
        if category_id:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(category_id=category_id)
            except ValueError:
                # Handle invalid category_id (not an integer)
                pass 
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Add image URLs to the serialized data
        for product_data in serializer.data:
            product_id = product_data['id']
            product = Product.objects.get(id=product_id)
            image_urls = [request.build_absolute_uri(image.image_path.url) for image in product.image_set.all()]
            product_data['images'] = image_urls

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Add image URLs to the serialized data
        image_urls = [request.build_absolute_uri(image.image_path.url) for image in instance.image_set.all()]
        data = serializer.data
        data['images'] = image_urls

        return Response(data)

from django.contrib.auth.hashers import check_password
from django.db.models import Q # Import Q from django.db.models
class CustomerLoginView(APIView):
    def post(self, request):
        # username = request.data.get('username')
        identifier = request.data.get('identifier')  # Nhận giá trị từ trường 'identifier'
        password = request.data.get('password')

        # Tìm kiếm người dùng dựa trên username hoặc email
        try:
            user = Customer.objects.get(Q(username=identifier) | Q(email=identifier))
        except Customer.DoesNotExist:
            return Response({'message': 'Tài khoản hoặc mật khẩu không đúng'}, status=401)

        if not user.is_active:
            return Response({
                'message': "Tài khoản của bạn bị tạm khóa,\n vui lòng liên hệ qua mail <b>hongducct23@gmail.com</b> để được mở khóa"
            }, 403)  # Forbidden

        if not check_password(password, user.password):
            return Response({'message': 'Tài khoản hoặc mật khẩu không đúng'}, status=401)  # Unauthorized

        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = CustomerSerializer(user)
        return Response({
            'message': 'Login successful',
            'user': user_serializer.data,
            'token': token.key
        }, 200)

class CustomerRegisterView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            # Lưu người dùng mới vào cơ sở dữ liệu
            user = serializer.save()

            # Tạo token cho người dùng mới
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=201)  # Created
        else:
            return Response(serializer.errors, status=400)  # Bad Request
        
# CustomerLogoutView
class CustomerLogoutView(APIView):
    def post(self, request):
        # Xóa token của người dùng
        request.user.auth_token.delete()
        return Response({'message': 'Đăng xuất thành công'}, status=200)

# edit profile
class CustomerUpdateView(APIView):
    def put(self, request, pk):  # pk là ID của Customer cần cập nhật
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data, partial=True)  # partial=True cho phép cập nhật một phần
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# change password
class CustomerChangePasswordView(APIView):
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        print("Received data:", request.data)

        serializer = ChangePasswordSerializer(data=request.data)
        print("Serializer is valid:", serializer.is_valid())
        if serializer.is_valid():

            # Kiểm tra mật khẩu cũ
            if not authenticate(username=customer.username, password=serializer.validated_data['oldPassword']):
                return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)

            # Đặt mật khẩu mới và cập nhật hash mật khẩu trong phiên làm việc
            customer.set_password(serializer.validated_data['newPassword'])
            customer.save()
            update_session_auth_hash(request, customer)  # Quan trọng để phiên làm việc không bị hết hạn

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


# class ImageUploadView(APIView):
#     def post(self, request):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.core.files.storage import default_storage
class ImageUploadView(APIView):
    def post(self, request, format=None):
        image = request.FILES.get('file') 

        if image is None:
            return Response({'error': 'Không có tệp ảnh được cung cấp'}, status=status.HTTP_400_BAD_REQUEST)

        # Lưu trữ ảnh tạm thời
        file_name = default_storage.save(image.name, image)
        image_url = default_storage.url(file_name)

        return Response({'image_url': image_url}, status=status.HTTP_201_CREATED)

class CustomerAddressList(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user_id = self.request.user.id 
        return Address.objects.filter(user_id=user_id)

class CreateAddressView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class UpdateAddressView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        address_id = self.kwargs['address_id']
        return Address.objects.get(id=address_id)

class DeleteAddressView(generics.DestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        address_id = self.kwargs['address_id']
        return Address.objects.get(id=address_id)

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [permissions.IsAuthenticated]

class CustomerOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id  # Lấy ID của người dùng đã đăng nhập
        return Order.objects.filter(user_id=user_id).order_by('-order_date')  # Sắp xếp theo order_date giảm dần

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = Order.objects.prefetch_related(
            Prefetch('order_items__product__image_set', to_attr='prefetched_images')
        ).get(pk=self.kwargs['pk'])
        return obj

class ContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

































# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes = F("votes") + 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})