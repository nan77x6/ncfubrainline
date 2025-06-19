<template>
  <div class="class-management">
    <!-- 1. Создать новый класс -->
    <section class="class-mgmt-section">
      <h2>Создать новый класс</h2>
      <div class="form-row">
        <div class="form-group">
          <input v-model="createName" placeholder="Название класса" class="form-input" />
        </div>
        <button @click="createClass" class="action-btn">Добавить</button>
      </div>
      <div v-if="createResult" class="result-message">{{ createResult }}</div>
    </section>

    <!-- 2. Изменить класс -->
    <section class="class-mgmt-section">
      <h2>Изменить класс</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="editId" class="form-select">
            <option disabled value="">Выберите класс</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.class_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <input v-model="editName" placeholder="Новое название класса" class="form-input" />
        </div>
        <button @click="updateClass" class="action-btn">Изменить</button>
      </div>
      <div v-if="editResult" class="result-message">{{ editResult }}</div>
    </section>

    <!-- 3. Удалить класс -->
    <section class="class-mgmt-section">
      <h2>Удалить класс</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="deleteId" class="form-select">
            <option disabled value="">Выберите класс</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.class_name }}
            </option>
          </select>
        </div>
        <button @click="deleteClass" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="deleteResult" class="result-message">{{ deleteResult }}</div>
    </section>

    <!-- 4. Добавить ученика в класс -->
    <section class="class-mgmt-section">
      <h2>Добавить ученика в класс</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="addStudentClassId" class="form-select">
            <option disabled value="">Выберите класс</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.class_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="addStudentUserId" class="form-select">
            <option disabled value="">Выберите ученика</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.full_name }}
            </option>
          </select>
        </div>
        <button @click="addStudentToClass" class="action-btn">Добавить</button>
      </div>
      <div v-if="addStudentResult" class="result-message">{{ addStudentResult }}</div>
    </section>

    <!-- 5. Удалить ученика из класса -->
    <section class="class-mgmt-section">
      <h2>Удалить ученика из класса</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="removeClassId" class="form-select">
            <option disabled value="">Выберите класс</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.class_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="removeStudentId" class="form-select">
            <option disabled value="">Выберите ученика</option>
            <option v-for="student in removeStudents" :key="student.id" :value="student.id">
              {{ student.full_name }}
            </option>
          </select>
        </div>
        <button @click="removeStudentFromClass" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="removeStudentResult" class="result-message">{{ removeStudentResult }}</div>
    </section>

    <!-- 6. Посмотреть списки классов -->
    <section class="class-mgmt-section">
      <h2>Посмотреть списки классов</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="viewClassId" class="form-select">
            <option disabled value="">Выберите класс</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.class_name }}
            </option>
          </select>
        </div>
        <button @click="fetchClassStudents" :disabled="!viewClassId" class="action-btn">Показать</button>
        <button v-if="showClassStudents" @click="hideClassStudents" class="action-btn">Скрыть</button>
      </div>
      <div v-if="showClassStudents" class="class-list">
        <h3 class="class-list-title">Ученики класса</h3>
        <table class="class-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>ФИО</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in classStudents" :key="student.id">
              <td>{{ student.id }}</td>
              <td>{{ student.full_name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const classes = ref([])
const students = ref([])
const createName = ref('')
const createResult = ref('')
const editId = ref('')
const editName = ref('')
const editResult = ref('')
const deleteId = ref('')
const deleteResult = ref('')
const addStudentClassId = ref('')
const addStudentUserId = ref('')
const addStudentResult = ref('')
const viewClassId = ref('')
const classStudents = ref([])
const showClassStudents = ref(false)
const removeClassId = ref('')
const removeStudentId = ref('')
const removeStudents = ref([])
const removeStudentResult = ref('')
const subjectsWithTeachers = ref([])

async function fetchClasses() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/classes/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    classes.value = await res.json()
  }
}

async function fetchStudents() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/users/students_without_class/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    students.value = await res.json()
  }
}

