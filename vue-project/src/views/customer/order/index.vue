<template>
  <h1 class="text-xl font-bold mt-4">Đơn hàng của tôi</h1>
  <div
    class="flex flex-col bg-white w-11/12 rounded-lg shadow-lg relative mt-4"
  >
    <div class="p-4">
      <div class="flex justify-between border-b pb-2 mb-4">
        <ul class="flex space-x-4 text-center">
          <li
            v-for="(status, index) in orderStatuses"
            :key="status.value"
            :class="{
              'font-medium text-blue-500 border-b-2 border-blue-500 pb-1.5 text-center':
                currentStatus === status.value,
            }"
            @click="handleStatusClick(status.value, index)"
          >
            <span class="text-gray-500 hover:text-gray-700 cursor-pointer">
              {{ status.label }}
            </span>
          </li>
        </ul>
      </div>

      <div class="flex items-center border rounded-l">
        <MagnifyingGlassIcon class="ml-4 h-6 w-6 text-gray-500" />
        <input
          type="text"
          v-model="searchTerm"
          placeholder="Tìm đơn hàng theo Mã đơn hàng, Brand hoặc Tên sản phẩm"
          class="px-3 py-2 w-full focus:outline-none border-none outline-none"
        />
        <button
          class="bg-blue-500 w-36 py-2 hover:bg-blue-700 text-white text-sm font-bold rounded-lg"
        >
          Tìm đơn hàng
        </button>
      </div>
    </div>

    <main class="px-4">
      <div
        v-for="order in filteredOrders"
        :key="order.id"
        class="border-b py-4"
      >
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center">
            <component
              :is="orderStatusInfo(order.status.toString()).icon"
              class="w-5 h-5 mr-2"
            />
            <span class="font-medium">
              {{ orderStatusInfo(order.status.toString()).label }}
            </span>
          </div>
          <span class="text-gray-500 text-sm">{{
            new Date(order.order_date).toLocaleString()
          }}</span>
        </div>

        <div
          v-for="orderItem in order.order_items"
          :key="orderItem.id"
          class="flex items-center mb-2"
        >
          <img
            :src="orderItem.product.images[0]"
            alt="Product Image"
            class="w-20 h-20 object-cover mr-4"
          />
          <div>
            <h4 class="font-medium">{{ orderItem.product.name }}</h4>
            <p class="text-gray-500 text-sm">{{ orderItem.product.brand }}</p>
            <p class="text-gray-500 text-sm">x{{ orderItem.quantity }}</p>
          </div>
          <div class="ml-auto font-medium">
            {{ formatPrice(orderItem.price) }}
          </div>
        </div>

        <div class="mt-2 flex justify-end">
          <div class="text-gray-500 text-sm mr-4">
            Tổng tiền: {{ formatPrice(order.total_amount) }}
          </div>
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded mr-2 text-sm"
          >
            Mua lại
          </button>
          <router-link
            :to="`/orders/${order.id}`"
            class="text-blue-500 hover:text-blue-700 text-sm"
          >
            Xem chi tiết
          </router-link>
        </div>
      </div>

      <div
        v-if="filteredOrders.length === 0"
        class="flex flex-col items-center justify-center flex-grow py-28"
      >
        <div class="flex items-center">
          <MagnifyingGlassIcon class="w-32 h-32 text-gray-300" />
          <DocumentTextIcon
            class="w-10 h-10 text-gray-300 absolute left-1/2 transform -translate-x-1/2 -translate-y-1/2"
          />
        </div>
        <h1 class="text-2xl font-bold mt-4 mb-2">Chưa có đơn hàng</h1>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, inject, watch } from "vue";
import { useRouter, useRoute } from "vue-router"; // Import useRoute
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
const route = useRoute(); // Get the current route
const currentStatus = ref(route.params.status || "all"); // Get status from route params or default to 'all'
// Sử dụng query params thay vì route params để lưu trữ trạng thái lọc
// const currentStatus = ref(route.query.status || "all");
const order = ref([]);
const orders = ref([]);

