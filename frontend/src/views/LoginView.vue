<template>
  <div class="login-wrapper">
    <main class="login-page">
      <h1>Вход</h1>
      <form @submit.prevent="login">
        <div>
          <label for="login">Логин:</label>
          <input id="login" v-model="loginValue" required />
        </div>
        <div>
          <label for="password">Пароль:</label>
          <input id="password" type="password" v-model="passwordValue" required />
        </div>
        <button type="submit">Войти</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const loginValue = ref('')
const passwordValue = ref('')
const error = ref('')
const router = useRouter()

async function login() {
  error.value = ''
  try {
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        username: loginValue.value,
        password: passwordValue.value
      })
    })
    const data = await response.json()
    if (response.ok && data.access_token) {
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('role', data.role)
      // После входа — на главную
      router.push('/')
    } else {
      error.value = data.detail || 'Ошибка входа'
    }
  } catch (e) {
    error.value = 'Ошибка соединения с сервером'
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f2e9e4;
}

.login-page {
  width: 300px;
  min-height: 350px;
  padding: 2.2rem 1.5rem 1.5rem 1.5rem;
  background: #4a4e69;
  border-radius: 14px;
  color: #f2e9e4;
  box-shadow: 0 4px 24px rgba(34, 34, 59, 0.18);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
h1 {
  margin-bottom: 1.2rem;
  color: #f2e9e4;
}
label {
  display: block;
  margin-bottom: 0.3rem;
  color: #f2e9e4;
}
input {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1.1rem;
  border: 1px solid #c9ada7;
  border-radius: 4px;
  background: #22223b;
  color: #f2e9e4;
  font-size: 1rem;
}
input:focus {
  outline: none;
  border-color: #9a8c98;
  background: #22223b;
}
button {
  width: 100%;
  padding: 0.7rem;
  background: #9a8c98;
  color: #22223b;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1.08rem;
  margin-top: 0.5rem;
  transition: background 0.2s;
}
button:hover {
  background: #c9ada7;
  color: #22223b;
}
.error {
  color: #bb0a21;
  margin-top: 0.7rem;
  text-align: center;
}
</style>