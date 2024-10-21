<template>
  <div
    v-if="showPasswordModal"
    class="fixed inset-0 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-lg p-6 shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Đổi mật khẩu</h2>
      <p v-if="errors" class="text-red-500 text-xs italic">
        {{ errors.password }}
      </p>
      <div class="mb-4">
        <label class="block mb-2">Mật khẩu cũ</label>
        <div class="mt-2">
          <a-input-password
            v-model:value="oldPassword"
            required=""
            placeholder="Nhập mật khẩu cũ"
            class="border flex block w-full rounded-md py-1.5 p-2 text-gray-900 shadow ring-1 ring-inset ring-gray-300 
            placeholder:text-white focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="mb-4">
        <label class="block mb-2">Mật khẩu mới</label>
        <div class="mt-2">
          <a-input-password
            v-model:value="newPassword"
            required=""
            placeholder="Nhập mật khẩu mới"
            class="border flex block w-full rounded-md py-1.5 p-2 text-gray-900 shadow ring-1 ring-inset ring-gray-300 placeholder:text-white focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="mb-4">
        <label class="block mb-2">Xác nhận mật khẩu mới</label>
        <div class="mt-2">
          <a-input-password
            v-model:value="confirmNewPassword"
            required=""
            placeholder="Xác nhận mật khẩu mới"
            class="border flex block w-full rounded-md py-1.5 p-2 text-gray-900 shadow ring-1 ring-inset ring-gray-300 placeholder:text-white focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          />
        </div>
      </div>
      <div class="flex justify-end">
        <button
          class="bg-blue-500 text-white px-4 py-2 rounded-md mr-2"
          @click="updatePassword"
        >
          Lưu
        </button>
        <button
          class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md"
          @click="emit('update:showPasswordModal', false)"
        >
          Đóng
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
const apiUrl = inject("apiUrl");
// Khai báo user là một reactive object
const user = ref(JSON.parse(localStorage.getItem("user")));

const props = defineProps({
  showPasswordModal: Boolean,
  errors: Object, 
});

const emit = defineEmits(["update:showPasswordModal", "updatePassword"]);

const oldPassword = ref("");
const newPassword = ref("");
const confirmNewPassword = ref("");

const updatePassword = () => {
  // Kiểm tra mật khẩu mới và xác nhận mật khẩu mới trùng khớp
  if (newPassword.value !== confirmNewPassword.value) {
    alert("Mật khẩu mới và xác nhận mật khẩu mới không trùng khớp");
    return;
  }

  axios.put(`${apiUrl}/customers/${user.value.id}/change-password/`, {
    oldPassword: oldPassword.value,  // Sửa lỗi chính tả ở đây
    newPassword: newPassword.value,  // Sửa lỗi chính tả ở đây
  })
  .then(() => {
    // Cập nhật mật khẩu thành công, đóng modal và emit sự kiện
    emit("updatePassword"); 
    oldPassword.value = "";
    newPassword.value = "";
    confirmNewPassword.value = "";
    if (props.errors) {
      props.errors.password = null; // Xóa thông báo lỗi nếu có
    }
    emit("update:showPasswordModal", false);
  })
  .catch(error => {
    // Xử lý lỗi, có thể hiển thị thông báo lỗi cho người dùng nhưng không đóng modal
    console.error('Lỗi khi cập nhật mật khẩu:', error);
    props.errors.password = error.response?.data?.error || 'Đã xảy ra lỗi khi cập nhật mật khẩu'; 
  });
};
</script>

<style scoped>
</style>

