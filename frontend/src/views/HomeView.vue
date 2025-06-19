<template>
  <main class="centered">
    <h1>Главная страница</h1>
    <p>Добро пожаловать на образовательную платформу!</p>
    <div class="search-block">
      <input
        v-model="query"
        @input="onSearch"
        type="text"
        class="search-input"
        placeholder="Поиск по предметам, темам, материалам, тестам..."
        @keydown.enter.prevent="onEnter"
      />
      <ul v-if="results.length && query" class="search-results">
        <li
          v-for="item in results"
          :key="item.type + '-' + item.id"
          @mousedown.prevent="goToItem(item)"
          class="search-result"
        >
          <span class="type">{{ typeLabel(item.type) }}:</span>
          <span class="title">{{ item.title }}</span>
        </li>
      </ul>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const query = ref('')
const results = ref([])
const router = useRouter()

function typeLabel(type) {
  switch (type) {
    case 'subject': return 'Предмет'
    case 'theme': return 'Тема'
    case 'material': return 'Материал'
    case 'test': return 'Тест'
    case 'media': return 'Медиа'
    default: return ''
  }
}

async function onSearch() {
  const q = query.value.trim()
  if (!q) {
    results.value = []
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/search/all?q=${encodeURIComponent(q)}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    results.value = await res.json()
  } else {
    results.value = []
  }
}

// Для перехода по Enter к первому результату
function onEnter() {
  if (results.value.length) {
    goToItem(results.value[0])
  }
}

function goToItem(item) {
  if (item.type === 'subject') {
    router.push(`/subjects/${item.id}/themes`)
  } else if (item.type === 'theme') {
    router.push(`/themes/${item.id}/materials`)
  } else if (item.type === 'material') {
    router.push(`/materials/${item.id}`)
  } else if (item.type === 'test') {
    router.push(`/tests/pass/${item.id}`)
  } else if (item.type === 'media') {
    // Переход на просмотр медиа для материала
    router.push(`/media/material/${item.material_id}`)
  }
  results.value = []
  query.value = ''
}
</script>

<style scoped>
.centered {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
h1 {
  font-size: 2.2rem;
  margin-bottom: 1.2rem;
  color: #22223b;
}
p {
  font-size: 1.25rem;
  color: #4a4e69;
  text-align: center;
}
.search-block {
  margin-top: 2.5rem;
  width: 100%;
  max-width: 700px;
  position: relative;
}
.search-input {
  width: 100%;
  padding: 1.2rem 1.5rem;
  border-radius: 16px;
  border: 2.5px solid #4a4e69;
  font-size: 1.25rem;
  background: #fff;
  color: #22223b;
  outline: none;
  transition: border 0.18s, box-shadow 0.18s;
  box-shadow: 0 4px 24px rgba(74, 78, 105, 0.08);
  font-weight: 500;
}
.search-input:focus {
  border-color: #bb0a21;
  box-shadow: 0 6px 32px rgba(187,10,33,0.10);
  background: #f2e9e4;
}
.search-results {
  position: absolute;
  left: 0;
  right: 0;
  top: 110%;
  background: #fff;
  border: 2px solid #c9ada7;
  border-radius: 0 0 16px 16px;
  box-shadow: 0 8px 32px rgba(34,34,59,0.13);
  z-index: 10;
  max-height: 320px;
  overflow-y: auto;
  margin: 0;
  padding: 0;
  list-style: none;
}
.search-result {
  padding: 1.1rem 1.5rem;
  cursor: pointer;
  display: flex;
  gap: 0.7rem;
  align-items: center;
  transition: background 0.15s;
  font-size: 1.13rem;
  font-weight: 500;
}
.search-result:hover {
  background: #f2e9e4;
}
.type {
  color: #4a4e69;
  font-weight: 600;
}
.title {
  color: #22223b;
}
</style>