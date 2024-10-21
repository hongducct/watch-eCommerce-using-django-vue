import { ref } from 'vue';
// localStorage.removeItem('token');
// localStorage.removeItem('user');
// useAuth.js
const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true');

const setIsLoggedIn = (value) => {
  isLoggedIn.value = value;
  localStorage.setItem('isLoggedIn', value.toString());
};
// setIsLoggedIn(false);
export { isLoggedIn, setIsLoggedIn };