async function createClass() {
  createResult.value = ''
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/classes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ class_name: createName.value })
  })
  if (res.ok) {
    createResult.value = 'Класс создан'
    createName.value = ''
    fetchClasses()
  } else {
    const data = await res.json()
    createResult.value = data.detail || 'Ошибка создания'
  }
}

async function updateClass() {
  editResult.value = ''
  if (!editId.value || !editName.value) {
    editResult.value = 'Выберите класс и введите новое название'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/classes/${editId.value}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ class_name: editName.value })
  })
  if (res.ok) {
    editResult.value = 'Класс изменён'
    editId.value = ''
    editName.value = ''
    fetchClasses()
  } else {
    const data = await res.json()
    editResult.value = data.detail || 'Ошибка изменения'
  }
}

async function deleteClass() {
  deleteResult.value = ''
  if (!deleteId.value) {
    deleteResult.value = 'Выберите класс'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/classes/${deleteId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteResult.value = 'Класс удалён'
    deleteId.value = ''
    fetchClasses()
  } else {
    const data = await res.json()
    deleteResult.value = data.detail || 'Ошибка удаления'
  }
}

async function addStudentToClass() {
  addStudentResult.value = ''
  if (!addStudentClassId.value || !addStudentUserId.value) {
    addStudentResult.value = 'Выберите класс и ученика'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/user-classes/?user_id=${addStudentUserId.value}&class_id=${addStudentClassId.value}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      user_id: addStudentUserId.value,
      class_id: addStudentClassId.value
    })
  })
  if (res.ok) {
    addStudentResult.value = 'Ученик добавлен в класс'
    addStudentClassId.value = ''
    addStudentUserId.value = ''
  } else {
    const data = await res.json()
    addStudentResult.value = data.detail || 'Ошибка добавления'
  }
}

watch(removeClassId, async (newClassId) => {
  removeStudentId.value = ''
  if (!newClassId) {
    removeStudents.value = []
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/classes/${newClassId}/students`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    removeStudents.value = await res.json()
  }
})

async function removeStudentFromClass() {
  removeStudentResult.value = ''
  if (!removeStudentId.value) {
    removeStudentResult.value = 'Выберите ученика'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/user-classes/${removeStudentId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    removeStudentResult.value = 'Ученик удалён из класса'
    const idx = removeStudents.value.findIndex(s => s.id === removeStudentId.value)
    if (idx !== -1) removeStudents.value.splice(idx, 1)
    removeStudentId.value = ''
    fetchStudents()
  } else {
    const data = await res.json()
    removeStudentResult.value = data.detail || 'Ошибка удаления'
  }
}

async function fetchClassStudents() {
  if (!viewClassId.value) return
  showClassStudents.value = false
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/classes/${viewClassId.value}/students`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    classStudents.value = (await res.json()).sort((a, b) =>
      a.full_name.localeCompare(b.full_name, 'ru')
    )
    showClassStudents.value = true
  }
}

function hideClassStudents() {
  showClassStudents.value = false
}

async function fetchSubjectsWithTeachers() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/subjects/with-teachers', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjectsWithTeachers.value = await res.json()
  }
}

onMounted(() => {
  fetchClasses()
  fetchStudents()
  fetchSubjectsWithTeachers()
})
</script>

<style scoped>
.class-management, 
.class-management * {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.class-management {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.class-mgmt-section {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.12);
  padding: 2rem;
  margin-bottom: 2rem;
}

.class-mgmt-section h2 {
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
  align-items: flex-end; /* Выравнивание по нижнему краю */
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
  white-space: nowrap; /* Запрет переноса текста */
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

.class-list {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #9a8c98;
  width: 100%;
}

.class-list-title {
  font-size: 1.1rem;
  color: #c9ada7;
  margin-bottom: 1rem;
  text-align: center;
}

.class-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.class-table th, .class-table td {
  border: 1px solid #9a8c98;
  padding: 0.75rem;
  text-align: left;
}

.class-table th {
  background-color: #4a4e69;
  color: #f2e9e4;
  font-weight: 500;
}

.class-table td {
  background-color: #22223b;
  color: #f2e9e4;
}

.class-table tr:nth-child(even) td {
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