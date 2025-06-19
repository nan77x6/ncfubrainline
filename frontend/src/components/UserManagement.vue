<template>
  <div class="user-management">
    <!-- 1. Создать профиль пользователя -->
    <section class="user-mgmt-section">
      <h2>Создать профиль пользователя</h2>
      <div class="form-row">
        <div class="form-group">
          <input v-model="createForm.full_name" placeholder="ФИО" class="form-input" />
        </div>
        <div class="form-group">
          <select v-model="createForm.role" class="form-select">
            <option value="student">Ученик</option>
            <option value="teacher">Учитель</option>
            <option value="admin">Администратор</option>
          </select>
        </div>
        <button @click="createUser" class="action-btn">Добавить</button>
      </div>
      <div v-if="createResult" class="result-message">{{ createResult }}</div>
    </section>

    <!-- 2. Создать новые профили для учеников -->
    <section class="user-mgmt-section">
      <h2>Создать новые профили для учеников</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="bulkForm.class_id" class="form-select">
            <option disabled value="">Выберите класс</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.class_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <input type="file" @change="onFileChange" accept=".xlsx" class="form-input" />
        </div>
        <button @click="bulkAddStudents" class="action-btn">Добавить</button>
      </div>
      <div v-if="bulkResult" class="result-message">{{ bulkResult }}</div>
    </section>

    <!-- 3. Изменить профиль пользователя -->
    <section class="user-mgmt-section">
      <h2>Изменить профиль пользователя</h2>
      <div class="form-row">
        <div class="form-group">
          <input v-model="editForm.id" placeholder="ID пользователя" class="form-input" />
        </div>
        <button @click="fetchUser" class="action-btn">Загрузить</button>
      </div>
      <div v-if="editUser" class="edit-form">
        <div class="form-row">
          <div class="form-group">
            <input v-model="editForm.login" placeholder="Логин" readonly class="form-input" />
          </div>
          <div class="form-group">
            <input v-model="editForm.password" placeholder="Пароль" readonly class="form-input" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <input v-model="editForm.full_name" placeholder="ФИО" class="form-input" />
          </div>
          <div class="form-group">
            <select v-model="editForm.role" class="form-select">
              <option value="student">Ученик</option>
              <option value="teacher">Учитель</option>
              <option value="admin">Администратор</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <button class="action-btn generate-btn" @click="toggleGenerate">
            {{ editForm.generated ? 'Отчистить данные' : 'Сгенерировать данные' }}
          </button>
          <button @click="updateUser" class="action-btn save-btn">Изменить</button>
        </div>
      </div>
      <div v-if="editResult" class="result-message">{{ editResult }}</div>
    </section>

    <!-- 4. Удалить профиль пользователя -->
    <section class="user-mgmt-section">
      <h2>Удалить профиль пользователя</h2>
      <div class="form-row">
        <div class="form-group">
          <input v-model="deleteForm.id" placeholder="ID пользователя" class="form-input" />
        </div>
        <button @click="deleteUser" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="deleteResult" class="result-message">{{ deleteResult }}</div>
    </section>

    <!-- 5. Удалить профили пользователей в диапазоне -->
    <section class="user-mgmt-section">
      <h2>Удалить профили пользователей в диапазоне</h2>
      <div class="form-row">
        <div class="form-group">
          <input v-model="bulkDeleteForm.start_id" placeholder="С какого id" class="form-input" />
        </div>
        <div class="form-group">
          <input v-model="bulkDeleteForm.end_id" placeholder="По какой id" class="form-input" />
        </div>
        <button @click="bulkDeleteUsers" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="bulkDeleteResult" class="result-message">{{ bulkDeleteResult }}</div>
    </section>

    <!-- 6. Удалить профили пользователей из определённого класса -->
    <section class="user-mgmt-section">
      <h2>Удалить профили пользователей из определённого класса</h2>
      <div class="form-row">
        <div class="form-group">
          <input v-model="deleteByClassForm.class_id" placeholder="ID класса" class="form-input" />
        </div>
        <button @click="deleteUsersByClass" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="deleteByClassResult" class="result-message">{{ deleteByClassResult }}</div>
    </section>

    <!-- 7. Посмотреть список пользователей -->
    <section class="user-mgmt-section">
      <h2>Посмотреть список пользователей</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="listRole" @change="onRoleChange" class="form-select">
            <option value="">Все</option>
            <option value="admin">Администраторы</option>
            <option value="teacher">Учителя</option>
            <option value="student">Ученики</option>
            <option value="teachers_without_subject">Учителя без предмета</option>
            <option value="students_without_class">Ученики без класса</option>       
          </select>
        </div>
        <button v-if="!anyListOpen" @click="fetchUsers" class="action-btn">Показать</button>
        <button v-else @click="hideAllLists" class="action-btn">Скрыть</button>
      </div>
      <div v-if="showList" class="user-list">
        <h3 class="user-list-title">
          <template v-if="listRole === ''">Все пользователи</template>
          <template v-else-if="listRole === 'student'">Все ученики</template>
          <template v-else-if="listRole === 'teacher'">Все учителя</template>
          <template v-else-if="listRole === 'admin'">Все администраторы</template>
        </h3>
        <table class="user-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>ФИО</th>
              <th>Роль</th>
              <th>Логин</th>
              <th>Пароль</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.full_name }}</td>
              <td>{{ u.role }}</td>
              <td>{{ u.login }}</td>
              <td>{{ u.password }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="showStudentsWithoutClass" class="user-list">
        <h3 class="user-list-title">Ученики без класса</h3>
        <table class="user-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>ФИО</th>
              <th>Логин</th>
              <th>Пароль</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in studentsWithoutClass" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.full_name }}</td>
              <td>{{ u.login }}</td>
              <td>{{ u.password }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="showTeachersWithoutSubject" class="user-list">
        <h3 class="user-list-title">Учителя без предмета</h3>
        <table class="user-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>ФИО</th>
              <th>Логин</th>
              <th>Пароль</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in teachersWithoutSubject" :key="u.id">
              <td>{{ u.id }}</td>
              <td>{{ u.full_name }}</td>
              <td>{{ u.login }}</td>
              <td>{{ u.password }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
function onRoleChange() {
  hideAllLists();
}

const mode = ref('create')
const menu = [
  { mode: 'create', label: 'Создать профиль пользователя' },
  { mode: 'bulk', label: 'Создать новые профили для учеников' },
  { mode: 'edit', label: 'Изменить профиль пользователя' },
  { mode: 'delete', label: 'Удалить профиль пользователя' },
  { mode: 'bulkDelete', label: 'Удалить профили пользователей в диапазоне' },
  { mode: 'deleteByClass', label: 'Удалить профили пользователей из определённого класса' },
  { mode: 'list', label: 'Посмотреть список пользователей' }
]

// --- Создание пользователя ---
const createForm = ref({ full_name: '', role: 'student' })
const createResult = ref('')
async function createUser() {
  createResult.value = ''
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/users/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(createForm.value)
  })
  if (res.ok) {
    const data = await res.json()
    createResult.value = `Пользователь создан. Логин: ${data.login}, Пароль: ${data.password}`
    createForm.value.full_name = ''
    createForm.value.role = 'student'
  } else {
    createResult.value = 'Ошибка создания пользователя'
  }
}

// --- Массовое добавление учеников ---
const bulkForm = ref({ class_id: '', file: null })
const bulkResult = ref('')
const classes = ref([])
async function fetchClasses() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/classes/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    classes.value = await res.json()
  }
}
function onFileChange(e) {
  bulkForm.value.file = e.target.files[0]
}
async function bulkAddStudents() {
  bulkResult.value = ''
  if (!bulkForm.value.class_id || !bulkForm.value.file) {
    bulkResult.value = 'Выберите класс и файл'
    return
  }
  const token = localStorage.getItem('token')
  const formData = new FormData()
  formData.append('class_id', bulkForm.value.class_id)
  formData.append('file', bulkForm.value.file)
  const res = await fetch('http://localhost:8000/users/bulk_students/', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData
  })
  if (res.ok) {
    const data = await res.json()
    bulkResult.value = `Добавлено: ${data.count}`
  } else {
    bulkResult.value = 'Ошибка массового добавления'
  }
}

