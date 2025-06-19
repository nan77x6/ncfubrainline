<template>
  <div class="theme-management">
    <!-- 1. Создать новую тему -->
    <section class="theme-mgmt-section">
      <h2>Создать новую тему</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="createSubjectId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <input v-model="createThemeName" placeholder="Название темы" class="form-input" />
        </div>
        <button @click="createTheme" class="action-btn">Добавить</button>
      </div>
      <div v-if="createResult" class="result-message">{{ createResult }}</div>
    </section>

    <!-- 2. Изменить тему -->
    <section class="theme-mgmt-section">
      <h2>Изменить тему</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="editSubjectId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="editThemeId" @focus="fetchThemesForEdit" class="form-select">
            <option disabled value="">Выберите тему</option>
            <option v-for="theme in editThemes" :key="theme.id" :value="theme.id">
              {{ theme.theme_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <input v-model="editThemeName" placeholder="Новое название темы" class="form-input" />
        </div>
        <button @click="updateTheme" class="action-btn">Изменить</button>
      </div>
      <div v-if="editResult" class="result-message">{{ editResult }}</div>
    </section>

    <!-- 3. Удалить тему -->
    <section class="theme-mgmt-section">
      <h2>Удалить тему</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="deleteSubjectId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="deleteThemeId" @focus="fetchThemesForDelete" class="form-select">
            <option disabled value="">Выберите тему</option>
            <option v-for="theme in deleteThemes" :key="theme.id" :value="theme.id">
              {{ theme.theme_name }}
            </option>
          </select>
        </div>
        <button @click="deleteTheme" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="deleteResult" class="result-message">{{ deleteResult }}</div>
    </section>

    <!-- 4. Посмотреть список тем по предмету -->
    <section class="theme-mgmt-section">
      <h2>Посмотреть список тем по предмету</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="viewSubjectId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <button @click="fetchThemesForView" :disabled="!viewSubjectId" class="action-btn">Показать</button>
        <button v-if="showThemesTable" @click="hideThemesTable" class="action-btn">Скрыть</button>
      </div>
      <div v-if="showThemesTable" class="theme-list">
        <table class="theme-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Название темы</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="theme in viewThemes" :key="theme.id">
              <td>{{ theme.id }}</td>
              <td>{{ theme.theme_name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const API_URL = import.meta.env.VITE_API_URL; // добавьте эту строку

const subjects = ref([])
const createSubjectId = ref('')
const createThemeName = ref('')
const createResult = ref('')

const editSubjectId = ref('')
const editThemes = ref([])
const editThemeId = ref('')
const editThemeName = ref('')
const editResult = ref('')

const deleteSubjectId = ref('')
const deleteThemes = ref([])
const deleteThemeId = ref('')
const deleteResult = ref('')

const viewSubjectId = ref('')
const viewThemes = ref([])
const showThemesTable = ref(false)

async function fetchSubjects() {
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/subjects/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjects.value = await res.json()
  }
}

async function fetchThemesForEdit() {
  if (!editSubjectId.value) {
    editThemes.value = []
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/themes/by_subject/${editSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    editThemes.value = await res.json()
  }
}

async function fetchThemesForDelete() {
  if (!deleteSubjectId.value) {
    deleteThemes.value = []
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/themes/by_subject/${deleteSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteThemes.value = await res.json()
  }
}

async function fetchThemesForView() {
  if (!viewSubjectId.value) {
    viewThemes.value = []
    showThemesTable.value = false
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/themes/by_subject/${viewSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    viewThemes.value = await res.json()
    showThemesTable.value = true
  }
}

async function createTheme() {
  createResult.value = ''
  if (!createSubjectId.value || !createThemeName.value) {
    createResult.value = 'Выберите предмет и введите название темы'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/themes/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ theme_name: createThemeName.value, subject_id: createSubjectId.value })
  })
  if (res.ok) {
    createResult.value = 'Тема создана'
    createThemeName.value = ''
    createSubjectId.value = ''
  } else {
    const data = await res.json()
    createResult.value = data.detail || 'Ошибка создания'
  }
}

async function updateTheme() {
  editResult.value = ''
  if (!editSubjectId.value || !editThemeId.value || !editThemeName.value) {
    editResult.value = 'Выберите предмет, тему и введите новое название'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/themes/${editThemeId.value}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ theme_name: editThemeName.value, subject_id: editSubjectId.value })
  })
  if (res.ok) {
    editResult.value = 'Тема изменена'
    editThemeId.value = ''
    editThemeName.value = ''
    editSubjectId.value = ''
  } else {
    const data = await res.json()
    editResult.value = data.detail || 'Ошибка изменения'
  }
}

async function deleteTheme() {
  deleteResult.value = ''
  if (!deleteSubjectId.value || !deleteThemeId.value) {
    deleteResult.value = 'Выберите предмет и тему'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/themes/${deleteThemeId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteResult.value = 'Тема удалена'
    deleteThemeId.value = ''
    deleteSubjectId.value = ''
  } else {
    const data = await res.json()
    deleteResult.value = data.detail || 'Ошибка удаления'
  }
}

function hideThemesTable() {
  showThemesTable.value = false
}

watch(editSubjectId, fetchThemesForEdit)
watch(deleteSubjectId, fetchThemesForDelete)
</script>

<style scoped>
.theme-management, 
.theme-management * {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.theme-management {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.theme-mgmt-section {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.12);
  padding: 2rem;
  margin-bottom: 2rem;
}

.theme-mgmt-section h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #f2e9e4;
  font-size: 1.5rem;
  font-weight: 600;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: flex-end;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-input, .form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #9a8c98;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #22223b;
  color: #f2e9e4;
}

.form-input::placeholder {
  color: #c9ada7;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #4a4e69;
  box-shadow: 0 0 0 2px #4a4e6933;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  background: #4a4e69;
  color: #f2e9e4;
  height: fit-content;
  white-space: nowrap;
}

.action-btn:hover {
  background: #22223b;
}

.action-btn:disabled {
  background: #9a8c98;
  cursor: not-allowed;
}

.delete-btn {
  background: #bb0a21;
}

.delete-btn:hover {
  background: #9a0a1a;
}

.result-message {
  margin-top: 1.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: #f2e9e4;
  color: #bb0a21;
  text-align: center;
  border: 1px solid #bb0a21;
}

.theme-list {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #9a8c98;
  width: 100%;
}

.theme-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.theme-table th, .theme-table td {
  border: 1px solid #9a8c98;
  padding: 0.75rem;
  text-align: left;
}

.theme-table th {
  background-color: #4a4e69;
  color: #f2e9e4;
  font-weight: 500;
}

.theme-table td {
  background-color: #22223b;
  color: #f2e9e4;
}

.theme-table tr:nth-child(even) td {
  background-color: #2a2a42;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-group {
    width: 100%;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>