<template>
  <div class="subject-management">
    <!-- 1. Создать новый предмет -->
    <section class="subject-mgmt-section">
      <h2>Создать новый предмет</h2>
      <div class="form-row">
        <div class="form-group">
          <input v-model="createName" placeholder="Название предмета" class="form-input" />
        </div>
        <button @click="createSubject" class="action-btn">Добавить</button>
      </div>
      <div v-if="createResult" class="result-message">{{ createResult }}</div>
    </section>

    <!-- 2. Изменить предмет -->
    <section class="subject-mgmt-section">
      <h2>Изменить предмет</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="editId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <input v-model="editName" placeholder="Новое название" class="form-input" />
        </div>
        <button @click="updateSubject" class="action-btn">Изменить</button>
      </div>
      <div v-if="editResult" class="result-message">{{ editResult }}</div>
    </section>

    <!-- 3. Удалить предмет -->
    <section class="subject-mgmt-section">
      <h2>Удалить предмет</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="deleteId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <button @click="deleteSubject" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="deleteResult" class="result-message">{{ deleteResult }}</div>
    </section>

    <!-- 4. Назначить учителя на предмет -->
    <section class="subject-mgmt-section">
      <h2>Назначить учителя на предмет</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="assignSubjectId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="assignTeacherId" class="form-select">
            <option disabled value="">Выберите учителя</option>
            <option
              v-for="teacher in sortedTeachers"
              :key="teacher.id"
              :value="teacher.id"
              :class="{ unassigned: !teacher.has_subject }"
            >
              {{ teacher.full_name }} <span v-if="!teacher.has_subject">— (без предмета)</span>
            </option>
          </select>
        </div>
        <button @click="assignTeacher" class="action-btn">Назначить</button>
      </div>
      <div v-if="assignResult" class="result-message">{{ assignResult }}</div>
    </section>

    <!-- 5. Удалить учителя из управления предметом -->
    <section class="subject-mgmt-section">
      <h2>Удалить учителя из управления предметом</h2>
      <div class="form-row">
        <div class="form-group">
          <select v-model="removeSubjectId" @focus="fetchSubjects" class="form-select">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">
              {{ subj.subject_name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="removeTeacherId" class="form-select">
            <option v-for="teacher in subjectTeachers" :key="teacher.id" :value="teacher.id">
              {{ teacher.full_name }}
            </option>
          </select>
        </div>
        <button @click="removeTeacher" class="action-btn delete-btn">Удалить</button>
      </div>
      <div v-if="removeResult" class="result-message">{{ removeResult }}</div>
    </section>

    <!-- 6. Посмотреть список предметов и назначенных на них учителей -->
    <section class="subject-mgmt-section">
      <h2>Посмотреть список предметов и назначенных на них учителей</h2>
      <div class="form-row">
        <button v-if="!showList" @click="fetchSubjectList" class="action-btn">Показать</button>
        <button v-if="showList" @click="showList = false" class="action-btn">Скрыть</button>
      </div>
      <div v-if="showList" class="subject-list">
        <table class="subject-table">
          <thead>
            <tr>
              <th>Предмет</th>
              <th>Учителя</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subj in subjectList" :key="subj.id">
              <td>{{ subj.subject_name }}</td>
              <td>
                <span v-if="subj.teachers.length === 0">—</span>
                <span v-else>{{ subj.teachers.map(t => t.full_name).join(', ') }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'

const subjects = ref([])
const teachers = ref([])
const subjectTeachers = ref([])
const subjectList = ref([])

const createName = ref('')
const createResult = ref('')
const editId = ref('')
const editName = ref('')
const editResult = ref('')
const deleteId = ref('')
const deleteResult = ref('')

const assignSubjectId = ref('')
const assignTeacherId = ref('')
const assignResult = ref('')

const removeSubjectId = ref('')
const removeTeacherId = ref('')
const removeResult = ref('')

const showList = ref(false)

async function fetchSubjects() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/subjects/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjects.value = await res.json()
  }
}

async function fetchTeachers() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/users/teachers_with_flag/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    teachers.value = await res.json()
  }
}

