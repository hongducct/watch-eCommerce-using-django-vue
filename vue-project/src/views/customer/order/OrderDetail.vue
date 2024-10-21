<template>
  <div v-if="order" class="bg-white rounded-lg shadow-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-xl font-bold">
        Chi tiết đơn hàng #{{ order.id }} -
        <span v-if="order.status">
          {{ orderStatusInfo(order.status.toString()).label }}
        </span>
        <span v-else> Trạng thái không xác định </span>
      </h1>
      <p class="text-gray-500 text-sm">
        Ngày đặt hàng: {{ new Date(order.order_date).toLocaleString() }}
      </p>
    </div>

    <div class="mb-4">
      <h3 class="text-lg font-semibold mb-2">THÔNG BÁO</h3>
      <div class="bg-yellow-100 p-4 rounded-lg">
        <p class="text-sm">
          Đơn hàng #{{ order.id }} đã sẵn sàng để giao đến quý khách. Chúng tôi
          vừa bàn giao đơn hàng của quý khách đến đối tác vận chuyển Giao Hang
          Nhanh. Đơn hàng sẽ được giao trước 23:59 ngày
        </p>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-4 mb-4">
      <div>
        <h3 class="text-lg font-semibold mb-2">ĐỊA CHỈ NGƯỜI NHẬN</h3>
        <p>{{ order.shipping_name }}</p>
        <p>
          Địa chỉ: {{ order.shipping_address }}, {{ order.shipping_ward }},
          {{ order.shipping_district }}, {{ order.shipping_province }}
        </p>
        <p>Điện thoại: {{ order.shipping_phone }}</p>
      </div>
      <div>
        <h3 class="text-lg font-semibold mb-2">HÌNH THỨC GIAO HÀNG</h3>
        <p>FAST Giao Tiết Kiệm</p>
        <!-- <p>Giao vào</p> -->
        <p>Được giao bởi TikiNOW Smart Logistics (giao từ Hà Nội)</p>
        <!-- <p>Phí vận chuyển: {{ order.shipping_fee || "22.000" }} ₫</p> -->
      </div>
      <div>
        <h3 class="text-lg font-semibold mb-2">HÌNH THỨC THANH TOÁN</h3>
        <p>Thanh toán tiền mặt khi nhận hàng</p>
      </div>
    </div>

    <h3 class="text-lg font-semibold mb-2">SẢN PHẨM</h3>
    <table class="w-full border-collapse mb-4">
      <thead>
        <tr>
          <th class="border p-2">Sản phẩm</th>
          <th class="border p-2">Giá</th>
          <th class="border p-2">Số lượng</th>
          <th class="border p-2">Giảm giá</th>
          <th class="border p-2">Tạm tính</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in order.order_items" :key="item.id">
          <td class="border p-2">
            <div class="flex items-center">
              <img
                :src="`http://127.0.0.1:8000/${item.product.images[0].image_path}`"
                alt="Product Image"
                class="w-20 h-20 object-cover mr-2"
              />
              <span>{{ item.product.name }}</span>
            </div>
            <!-- <p class="text-sm text-gray-500">
                Cung cấp bởi {{ item.product.seller }}
              </p> -->
            <p class="text-sm text-gray-500">Brand: {{ item.product.brand }}</p>
          </td>
          <td class="border p-2 text-right">{{ formatPrice(item.price) }}</td>
          <td class="border p-2 text-center">{{ item.quantity }}</td>
          <td class="border p-2 text-right">{{ item.discount || 0 }} ₫</td>
          <td class="border p-2 text-right">
            {{ formatPrice(item.price * item.quantity) }}
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex justify-end mb-4">
      <div class="flex flex-col text-right">
        <div class="mb-2">
          <span class="text-gray-500">Tạm tính:</span>
          <span class="font-medium">
            <!-- {{ order.total_amount - (order.shipping_fee || 22000) }} ₫ -->
            {{ formatPrice(order.total_amount) }}
          </span>
        </div>
        <div class="mb-2">
          <span class="text-gray-500">Phí vận chuyển:</span>
          <span class="font-medium">
            <!-- {{ order.shipping_fee || "22.000" }} ₫ -->
            0
          </span>
        </div>
        <div>
          <span class="text-gray-500">Tổng cộng:</span>
          <span class="font-medium"><b>{{ formatPrice(order.total_amount) }}</b></span>
        </div>
      </div>
    </div>

    <div class="flex justify-end">
      <button
        type="button"
        @click="handleAddToCart(order.order_items[0].product)"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2 text-sm"
      >
        Mua lại
      </button>
      <button
        class="bg-gray-300 hover:bg-gray-400 text-gray-700 font-bold py-2 px-4 rounded text-sm"
      >
        Chat với nhà bán
      </button>
    </div>
  </div>
  <div v-else>Loading...</div>
</template>

<script setup>
import { ref, onMounted, computed, inject } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import axios from "axios";
import {
  MagnifyingGlassIcon,
  DocumentTextIcon,
  ClockIcon,
  CheckIcon,
  TruckIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  ExclamationCircleIcon,
} from "@heroicons/vue/24/outline";

const apiUrl = inject("apiUrl");
const token = localStorage.getItem("token");
const router = useRouter();
const route = useRoute();
const orderId = route.params.id;
console.log("orderId:", orderId);
const order = ref({});

const orderStatusInfo = computed(() => {
  return (status) => {
    switch (status) {
      case "1":
        return { label: "Đang chờ xử lý / Chờ xác nhận", icon: ClockIcon };
      case "2":
        return { label: "Đã xác nhận", icon: CheckIcon };
      case "3":
        return { label: "Đang giao hàng", icon: TruckIcon };
      case "4":
        return { label: "Đã giao hàng", icon: CheckCircleIcon };
      case "5":
        return { label: "Hoàn thành", icon: CheckCircleIcon };
      case "6":
        return { label: "Đã hủy", icon: XCircleIcon };
      case "7":
        return { label: "Trả hàng / Hoàn tiền", icon: ArrowPathIcon };
      case "8":
        return { label: "Giao hàng thất bại", icon: ExclamationCircleIcon };
      default:
        return { label: "Không xác định", icon: "" };
    }
  };
});

const addToCart = inject("addToCart");

const quantity = ref(1);

const handleAddToCart = (product) => {
  console.log(order.value.order_items[0].product);
  if (quantity.value > product.stock) {
    alert(`Chỉ có thể thêm tối đa ${product.stock} sản phẩm vào giỏ hàng.`);
    return;
  }

  console.log("ok:", product);

  // Thực hiện các hành động khác (ví dụ: thêm sản phẩm vào giỏ hàng)
  const productToAdd = { ...product, quantity: quantity.value };
  addToCart(productToAdd);
  quantity.value = 1; // Reset quantity after adding to cart
};

const formatPrice = (price) => {
  // Thêm dấu chấm sau 3 số và thêm VNĐ
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "VND",
    minimumFractionDigits: 0,
  }).format(price);
}

onMounted(async () => {
  try {
    const response = await axios.get(`${apiUrl}/orders/${orderId}/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    console.log("response order detail:", response.data);
    order.value = response.data;
    console.log("x", order.value);
  } catch (error) {
    console.error("Error fetching order details:", error);
    // Handle error appropriately (e.g., display an error message)
  }
});

// ... (orderStatusInfo computed property remains the same)
</script>