const fetchOrder = async () => {
  try {
    const response = await axios.get(`${apiUrl}/customer-orders/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    order.value = response.data;

    // Lặp qua từng đơn hàng và lấy thông tin sản phẩm
    for (const orderItem of order.value) {
      const orderWithProducts = { ...orderItem }; // Sao chép đơn hàng
      orderWithProducts.order_items = []; // Tạo một mảng mới để lưu trữ thông tin sản phẩm

      for (const item of orderItem.order_items) {
        try {
          const productResponse = await axios.get(
            `${apiUrl}/product/${item.product_id}/`
          );
          const productData = productResponse.data;
          orderWithProducts.order_items.push({ ...item, product: productData });
        } catch (error) {
          console.error("Error fetching product:", error);
          // Xử lý lỗi ở đây, ví dụ: thêm một đối tượng sản phẩm mặc định với thông báo lỗi
          orderWithProducts.order_items.push({
            ...item,
            product: { error: "Không thể lấy thông tin sản phẩm" },
          });
        }
      }

      orders.value.push(orderWithProducts);
    }

    console.log("orders: ", orders.value);
  } catch (error) {
    console.error(error);
  }
};

const orderStatuses = ref([
  { label: "Tất cả đơn", value: "all" },
  { label: "Đang chờ xử lý / Chờ xác nhận", value: "1" },
  { label: "Đã xác nhận", value: "2" },
  { label: "Đang giao hàng", value: "3" },
  { label: "Đã giao hàng", value: "4" },
  { label: "Hoàn thành", value: "5" },
  { label: "Đã hủy", value: "6" },
  { label: "Trả hàng / Hoàn tiền", value: "7" },
  { label: "Giao hàng thất bại", value: "8" },
]);

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

// const filteredOrders = computed(() => {
  //   if (currentStatus.value === "all") {
    //     return orders.value;
    //   } else {
      //     // Lọc đơn hàng dựa trên status (chú ý chuyển đổi order.status thành kiểu chuỗi để so sánh)
      //     return orders.value.filter(
        //       (order) => String(order.status) === currentStatus.value
        //     );
        //   }
        // });
const searchTerm = ref(''); // Biến để lưu trữ từ khóa tìm kiếm

// Tính toán danh sách đơn hàng đã lọc dựa trên từ khóa tìm kiếm và trạng thái hiện tại
const filteredOrders = computed(() => {
  // Nếu không có từ khóa tìm kiếm, lọc chỉ dựa trên trạng thái
  console.log(searchTerm.value)
  if (searchTerm.value.trim() === '') {
    if (currentStatus.value === "all") {
      return orders.value;
    } else {
      return orders.value.filter(
        (order) => order.status.toString() === currentStatus.value
      );
    }
  }

  // Nếu có từ khóa tìm kiếm, lọc dựa trên cả trạng thái và từ khóa
  const lowerCaseSearchTerm = searchTerm.value.toLowerCase();
  return orders.value.filter((order) => {
    // Kiểm tra trạng thái đơn hàng
    const statusMatch = currentStatus.value === "all" || order.status.toString() === currentStatus.value;

    // Kiểm tra từ khóa tìm kiếm trong mã đơn hàng, brand, hoặc tên sản phẩm
    const searchMatch =
      String(order.id).toLowerCase().includes(lowerCaseSearchTerm) ||
      order.order_items.some(item =>
        item.product.brand.toLowerCase().includes(lowerCaseSearchTerm) ||
        item.product.name.toLowerCase().includes(lowerCaseSearchTerm)
      );
    console.log(statusMatch, searchMatch)

    return statusMatch && searchMatch; 
  });
});

console.log("filteredOrders: ", filteredOrders.value);
        
const handleStatusClick = (status, index) => {
  currentStatus.value = status;
  router.push({ name: "customer-order", params: { status } });
  //   Sử dụng query params thay vì route params
  //   router.push({ name: "customer-order", query: { status } });
};



const formatPrice = (price) => {
  // Thêm dấu chấm sau 3 số và thêm VNĐ
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "VND",
    minimumFractionDigits: 0,
  }).format(price);
};

// Theo dõi sự thay đổi của route params và cập nhật currentStatus
watch(
  () => route.params.status,
  (newStatus) => {
    // Chuyển đổi newStatus thành kiểu chuỗi nếu cần
    currentStatus.value = newStatus ? String(newStatus) : "all";
  }
);
// // Theo dõi sự thay đổi của query params và cập nhật currentStatus
// watch(
//   () => route.query.status,
//   (newStatus) => {
//     currentStatus.value = newStatus || "all";
//   }
// );

fetchOrder();
</script>
