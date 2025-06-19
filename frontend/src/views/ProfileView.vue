<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="user-info">
        <div class="user-avatar">{{ initials }}</div>
        <div class="user-details">
          <div class="user-name">{{ user.full_name }}</div>
          <div class="user-role">{{ roleName(user.role) }}</div>
        </div>
      </div>
      <nav class="admin-nav">
        <button
          v-if="user.role === 'admin'"
          class="admin-nav-btn"
          @click="openUserMgmt"
        >Управление пользователями</button>
        <button
          v-if="user.role === 'admin'"
          class="admin-nav-btn"
          @click="openClassMgmt"
        >Управление классами</button>
        <button
          v-if="user.role === 'admin'"
          class="admin-nav-btn"
          @click="openSubjectMgmt"
        >Управление предметами</button>
        <button
          v-if="user.role === 'admin' || user.role === 'teacher'"
          class="admin-nav-btn"
          @click="openThemeMgmt"
        >Управление темами</button>
        <button
          v-if="user.role === 'admin' || user.role === 'teacher'"
          class="admin-nav-btn"
          @click="openMaterialMgmt"
        >Управление материалом</button>
        <button
          v-if="user.role === 'admin' || user.role === 'teacher'"
          class="admin-nav-btn"
          @click="openTestMgmt"
        >
          Управление тестами
        </button>
        <button
          v-if="user.role === 'admin' || user.role === 'teacher'"
          class="admin-nav-btn"
          @click="openMediaMgmt"
        >
          Управление медиа
        </button>
        <button
          v-if="user.role === 'admin' || user.role === 'student'"
          class="admin-nav-btn"
          @click="openResults"
        >
          Результаты
        </button>
        <button
          v-if="user.role === 'admin' || user.role === 'teacher'"
          class="admin-nav-btn"
          @click="openResultsTeacher"
        >
          Результаты по классам
        </button>
      </nav>
    </aside>
    <main class="admin-content">
      <UserManagement v-if="showUserMgmt && user.role === 'admin'" />
      <ClassManagement v-if="showClassMgmt && user.role === 'admin'" />
      <SubjectManagement v-if="showSubjectMgmt && user.role === 'admin'" />
      <ThemeManagement v-if="showThemeMgmt && (user.role === 'admin' || user.role === 'teacher')" />
      <MaterialManagement v-if="showMaterialMgmt && (user.role === 'admin' || user.role === 'teacher')" />
      <TestManagement v-if="showTestMgmt && (user.role === 'admin' || user.role === 'teacher')" />
      <ResultsView v-if="showResults && (user.role === 'student' || user.role === 'admin')" />
      <ResultsTeacherView v-if="showResultsTeacher && (user.role === 'teacher' || user.role === 'admin')" />
      <MediaManagement v-if="showMediaMgmt && (user.role === 'admin' || user.role === 'teacher')" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import UserManagement from '../components/UserManagement.vue'
import ClassManagement from '../components/ClassManagement.vue'
import SubjectManagement from '../components/SubjectManagement.vue'
import ThemeManagement from '../components/ThemeManagement.vue'
import MaterialManagement from '../components/MaterialManagement.vue'
import TestManagement from '../components/TestManagement.vue'
import ResultsView from '@/components/ResultsView.vue'
import ResultsTeacherView from '@/components/ResultsTeacherView.vue'
import MediaManagement from '@/components/MediaManagement.vue'

const router = useRouter()

const user = ref({ full_name: '', role: '' })
const showUserMgmt = ref(false)
const showClassMgmt = ref(false)
const showSubjectMgmt = ref(false)
const showThemeMgmt = ref(false)
const showMaterialMgmt = ref(false)
const showTestMgmt = ref(false)
const showResults = ref(false)
const showResultsTeacher = ref(false)
const showMediaMgmt = ref(false)