watch(removeSubjectId, async (newVal) => {
  removeTeacherId.value = ''
  if (!newVal) {
    subjectTeachers.value = []
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/subjects/${newVal}/teachers`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjectTeachers.value = await res.json()
  }
})

const sortedTeachers = computed(() => {
  return [...teachers.value].sort((a, b) => {
    if (a.has_subject === b.has_subject) {
      return a.full_name.localeCompare(b.full_name, 'ru')
    }
    return a.has_subject ? 1 : -1
  })
})

async function createSubject() {
  createResult.value = ''
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/subjects/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ subject_name: createName.value })
  })
  if (res.ok) {
    createResult.value = 'Предмет создан'
    createName.value = ''
    fetchSubjects()
  } else {
    const data = await res.json()
    createResult.value = data.detail || 'Ошибка создания'
  }
}

async function updateSubject() {
  editResult.value = ''
  if (!editId.value || !editName.value) {
    editResult.value = 'Выберите предмет и введите новое название'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/subjects/${editId.value}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ subject_name: editName.value })
  })
  if (res.ok) {
    editResult.value = 'Предмет изменён'
    editId.value = ''
    editName.value = ''
    fetchSubjects()
  } else {
    const data = await res.json()
    editResult.value = data.detail || 'Ошибка изменения'
  }
}

async function deleteSubject() {
  deleteResult.value = ''
  if (!deleteId.value) {
    deleteResult.value = 'Выберите предмет'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/subjects/${deleteId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    deleteResult.value = 'Предмет удалён'
    deleteId.value = ''
    fetchSubjects()
  } else {
    const data = await res.json()
    deleteResult.value = data.detail || 'Ошибка удаления'
  }
}

async function assignTeacher() {
  assignResult.value = ''
  if (!assignSubjectId.value || !assignTeacherId.value) {
    assignResult.value = 'Выберите предмет и учителя'
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch(
    `http://localhost:8000/user-subjects/?user_id=${Number(assignTeacherId.value)}&subject_id=${Number(assignSubjectId.value)}`,
    {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    }
  )
  if (res.ok) {
    assignResult.value = 'Учитель назначен на предмет'
    assignSubjectId.value = ''
    assignTeacherId.value = ''
    fetchTeachers()
  } else {
    const data = await res.json()
    assignResult.value = data.detail || 'Ошибка назначения'
  }
}

async function removeTeacher() {
  removeResult.value = ''
  if (!removeSubjectId.value || !removeTeacherId.value) {
    removeResult.value = 'Выберите предмет и учителя'
    return
  }
  const token = localStorage.getItem('token')
  const teacherId = typeof removeTeacherId.value === 'object' ? removeTeacherId.value.id : removeTeacherId.value
  const subjectId = typeof removeSubjectId.value === 'object' ? removeSubjectId.value.id : removeSubjectId.value

  const res = await fetch(`http://localhost:8000/user-subjects/?user_id=${teacherId}&subject_id=${subjectId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    removeResult.value = 'Учитель удалён из предмета'
    removeTeacherId.value = ''
    const res2 = await fetch(`http://localhost:8000/subjects/${removeSubjectId.value}/teachers`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (res2.ok) {
      subjectTeachers.value = await res2.json()
    }
    fetchTeachers()
  } else {
    const data = await res.json()
    removeResult.value = data.detail || 'Ошибка удаления'
  }
}

async function fetchSubjectList() {
  showList.value = false
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/subjects/with-teachers', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    subjectList.value = await res.json()
    showList.value = true
  }
}

onMounted(() => {
  fetchSubjects()
  fetchTeachers()
})
</script>

<style scoped>
.subject-management, 
.subject-management * {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.subject-management {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.subject-mgmt-section {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.12);
  padding: 2rem;
  margin-bottom: 2rem;
}

.subject-mgmt-section h2 {
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

/* Центрирование кнопки "Показать" и "Скрыть" только для блока списка */
.subject-mgmt-section:last-of-type .form-row {
  justify-content: center;
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

.unassigned {
  font-weight: bold;
  color: #f2e9e4;
  background: #4a4e69;
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

.subject-list {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #9a8c98;
  width: 100%;
}

.subject-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.subject-table th, .subject-table td {
  border: 1px solid #9a8c98;
  padding: 0.75rem;
  text-align: left;
}

.subject-table th {
  background-color: #4a4e69;
  color: #f2e9e4;
  font-weight: 500;
}

.subject-table td {
  background-color: #22223b;
  color: #f2e9e4;
}

.subject-table tr:nth-child(even) td {
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