// --- Изменение пользователя ---
const editForm = ref({ id: '', login: '', password: '', full_name: '', role: 'student', generated: false })
const editUser = ref(null)
const editResult = ref('')
async function fetchUser() {
  editResult.value = ''
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/users/?role=`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const users = await res.json()
    const user = users.find(u => u.id == editForm.value.id)
    if (user) {
      editUser.value = user
      editForm.value.full_name = user.full_name
      editForm.value.role = user.role
    } else {
      editResult.value = 'Пользователь не найден'
    }
  }
}
function toggleGenerate() {
  if (!editForm.value.generated) {
    editForm.value.login = Math.random().toString(36).slice(2, 10)
    editForm.value.password = Math.random().toString(36).slice(2, 10)
    editForm.value.generated = true
  } else {
    editForm.value.login = ''
    editForm.value.password = ''
    editForm.value.generated = false
  }
}
async function updateUser() {
  editResult.value = ''
  const token = localStorage.getItem('token')
  const body = {}
  if (editForm.value.login) body.login = editForm.value.login
  if (editForm.value.password) body.password = editForm.value.password
  if (editForm.value.full_name) body.full_name = editForm.value.full_name
  if (editForm.value.role) body.role = editForm.value.role
  const res = await fetch(`http://localhost:8000/users/${editForm.value.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(body)
  })
  if (res.ok) {
    editResult.value = 'Профиль обновлён'
  } else {
    editResult.value = 'Ошибка обновления'
  }
}

