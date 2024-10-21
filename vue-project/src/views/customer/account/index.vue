<template>
  <h2>Thông tin tài khoản</h2>
  <div class="mr-12">
    <div class="flex bg-white rounded-lg">
      <div class="p-4 w-6/12">
        <span class="text-base">Thông tin cá nhân</span>
        <div class="mt-4">
          <form @submit.prevent="updateUser">
            <div class="flex">
              <div class="mr-4">
                <div
                  class="border-4 flex items-center rounded-full w-28 h-28 bg-sky-100 relative justify-center"
                >
                  <div class="">
                    <div class="flex items-center cursor-pointer">
                      <img
                        :src="userImageUrl"
                        alt="avatar"
                        class="w-28 h-28 rounded-full object-cover"
                        @click="changeAvatar"
                      />
                      <div
                        class="absolute flex w-4 h-4 rounded-full justify-center items-center"
                        style="
                          background-color: rgb(100, 100, 109);
                          right: 3px;
                          bottom: 5px;
                        "
                      >
                        <img
                          src="https://frontend.tikicdn.com/_desktop-next/static/img/account/edit.png"
                          class="w-3 h-3"
                          alt="edit icon"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="w-full flex justify-between flex-col">
                <div class="mb-4 flex items-center">
                  <label class="mr-4 w-24">Họ &amp; Tên</label>
                  <div class="flex">
                    <div class="">
                      <input
                        class="input rounded border-2 p-2"
                        type="search"
                        name="fullName"
                        maxlength="128"
                        placeholder="Thêm họ tên"
                        v-model="user.name"
                      />
                    </div>
                  </div>
                </div>
                <div class="mb-4 flex items-center">
                  <label class="mr-4 w-24">Username</label>
                  <div class="relative"> <div class="">
                      <input
                        class="input rounded border-2 p-2"
                        name="userName"
                        maxlength="128"
                        placeholder="Thêm username"
                        type="search"
                        v-model="user.username"
                      />
                      <p 
                        v-if="errors.username" 
                        class="absolute text-red-500 text-xs italic top-full left-0"
                      >
                        {{ errors.username }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="mb-4 flex items-center">
              <label class="mr-4 w-28">&nbsp;</label>
              <button
                type="submit"
                class="w-44 h-10 rounded border-2 bg-blue-500 text-white"
              >
                Lưu thay đổi
              </button>
            </div>
          </form>
        </div>
      </div>
      <div class="border-x my-4"></div>
      <div class="flex flex-col p-4 space-y-4 w-full">
        <span class="font-bold text-lg">Email</span>
        <div class="space-y-4">
          <div class="py-3 flex items-center justify-between border-y">
            <div class="flex items-center space-x-4">
              <img
                src="https://frontend.tikicdn.com/_desktop-next/static/img/account/email.png"
                class="w-6 h-6"
                alt="Email icon"
              />
              <div class="flex flex-col">
                <span class="font-medium">Địa chỉ email</span>
                <span>{{ user.email }}</span>
              </div>
            </div>
            <button
              class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
              @click="changeEmail"
            >
              Cập nhật
            </button>
          </div>
        </div>

        <span class="font-bold text-lg">Bảo mật</span>
        <div class="space-y-4">
          <div class="py-3 flex items-center justify-between border-y">
            <div class="flex items-center space-x-4">
              <img
                src="https://frontend.tikicdn.com/_desktop-next/static/img/account/lock.png"
                class="w-6 h-6"
                alt="Lock icon"
              />
              <span class="font-medium">Đổi mật khẩu</span>
            </div>
            <button
              class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
              @click="changePassword"
            >
              Cập nhật
            </button>
          </div>
        </div>
        <EmailModal
          v-model:showEmailModal="showEmailModal"
          @updateEmail="handleUpdateEmail"
          :errors="errors"
        />
        <PasswordModal
          v-model:showPasswordModal="showPasswordModal"
          @updatePassword="handleUpdatePassword"
          :errors="errors"
        />
        <span class="font-bold text-lg">Liên kết mạng xã hội</span>
        <div class="space-y-4">
          <div class="py-3 flex items-center justify-between border-y">
            <div class="flex items-center space-x-4">
              <img
                src="https://frontend.tikicdn.com/_desktop-next/static/img/account/facebook.png"
                class="w-6 h-6"
                alt="Facebook icon"
              />
              <span class="font-medium">Facebook</span>
            </div>
            <button
              class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
            >
              Liên kết
            </button>
          </div>
          <div class="py-3 flex items-center justify-between border-y">
            <div class="flex items-center space-x-4">
              <img
                src="https://frontend.tikicdn.com/_desktop-next/static/img/account/google.png"
                class="w-6 h-6"
                alt="Google icon"
              />
              <span class="font-medium">Google</span>
            </div>
            <button
              class="bg-green-500 text-white px-4 py-2 rounded-md cursor-not-allowed"
            >
              Đã liên kết
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, inject, watch, computed } from "vue";
import axios from "axios";

