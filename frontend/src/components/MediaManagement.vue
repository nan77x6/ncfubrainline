<template>
  <div class="media-management">
    <!-- Загрузка медиа -->
    <section class="media-mgmt-section">
      <h2>Загрузить медиафайл</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="subjectId" @change="onSubjectChange" class="form-select" required>
            <option value="">Выберите предмет</option>
            <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.subject_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="themeId" @change="onThemeChange" :disabled="!subjectId" class="form-select" required>
            <option value="">Выберите тему</option>
            <option v-for="t in themes" :key="t.id" :value="t.id">{{ t.theme_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="materialId" @change="onMaterialChange" :disabled="!themeId" class="form-select" required>
            <option value="">Выберите материал</option>
            <option v-for="m in materials" :key="m.id" :value="m.id">{{ m.title }}</option>
          </select>
        </div>
        <div class="form-group">
          <input type="file" @change="onFileChange" class="form-input" required />
        </div>
        <button @click="uploadMedia" class="action-btn">Загрузить</button>
      </div>
      <div v-if="uploadStatus" class="result-message">{{ uploadStatus }}</div>
    </section>

    <!-- Удаление медиа -->
    <section class="media-mgmt-section">
      <h2>Удалить медиафайл</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="delSubjectId" @change="onDelSubjectChange" class="form-select" required>
            <option value="">Выберите предмет</option>
            <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.subject_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="delThemeId" @change="onDelThemeChange" :disabled="!delSubjectId" class="form-select" required>
            <option value="">Выберите тему</option>
            <option v-for="t in delThemes" :key="t.id" :value="t.id">{{ t.theme_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="delMaterialId" @change="onDelMaterialChange" :disabled="!delThemeId" class="form-select" required>
            <option value="">Выберите материал</option>
            <option v-for="m in delMaterials" :key="m.id" :value="m.id">{{ m.title }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="mediaIdToDelete" :disabled="!delMaterialId" class="form-select" required>
            <option value="">Выберите медиафайл</option>
            <option v-for="media in mediaList" :key="media.id" :value="media.id">
              {{ media.url.split('/').pop() }} ({{ media.type }})
            </option>
          </select>
        </div>
        <button @click="deleteMedia" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="deleteStatus" class="result-message">{{ deleteStatus }}</div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const subjects = ref([])
const themes = ref([])
const materials = ref([])
const subjectId = ref('')
const themeId = ref('')
const materialId = ref('')
const file = ref(null)
const uploadStatus = ref('')

// Для удаления
const delSubjectId = ref('')
const delThemeId = ref('')
const delMaterialId = ref('')
const delThemes = ref([])
const delMaterials = ref([])
const mediaList = ref([])
const mediaIdToDelete = ref('')
const deleteStatus = ref('')

onMounted(fetchSubjects)

async function fetchSubjects() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/subjects/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjects.value = await res.json()
  }
}

// --- Загрузка медиа ---
async function onSubjectChange() {
  themeId.value = ''
  materialId.value = ''
  themes.value = []
  materials.value = []
  if (!subjectId.value) return
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/themes/by_subject/${subjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    themes.value = await res.json()
  }
}

async function onThemeChange() {
  materialId.value = ''
  materials.value = []
  if (!themeId.value) return
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/materials/by_theme/${themeId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    materials.value = await res.json()
  }
}

function onMaterialChange() {
  // ничего не делаем, но можно добавить предпросмотр медиа
}

function onFileChange(e) {
  file.value = e.target.files[0]
}

async function uploadMedia() {
  if (!materialId.value || !file.value) return
  const formData = new FormData()
  formData.append('material_id', materialId.value)
  formData.append('file', file.value)
  const token = localStorage.getItem('token')
  uploadStatus.value = 'Загрузка...'
  const res = await fetch('http://localhost:8000/media/upload/', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData
  })
  if (res.ok) {
    uploadStatus.value = 'Файл успешно загружен!'
    file.value = null
  } else {
    uploadStatus.value = 'Ошибка загрузки'
  }
}

// --- Удаление медиа ---
async function onDelSubjectChange() {
  delThemeId.value = ''
  delMaterialId.value = ''
  mediaIdToDelete.value = ''
  delThemes.value = []
  delMaterials.value = []
  mediaList.value = []
  if (!delSubjectId.value) return
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/themes/by_subject/${delSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    delThemes.value = await res.json()
  }
}

async function onDelThemeChange() {
  delMaterialId.value = ''
  mediaIdToDelete.value = ''
  delMaterials.value = []
  mediaList.value = []
  if (!delThemeId.value) return
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/materials/by_theme/${delThemeId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    delMaterials.value = await res.json()
  }
}

async function onDelMaterialChange() {
  mediaIdToDelete.value = ''
  mediaList.value = []
  if (!delMaterialId.value) return
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/media/by_material/${delMaterialId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    mediaList.value = await res.json()
  }
}

async function deleteMedia() {
  if (!mediaIdToDelete.value) return
  const token = localStorage.getItem('token')
  deleteStatus.value = 'Удаление...'
  const res = await fetch(`http://localhost:8000/media/${mediaIdToDelete.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteStatus.value = 'Медиафайл удалён'
    // Обновить список медиа
    await onDelMaterialChange()
    mediaIdToDelete.value = ''
  } else {
    deleteStatus.value = 'Ошибка удаления'
  }
}
</script>

<style scoped>
.media-management, 
.media-management * {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.media-management {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.media-mgmt-section {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.12);
  padding: 2rem;
  margin-bottom: 2rem;
}

.media-mgmt-section h2 {
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
  align-self: flex-end;
  height: fit-content;
}

.action-btn:hover {
  background: #22223b;
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
</style>