function openUserMgmt() {
  showUserMgmt.value = true
  showClassMgmt.value = false
  showSubjectMgmt.value = false
  showThemeMgmt.value = false
  showMaterialMgmt.value = false
  showTestMgmt.value = false
  showResults.value = false
  showResultsTeacher.value = false
  showMediaMgmt.value = false
}
function openClassMgmt() {
  showClassMgmt.value = true
  showUserMgmt.value = false
  showSubjectMgmt.value = false
  showThemeMgmt.value = false
  showMaterialMgmt.value = false
  showTestMgmt.value = false
  showResults.value = false
  showResultsTeacher.value = false
  showMediaMgmt.value = false
}
function openSubjectMgmt() {
  showSubjectMgmt.value = true
  showUserMgmt.value = false
  showClassMgmt.value = false
  showThemeMgmt.value = false
  showMaterialMgmt.value = false
  showTestMgmt.value = false
  showResults.value = false
  showResultsTeacher.value = false
  showMediaMgmt.value = false
}
function openThemeMgmt() {
  showThemeMgmt.value = true
  showUserMgmt.value = false
  showClassMgmt.value = false
  showSubjectMgmt.value = false
  showMaterialMgmt.value = false
  showTestMgmt.value = false
  showResults.value = false
  showResultsTeacher.value = false
  showMediaMgmt.value = false
}
function openMaterialMgmt() {
  showMaterialMgmt.value = true
  showUserMgmt.value = false
  showClassMgmt.value = false
  showSubjectMgmt.value = false
  showThemeMgmt.value = false
  showTestMgmt.value = false
  showResults.value = false
  showResultsTeacher.value = false
  showMediaMgmt.value = false
}
function openTestMgmt() {
  showTestMgmt.value = true
  showUserMgmt.value = false
  showClassMgmt.value = false
  showSubjectMgmt.value = false
  showThemeMgmt.value = false
  showMaterialMgmt.value = false
  showResults.value = false
  showResultsTeacher.value = false
  showMediaMgmt.value = false
}
function openResults() {
  showResults.value = true
  showResultsTeacher.value = false
  showUserMgmt.value = false
  showClassMgmt.value = false
  showSubjectMgmt.value = false
  showThemeMgmt.value = false
  showMaterialMgmt.value = false
  showTestMgmt.value = false
  showMediaMgmt.value = false
}
function openResultsTeacher() {
  showResultsTeacher.value = true
  showResults.value = false
  showUserMgmt.value = false
  showClassMgmt.value = false
  showSubjectMgmt.value = false
  showThemeMgmt.value = false
  showMaterialMgmt.value = false
  showTestMgmt.value = false
  showMediaMgmt.value = false
}
function openMediaMgmt() {
  showMediaMgmt.value = true
  showResultsTeacher.value = false
  showResults.value = false
  showUserMgmt.value = false
  showClassMgmt.value = false
  showSubjectMgmt.value = false
  showThemeMgmt.value = false
  showMaterialMgmt.value = false
  showTestMgmt.value = false
}

function roleName(role) {
  if (role === 'admin') return 'Администратор'
  if (role === 'teacher') return 'Учитель'
  if (role === 'student') return 'Ученик'
  return role
}

// Получаем данные только о текущем пользователе
onMounted(async () => {
  const token = localStorage.getItem('token')
  const response = await fetch('http://localhost:8000/users/me', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (response.ok) {
    user.value = await response.json()
  }
})

// Инициалы для аватара
const initials = computed(() => {
  if (!user.value.full_name) return ''
  return user.value.full_name
    .split(' ')
    .map(w => w[0]?.toUpperCase())
    .join('')
    .slice(0, 2)
})
</script>

<style scoped>

.admin-layout {
  display: flex;
  min-height: calc(100vh - var(--navbar-height));
  margin-top: var(--navbar-height);
  background: #f2e9e4;
}
.sidebar {
  position: fixed;
  top: var(--navbar-height);
  left: 0;
  width: var(--sidebar-width);
  height: calc(100vh - var(--navbar-height));
  background: #22223b;
  color: #f2e9e4;
  padding: 2rem 1.2rem 1.2rem 1.2rem;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  box-shadow: 2px 0 10px rgba(34,34,59,0.05);
  z-index: 10;
  overflow-y: auto;
}
.admin-content {
  flex: 1;
  padding: 2.5rem 2rem;
  margin-left: var(--sidebar-width);
  min-height: 100%;
}
.user-info {
  display: flex;
  align-items: center;
  margin-top: 1.2rem;
  gap: 1rem;
}
.user-avatar {
  width: 48px;
  height: 48px;
  background: #9a8c98;
  color: #22223b;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.5rem;
  letter-spacing: 1px;
}
.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}
.user-name {
  font-weight: bold;
  font-size: 1.08rem;
  color: #f2e9e4;
}
.user-role {
  font-size: 0.98rem;
  color: #c9ada7;
}
.admin-nav {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  margin-top: 1.5rem;
}
.admin-nav-btn {
  background: none;
  border: none;
  color: #f2e9e4;
  font-size: 1.05rem;
  text-align: center;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.18s;
  border-bottom: 2px solid #9a8c98;
}
.admin-nav-btn:hover {
  background: #4a4e69;
}
.navbar {
  z-index: 100;
}
</style>
