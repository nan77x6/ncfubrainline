<template>
  <div class="material-management">
    <!-- 1. Добавить новый материал к теме -->
    <section class="material-mgmt-section">
      <h2>Добавить новый материал к теме</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="addSubjectId" class="form-select" @focus="fetchSubjects">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">{{ subj.subject_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="addThemeId" class="form-select">
            <option disabled value="">Выберите тему</option>
            <option v-for="theme in addThemes" :key="theme.id" :value="theme.id">{{ theme.theme_name }}</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <input v-model="addTitle" placeholder="Заголовок материала" class="form-input" />
        </div>
      </div>
      <div class="editor-container">
        <textarea ref="addTextareaRef"></textarea>
      </div>
      <div class="form-row">
        <button @click="createMaterial" class="action-btn">Добавить материал</button>
      </div>
      <div v-if="addResult" class="result-message">{{ addResult }}</div>
    </section>

    <!-- 2. Изменить материал темы -->
    <section class="material-mgmt-section">
      <h2>Изменить материал темы</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="editSubjectId" class="form-select" @focus="fetchSubjects">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">{{ subj.subject_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="editThemeId" class="form-select" @focus="fetchThemesForEdit">
            <option disabled value="">Выберите тему</option>
            <option v-for="theme in editThemes" :key="theme.id" :value="theme.id">{{ theme.theme_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="editMaterialId" class="form-select">
            <option disabled value="">Выберите материал</option>
            <option v-for="mat in editMaterials" :key="mat.id" :value="mat.id">{{ mat.title }}</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <input v-model="editTitle" placeholder="Заголовок материала" class="form-input" />
        </div>
      </div>
      <div class="editor-container">
        <textarea ref="editTextareaRef"></textarea>
      </div>
      <div class="form-row">
        <button @click="updateMaterial" class="action-btn">Изменить материал</button>
      </div>
      <div v-if="editResult" class="result-message">{{ editResult }}</div>
    </section>

    <!-- 3. Удалить материал из темы -->
    <section class="material-mgmt-section">
      <h2>Удалить материал из темы</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="deleteSubjectId" class="form-select" @focus="fetchSubjects">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">{{ subj.subject_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="deleteThemeId" class="form-select" @focus="fetchThemesForDelete">
            <option disabled value="">Выберите тему</option>
            <option v-for="theme in deleteThemes" :key="theme.id" :value="theme.id">{{ theme.theme_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="deleteMaterialId" class="form-select">
            <option disabled value="">Выберите материал</option>
            <option v-for="mat in deleteMaterials" :key="mat.id" :value="mat.id">{{ mat.title }}</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <button @click="deleteMaterial" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="deleteResult" class="result-message">{{ deleteResult }}</div>
    </section>

    <!-- 4. Просмотреть добавленный материал к темам в виде списка -->
    <section class="material-mgmt-section">
      <h2>Просмотреть добавленный материал к темам в виде списка</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="viewSubjectId" class="form-select" @focus="fetchSubjects">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">{{ subj.subject_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="viewThemeId" class="form-select">
            <option disabled value="">Выберите тему</option>
            <option v-for="theme in viewThemes" :key="theme.id" :value="theme.id">{{ theme.theme_name }}</option>
          </select>
        </div>
        <button @click="fetchMaterialsForView" :disabled="!viewThemeId" class="action-btn">Показать материалы</button>
      </div>
      <div v-if="showMaterialsTable" class="material-list">
        <table class="material-table">
          <thead>
            <tr>
              <th>Название</th>
              <th>ID темы</th>
              <th>Создал</th>
              <th>Дата создания</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mat in viewMaterials" :key="mat.id">
              <td>{{ mat.title }}</td>
              <td>{{ mat.theme_id }}</td>
              <td>{{ mat.created_by }}</td>
              <td>{{ mat.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import SimpleMDE from 'simplemde'
import 'simplemde/dist/simplemde.min.css'

// --- Данные и состояния ---
const subjects = ref([])
const addThemes = ref([])
const editThemes = ref([])
const deleteThemes = ref([])
const viewThemes = ref([])

const addSubjectId = ref('')
const addThemeId = ref('')
const addTitle = ref('')
const addMarkdown = ref('')
const addTextareaRef = ref(null)
let addSimplemde = null

const editSubjectId = ref('')
const editThemeId = ref('')
const editMaterialId = ref('')
const editTitle = ref('')
const editMarkdown = ref('')
const editTextareaRef = ref(null)
let editSimplemde = null
const editMaterials = ref([])

const deleteSubjectId = ref('')
const deleteThemeId = ref('')
const deleteMaterialId = ref('')
const deleteMaterials = ref([])

const viewSubjectId = ref('')
const viewThemeId = ref('')
const viewMaterials = ref([])
const showMaterialsTable = ref(false)

const addResult = ref('')
const editResult = ref('')
const deleteResult = ref('')

// --- Получение токена ---
function getToken() {
  return localStorage.getItem('token')
}

// --- CRUD: Загрузка предметов и тем ---
async function fetchSubjects() {
  const token = getToken()
  if (!token) return
  const res = await fetch('http://localhost:8000/subjects/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjects.value = await res.json()
  }
}

// Для добавления материала
async function fetchThemesForAdd() {
  if (!addSubjectId.value) {
    addThemes.value = []
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/themes/by_subject/${addSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    addThemes.value = await res.json()
  }
}

// Для редактирования материала
async function fetchThemesForEdit() {
  if (!editSubjectId.value) {
    editThemes.value = []
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/themes/by_subject/${editSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    editThemes.value = await res.json()
  }
  fetchMaterialsForEdit()
}

// Для удаления материала
async function fetchThemesForDelete() {
  if (!deleteSubjectId.value) {
    deleteThemes.value = []
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/themes/by_subject/${deleteSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteThemes.value = await res.json()
  }
  fetchMaterialsForDelete()
}

// Для просмотра материалов
async function fetchThemesForView() {
  if (!viewSubjectId.value) {
    viewThemes.value = []
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/themes/by_subject/${viewSubjectId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    viewThemes.value = await res.json()
  }
}

// --- Загрузка материалов для редактирования/удаления ---
async function fetchMaterialsForEdit() {
  if (!editThemeId.value) {
    editMaterials.value = []
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/materials/by_theme/${editThemeId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    editMaterials.value = await res.json()
  }
}

async function fetchMaterialsForDelete() {
  if (!deleteThemeId.value) {
    deleteMaterials.value = []
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/materials/by_theme/${deleteThemeId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteMaterials.value = await res.json()
  }
}

async function fetchMaterialsForView() {
  if (!viewThemeId.value) {
    viewMaterials.value = []
    showMaterialsTable.value = false
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/materials/by_theme/${viewThemeId.value}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    viewMaterials.value = await res.json()
    showMaterialsTable.value = true
  }
}

// --- Watchers для автоматической загрузки тем и материалов ---
watch(addSubjectId, () => {
  fetchThemesForAdd()
  addThemeId.value = ''
})
watch(addThemeId, () => {
  // Можно добавить автозагрузку материалов, если нужно
})

watch(editSubjectId, () => {
  fetchThemesForEdit()
  editThemeId.value = ''
  editMaterialId.value = ''
})
watch(editThemeId, () => {
  fetchMaterialsForEdit()
  editMaterialId.value = ''
})

watch(deleteSubjectId, () => {
  fetchThemesForDelete()
  deleteThemeId.value = ''
  deleteMaterialId.value = ''
})
watch(deleteThemeId, () => {
  fetchMaterialsForDelete()
  deleteMaterialId.value = ''
})

watch(viewSubjectId, () => {
  fetchThemesForView()
  viewThemeId.value = ''
  showMaterialsTable.value = false
})
watch(viewThemeId, () => {
  showMaterialsTable.value = false
})

// --- CRUD: Добавление, изменение, удаление материала ---
async function createMaterial() {
  addResult.value = ''
  if (!addTitle.value || !addThemeId.value || !addMarkdown.value) {
    addResult.value = 'Заполните все поля'
    return
  }
  const token = getToken()
  const res = await fetch('http://localhost:8000/materials/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      title: addTitle.value,
      markdown_content: addMarkdown.value,
      theme_id: addThemeId.value
    })
  })
  if (res.ok) {
    addResult.value = 'Материал успешно добавлен'
    addTitle.value = ''
    addMarkdown.value = ''
    if (addSimplemde) addSimplemde.value('')
    fetchMaterialsForView()
  } else {
    addResult.value = 'Ошибка добавления материала'
  }
}

async function updateMaterial() {
  editResult.value = ''
  if (!editMaterialId.value || !editTitle.value || !editThemeId.value || !editMarkdown.value) {
    editResult.value = 'Заполните все поля'
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/materials/${editMaterialId.value}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      title: editTitle.value,
      markdown_content: editMarkdown.value,
      theme_id: editThemeId.value
    })
  })
  if (res.ok) {
    editResult.value = 'Материал успешно изменён'
    fetchMaterialsForEdit()
    fetchMaterialsForView()
  } else {
    editResult.value = 'Ошибка изменения материала'
  }
}

async function deleteMaterial() {
  deleteResult.value = ''
  if (!deleteMaterialId.value) {
    deleteResult.value = 'Выберите материал'
    return
  }
  const token = getToken()
  const res = await fetch(`http://localhost:8000/materials/${deleteMaterialId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteResult.value = 'Материал успешно удалён'
    fetchMaterialsForDelete()
    fetchMaterialsForView()
  } else {
    deleteResult.value = 'Ошибка удаления материала'
  }
}

// --- Инициализация SimpleMDE ---
onMounted(async () => {
  await nextTick()
  await fetchSubjects()
  if (addTextareaRef.value) {
    addSimplemde = new SimpleMDE({
      element: addTextareaRef.value,
      initialValue: addMarkdown.value,
      spellChecker: false,
      status: false,
      autosave: false,
      placeholder: 'Введите текст в формате Markdown...',
      toolbar: ["bold", "italic", "heading", "|", "quote", "unordered-list", "ordered-list", "|", "link", "image", "|", "preview", "side-by-side", "fullscreen", "|", "guide"]
    })
    addSimplemde.codemirror.on('change', () => {
      addMarkdown.value = addSimplemde.value()
    })
  }
  if (editTextareaRef.value) {
    editSimplemde = new SimpleMDE({
      element: editTextareaRef.value,
      initialValue: editMarkdown.value,
      spellChecker: false,
      status: false,
      autosave: false,
      placeholder: 'Измените текст в формате Markdown...',
      toolbar: ["bold", "italic", "heading", "|", "quote", "unordered-list", "ordered-list", "|", "link", "image", "|", "preview", "side-by-side", "fullscreen", "|", "guide"]
    })
    editSimplemde.codemirror.on('change', () => {
      editMarkdown.value = editSimplemde.value()
    })
  }
})

onBeforeUnmount(() => {
  if (addSimplemde) {
    addSimplemde.toTextArea()
    addSimplemde = null
  }
  if (editSimplemde) {
    editSimplemde.toTextArea()
    editSimplemde = null
  }
})
</script>

<style scoped>
.material-management,
.material-management * {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.material-management {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.material-mgmt-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.10);
  padding: 2rem;
  margin-bottom: 2rem;
}

.material-mgmt-section h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #22223b;
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

/* Центрирование кнопок */
.form-row:has(.action-btn),
.form-row:has(.delete-btn) {
  justify-content: center;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-input, .form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #c9ada7;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #f2e9e4;
  color: #22223b;
}

.form-input::placeholder {
  color: #9a8c98;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #4a4e69;
  box-shadow: 0 0 0 2px #4a4e6933;
}

.editor-container {
  margin: 1rem auto 1.5rem auto;
  width: 100%;
  max-width: 700px;
}

/* SimpleMDE редактор */
.editor-container .CodeMirror {
  background: #f2e9e4;
  color: #22223b;
  border: 1px solid #c9ada7;
  border-radius: 8px;
}

.editor-container .CodeMirror-cursor {
  border-left: 1px solid #22223b;
}

.editor-container .editor-toolbar {
  background: #fff !important;
  border: 1px solid #c9ada7 !important;
  border-radius: 8px 8px 0 0 !important;
  opacity: 1 !important;
}

.editor-container .editor-toolbar button,
.editor-container .editor-toolbar i,
.editor-container .editor-toolbar svg {
  color: #22223b !important;
  opacity: 1 !important;
  filter: none !important;
}

.editor-container .editor-toolbar button:hover,
.editor-container .editor-toolbar button.active {
  background: #f2e9e4 !important;
  color: #bb0a21 !important;
}

.editor-container .editor-toolbar button.disabled,
.editor-container .editor-toolbar button[disabled] {
  color: #c9ada7 !important;
  opacity: 0.7 !important;
  background: transparent !important;
  cursor: not-allowed !important;
  filter: none !important;
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
  color: #fff;
  height: fit-content;
  white-space: nowrap;
  /* Центрирование для одиночной кнопки */
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #22223b;
  color: #fff;
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

.material-list {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #c9ada7;
  width: 100%;
}

.material-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.material-table th, .material-table td {
  border: 1px solid #c9ada7;
  padding: 0.75rem;
  text-align: left;
}

.material-table th {
  background-color: #f2e9e4;
  color: #22223b;
  font-weight: 500;
}

.material-table td {
  background-color: #fff;
  color: #22223b;
}

.material-table tr:nth-child(even) td {
  background-color: #f2e9e4;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 1rem;
    align-items: center;
  }
  .action-btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>