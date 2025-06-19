<template>
  <nav class="navbar">
    <div class="navbar-left">
      <RouterLink to="/" exact-active-class="active-link">Главная</RouterLink>
      <RouterLink to="/subjects" exact-active-class="active-link">Предметы</RouterLink>
      <RouterLink to="/tests" exact-active-class="active-link">Тесты</RouterLink>
      <RouterLink to="/media" exact-active-class="active-link">Медиа</RouterLink>
    </div>
    <div class="navbar-right">
      <RouterLink :to="profileRoute" exact-active-class="active-link">Профиль</RouterLink>
      <button @click="logout" class="logout-btn">Выйти</button>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  router.push('/login')
}

const profileRoute = computed(() => {
  const role = localStorage.getItem('role')
  if (role === 'admin') return '/profile/admin'
  if (role === 'teacher') return '/profile/teacher'
  return '/profile/student'
})
</script>

<style scoped>
.navbar,
.navbar *,
.navbar a,
.navbar .router-link-active,
.navbar .active-link,
.navbar .logout-btn {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.01em;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.7rem 2rem;
  background: #22223b;
  border-bottom: 3px solid #9a8c98;
  box-sizing: border-box;
}

.navbar-left,
.navbar-right {
  display: flex;
  gap: 1.5rem;
}

a, .router-link-active {
  color: #f2e9e4;
  text-decoration: none;
  font-size: 1.08rem;
  transition: none;
  border-radius: 4px;
  padding: 0.3rem 0.8rem;
  border: 2px solid transparent;
}

.active-link {
  border: 2px solid #9a8c98;
  background: #4a4e69;
}

.logout-btn {
  background: none;
  border: none;
  color: #f2e9e4;
  font-size: 1rem;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  transition: background 0.2s;
}
.logout-btn:hover {
  background: #9a8c98;
  color: #22223b;
}
</style>