// --- Удаление пользователя ---
const deleteForm = ref({ id: '' })
const deleteResult = ref('')
async function deleteUser() {
  deleteResult.value = ''
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/users/${deleteForm.value.id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteResult.value = 'Пользователь удалён'
  } else {
    deleteResult.value = 'Ошибка удаления'
  }
}

// --- Массовое удаление по диапазону ---
const bulkDeleteForm = ref({ start_id: '', end_id: '' })
const bulkDeleteResult = ref('')
async function bulkDeleteUsers() {
  bulkDeleteResult.value = ''
  const token = localStorage.getItem('token')
  const params = new URLSearchParams({
    start_id: bulkDeleteForm.value.start_id,
    end_id: bulkDeleteForm.value.end_id
  })
  const res = await fetch(`http://localhost:8000/users/bulk_delete/?${params}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const data = await res.json()
    bulkDeleteResult.value = `Удалено: ${data.deleted}`
  } else {
    bulkDeleteResult.value = 'Ошибка удаления'
  }
}

// --- Удаление по классу ---
const deleteByClassForm = ref({ class_id: '' })
const deleteByClassResult = ref('')
async function deleteUsersByClass() {
  deleteByClassResult.value = ''
  const token = localStorage.getItem('token')
  const params = new URLSearchParams({ class_id: deleteByClassForm.value.class_id })
  const res = await fetch(`http://localhost:8000/users/delete_by_class/?${params}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const data = await res.json()
    deleteByClassResult.value = `Удалено: ${data.deleted}`
  } else {
    deleteByClassResult.value = 'Ошибка удаления'
  }
}

// --- Список пользователей ---
const listRole = ref('')
const users = ref([])
const showList = ref(false)
const studentsWithoutClass = ref([])
const teachersWithoutSubject = ref([])
const showStudentsWithoutClass = ref(false)
const showTeachersWithoutSubject = ref(false)
const anyListOpen = computed(() =>
  showList.value || showStudentsWithoutClass.value || showTeachersWithoutSubject.value
)

function hideAllLists() {
  showList.value = false
  showStudentsWithoutClass.value = false
  showTeachersWithoutSubject.value = false
}

async function fetchUsers() {
  showList.value = false
  showStudentsWithoutClass.value = false
  showTeachersWithoutSubject.value = false

  const token = localStorage.getItem('token')

  if (listRole.value === 'students_without_class') {
    const res = await fetch('http://localhost:8000/users/students_without_class/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      studentsWithoutClass.value = await res.json()
      showStudentsWithoutClass.value = true
    }
    return
  }

  if (listRole.value === 'teachers_without_subject') {
    const res = await fetch('http://localhost:8000/users/teachers_without_subject/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res.ok) {
      teachersWithoutSubject.value = await res.json()
      showTeachersWithoutSubject.value = true
    }
    return
  }

  // Обычный список пользователей
  const params = listRole.value ? `?role=${listRole.value}` : ''
  const res = await fetch(`http://localhost:8000/users/${params}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    users.value = await res.json()
    showList.value = true
  }
}

onMounted(() => {
  fetchClasses()
})
</script>

<style scoped>
.user-management, 
.user-management * {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.user-management {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.user-mgmt-section {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.12);
  padding: 2rem;
  margin-bottom: 2rem;
}

.user-mgmt-section h2 {
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

.save-btn {
  background: #4a4e69;
}

.delete-btn {
  background: #bb0a21;
}

.delete-btn:hover {
  background: #9a0a1a;
}

.generate-btn {
  background: #4a4e69;
  white-space: nowrap;
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

.user-list {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #9a8c98;
}

.user-list-title {
  font-size: 1.1rem;
  color: #c9ada7;
  margin-bottom: 1rem;
  text-align: center;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.user-table th, .user-table td {
  border: 1px solid #9a8c98;
  padding: 0.75rem;
  text-align: left;
}

.user-table th {
  background-color: #4a4e69;
  color: #f2e9e4;
  font-weight: 500;
}

.user-table td {
  background-color: #22223b;
  color: #f2e9e4;
}

.user-table tr:nth-child(even) td {
  background-color: #2a2a42;
}

.edit-form {
  width: 100%;
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