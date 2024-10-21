<template>
  <div v-if="showEmailModal" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 shadow-lg">
      <h2 class="text-lg font-bold mb-4">Cập nhật email</h2>
      <input
        v-model="newEmail"
        type="email"
        class="border rounded-md p-2 mb-4 w-full"
        placeholder="Nhập email mới"
      />
      <p v-if="errors.email" class="text-red-500 text-xs italic">
        {{ errors.email }}
      </p>
      <div class="flex justify-end">
        <button
          class="bg-blue-500 text-white px-4 py-2 rounded-md mr-2"
          @click="updateEmail"
        >
          Lưu
        </button>
        <button
          class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md"
          @click="closeEmailModal"
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
  showEmailModal: Boolean,
  errors: Object, // Nhận prop errors
});

const emit = defineEmits(['update:showEmailModal', 'updateEmail']);

const newEmail = ref('');

const updateEmail = () => {
  axios.put(`${apiUrl}/customers/${user.value.id}/`, {
    email: newEmail.value,
  })
  .then(() => {
      // Cập nhật email thành công
      emit('updateEmail', newEmail.value); // Emit sự kiện cập nhật email
      newEmail.value = ''; 
      props.errors.email = null; // Xóa thông báo lỗi nếu có
      emit('update:showEmailModal', false);
    })
    .catch(error => {
      // Xử lý lỗi, có thể hiển thị thông báo lỗi cho người dùng nhưng không đóng modal
      console.error('Lỗi khi cập nhật email:', error);
      props.errors.email = error.response?.data?.email || 'Đã xảy ra lỗi khi cập nhật email'; 
    });
};

const closeEmailModal = () => {
  emit('update:showEmailModal', false);
}
</script>