import EmailModal from "./EmailModal.vue";
import PasswordModal from './PasswordModal.vue';

import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const showEmailModal = ref(false);
const showPasswordModal = ref(false);

const changeEmail = () => {
  showEmailModal.value = true;
};

const handleUpdateEmail = async (newEmail) => {
  try {
    // Cập nhật email của user
    user.value.email = newEmail;
    toast(`Đã cập nhật thành công!`, {
      autoClose: 3000,
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
    });
  }
  catch(error) {
    console.log("error: ", error);
    errors.value = error.response.data;
    if (error.response) {
      console.log(error.response.data); // Hiển thị lỗi từ server
    } else if (error.request) {
      console.error("Request error:", error.request);
    } else {
      console.error("Request setup error:", error.message);
    }
  };
};

const changePassword = () => {
  showPasswordModal.value = true;
};

const handleUpdatePassword = () => {
  try {
    // Xử lý phản hồi từ API (nếu cần)
    toast(`Đã cập nhật thành công!`, {
      autoClose: 3000,
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
    });
  } catch (error) {
    console.log("error: ", error);
    errors.value = error.response.data;
    if (error.response) {
      console.log(error.response.data); // Hiển thị lỗi từ server
    } else if (error.request) {
      console.error("Request error:", error.request);
    } else {
      console.error("Request setup error:", error.message);
    }
  }
};

const apiUrl = inject("apiUrl");
const baseURL = "http://127.0.0.1:8000/";

// Khai báo user là một reactive object
const user = ref(JSON.parse(localStorage.getItem("user")));

// Computed property để lấy đường dẫn ảnh đại diện
const userImageUrl = computed(() => {
  return user.value.avatar ? `${baseURL}${user.value.avatar}` : "";
});

// Watch sự thay đổi của user để lưu vào localStorage
watch(
  user,
  (newValue) => {
    localStorage.setItem("user", JSON.stringify(newValue));
  },
  { deep: true }
);

const changeAvatar = async () => {
  try {
    const file = await openImageFileDialog();

    if (file) {
      const formData = new FormData();
      formData.append("avatar", file); // Gửi trực tiếp file ảnh
      formData.append("name", user.value.name); // Gửi kèm các thông tin khác nếu cần
      formData.append("username", user.value.username);

      // Gửi yêu cầu PUT để cập nhật thông tin người dùng, bao gồm cả avatar
      const response = await axios.put(
        `${apiUrl}/customers/${user.value.id}/`, 
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Cập nhật user.value với dữ liệu mới từ server
      console.log("xx",response.data);
      user.value = response.data; 
      toast(`Đã cập nhật thành công!`, {
        autoClose: 3000,
        theme: "auto",
        type: "success",
        dangerouslyHTMLString: true,
      });
    }
  } catch (error) {
    console.error("Lỗi khi thay đổi ảnh đại diện:", error);
    // Xử lý lỗi ở đây, ví dụ: hiển thị thông báo lỗi cho người dùng
  }
};

const openImageFileDialog = async () => {
  return new Promise((resolve, reject) => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.addEventListener("change", () => {
      const file = input.files[0];
      resolve(file);
    });
    input.click();
  });
};

const errors = ref([]);
const updateUser = async () => {
  try {
    const response = await axios.put(`${apiUrl}/customers/${user.value.id}/`, {
      name: user.value.name,
      username: user.value.username,
    });
    errors.value = [];
    console.log(response.data);

    // Thông báo thành công
    // alert("Cập nhật thông tin thành công!");
    toast(`Đã cập nhật thành công!`, {
      autoClose: 3000,
      theme: "auto",
      type: "success",
      dangerouslyHTMLString: true,
    });
    
    // Cập nhật các thuộc tính tương ứng của user.value
    user.value.name = response.data.name;
    user.value.username = response.data.username;
    localStorage.setItem("user", JSON.stringify(user.value));
  }
  catch(error) {
    console.log("error: ", error);
    errors.value = error.response.data;
    if (error.response) {
      console.log(error.response.data); // Hiển thị lỗi từ server
    } else if (error.request) {
      console.error("Request error:", error.request);
    } else {
      console.error("Request setup error:", error.message);
    }
  };
};
</script>
