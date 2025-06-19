<template>
  <div class="results-view">
    <h2>Мои результаты тестов</h2>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="results.length === 0" class="empty">Нет результатов</div>
    <table v-else class="results-table">
      <thead>
        <tr>
          <th>Предмет</th>
          <th>Тема</th>
          <th>Материал</th>
          <th>Тест</th>
          <th>Всего</th>
          <th>Правильных</th>
          <th>Процент</th>
          <th>Дата</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="res in results" :key="res.id">
          <td>{{ res.subject_name }}</td>
          <td>{{ res.theme_name }}</td>
          <td>{{ res.material_title }}</td>
          <td>{{ res.test_title }}</td>
          <td>{{ res.total_questions }}</td>
          <td>{{ res.correct_answers }}</td>
          <td>{{ res.percent }}%</td>
          <td>{{ formatDate(res.passed_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const results = ref([])
const loading = ref(true)

function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleString('ru-RU')
}

onMounted(async () => {
  loading.value = true
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/test_results/my', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    results.value = await res.json()
  } else {
    results.value = []
  }
  loading.value = false
})
</script>

<style scoped>
.results-view {
  padding: 2rem;
}
h2 {
  color: #22223b;
  margin-bottom: 2rem;
  text-align: center;
}
.results-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(34,34,59,0.07);
}
.results-table th, .results-table td {
  padding: 0.7rem 1rem;
  border: 1px solid #c9ada7;
  text-align: center;
}
.results-table th {
  background: #4a4e69;
  color: #fff;
}
.loading, .empty {
  text-align: center;
  color: #4a4e69;
  margin-top: 2rem;
}
</style>