<template>
  <div class="results-teacher-view">
    <section class="results-section">
      <h2>Результаты по классам</h2>
      <div class="filters-row">
        <select v-model="selectedSubject" @change="fetchThemes" class="form-select">
          <option value="">Выберите предмет</option>
          <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.subject_name }}</option>
        </select>
        <select v-model="selectedTheme" @change="fetchMaterials" :disabled="!selectedSubject" class="form-select">
          <option value="">Выберите тему</option>
          <option v-for="t in themes" :key="t.id" :value="t.id">{{ t.theme_name }}</option>
        </select>
        <select v-model="selectedMaterial" @change="fetchClasses" :disabled="!selectedTheme" class="form-select">
          <option value="">Выберите материал</option>
          <option v-for="m in materials" :key="m.id" :value="m.id">{{ m.title }}</option>
        </select>
        <select v-model="selectedClass" @change="fetchResults" :disabled="!selectedMaterial" class="form-select">
          <option value="">Выберите класс</option>
          <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.class_name }}</option>
        </select>
      </div>
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="results.length === 0 && selectedClass" class="empty">Нет результатов</div>
      <div v-else-if="results.length" class="table-wrapper">
        <table class="results-table">
          <thead>
            <tr>
              <th>Ученик</th>
              <th>Правильных</th>
              <th>Всего</th>
              <th>Процент</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in results" :key="res.user_id">
              <td>{{ res.full_name }}</td>
              <td>{{ res.correct_answers }}</td>
              <td>{{ res.total_questions }}</td>
              <td :class="{ low: res.percent < 50 }">{{ res.percent }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const subjects = ref([])
const themes = ref([])
const materials = ref([])
const classes = ref([])
const results = ref([])
const loading = ref(false)

const selectedSubject = ref('')
const selectedTheme = ref('')
const selectedMaterial = ref('')
const selectedClass = ref('')

async function fetchSubjects() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/subjects/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjects.value = await res.json()
  }
}

async function fetchThemes() {
  selectedTheme.value = ''
  selectedMaterial.value = ''
  selectedClass.value = ''
  themes.value = []
  materials.value = []
  classes.value = []
  results.value = []
  if (!selectedSubject.value) return
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/themes/by_subject/${selectedSubject.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    themes.value = await res.json()
  }
}

async function fetchMaterials() {
  selectedMaterial.value = ''
  selectedClass.value = ''
  materials.value = []
  classes.value = []
  results.value = []
  if (!selectedTheme.value) return
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/materials/by_theme/${selectedTheme.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    materials.value = await res.json()
  }
}

async function fetchClasses() {
  selectedClass.value = ''
  classes.value = []
  results.value = []
  if (!selectedMaterial.value) return
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/classes/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    classes.value = await res.json()
  }
}

async function fetchResults() {
  results.value = []
  if (!selectedClass.value || !selectedMaterial.value) return
  loading.value = true
  const token = localStorage.getItem('token')
  const res = await fetch(
    `http://localhost:8000/test_results/class?class_id=${selectedClass.value}&material_id=${selectedMaterial.value}`,
    { headers: { Authorization: `Bearer ${token}` } }
  )
  if (res.ok) {
    results.value = await res.json()
  }
  loading.value = false
}

onMounted(fetchSubjects)
</script>

<style scoped>
.results-teacher-view {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.results-section {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.12);
  padding: 2rem;
  margin-bottom: 2rem;
}

.results-section h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #f2e9e4;
  font-size: 1.5rem;
  font-weight: 600;
}

.filters-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.form-select {
  width: 100%;
  min-width: 170px;
  padding: 0.75rem;
  border: 1px solid #9a8c98;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #22223b;
  color: #f2e9e4;
}

.form-select:focus {
  outline: none;
  border-color: #4a4e69;
  box-shadow: 0 0 0 2px #4a4e6933;
}

.table-wrapper {
  margin-top: 2rem;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  background: #22223b;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(34,34,59,0.07);
}

.results-table th, .results-table td {
  border: 1px solid #9a8c98;
  padding: 0.75rem;
  text-align: center;
}

.results-table th {
  background-color: #4a4e69;
  color: #f2e9e4;
  font-weight: 500;
}

.results-table td {
  background-color: #22223b;
  color: #f2e9e4;
}

.results-table tr:nth-child(even) td {
  background-color: #2a2a42;
}

.low {
  color: #bb0a21;
  font-weight: bold;
}

.loading, .empty {
  text-align: center;
  color: #4a4e69;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .filters-row {
    flex-direction: column;
    gap: 1rem;
  }
  .form-select {
    width: 100%;
  }
}
</style>