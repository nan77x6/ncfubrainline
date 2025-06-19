<template>
  <main>
    <button class="back-btn" @click="goBack">← Назад</button>
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      Загрузка материала...
    </div>
    <div v-else-if="error" class="error">
      <!-- ...иконка и текст ошибки... -->
      {{ error }}
    </div>
    <div v-else class="material-container">
      <div class="material-header">
        <div class="header-top">
          <span class="icon">{{ subjectIcon }}</span>
          <div class="meta">
            <span class="author">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" stroke-width="2"/>
                <path d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              Тему добавил(а): {{ formattedAuthor }}
            </span>
            <span class="date">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 9H21M7 3V5M17 3V5M6 12H8M11 12H13M16 12H18M6 15H8M11 15H13M16 15H18M6 18H8M11 18H13M16 18H18M6.2 21H17.8C18.9201 21 19.4802 21 19.908 20.782C20.2843 20.5903 20.5903 20.2843 20.782 19.908C21 19.4802 21 18.9201 21 17.8V8.2C21 7.07989 21 6.51984 20.782 6.09202C20.5903 5.71569 20.2843 5.40973 19.908 5.21799C19.4802 5 18.9201 5 17.8 5H6.2C5.0799 5 4.51984 5 4.09202 5.21799C3.71569 5.40973 3.40973 5.71569 3.21799 6.09202C3 6.51984 3 7.07989 3 8.2V17.8C3 18.9201 3 19.4802 3.21799 19.908C3.40973 20.2843 3.71569 20.5903 4.09202 20.782C4.51984 21 5.07989 21 6.2 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              {{ formatDate(material.created_at) }}
            </span>
          </div>
        </div>
        <h1 class="title">{{ material.title }}</h1>
      </div>
      <div class="material-content">
        <vue-markdown :source="material.content" />
      </div>
      <div v-if="hasTest" class="test-link-block">
        <button class="test-link-btn" @click="goToThemeTests">
          Пройти тесты по теме
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import VueMarkdown from 'vue-markdown-render'

const route = useRoute()
const router = useRouter()
const material = ref({})
const loading = ref(true)
const error = ref('')
const subjectIcon = ref('📚')
const hasTest = ref(false)

const subjectIcons = [
  { keyword: 'алгебра', icon: '➗' },
  { keyword: 'английский', icon: '🇬🇧' },
  { keyword: 'биология', icon: '🧬' },
  { keyword: 'география', icon: '🌍' },
  { keyword: 'геометрия', icon: '📐' },
  { keyword: 'информатика', icon: '💻' },
  { keyword: 'история', icon: '🏺' },
  { keyword: 'литература', icon: '📖' },
  { keyword: 'обществознание', icon: '🌐' },
  { keyword: 'русский', icon: '🇷🇺' },
  { keyword: 'физика', icon: '🔬' },
  { keyword: 'химия', icon: '🧪' }
]

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const getSubjectIcon = (subjectName) => {
  const lower = subjectName?.toLowerCase() || ''
  for (const { keyword, icon } of subjectIcons) {
    if (lower.includes(keyword)) return icon
  }
  return '📚'
}

const goBack = () => {
  router.back()
}

const fetchMaterial = async () => {
  loading.value = true
  error.value = ''
  const token = localStorage.getItem('token')
  const materialId = route.params.materialId

  try {
    const materialRes = await fetch(`http://localhost:8000/materials/${materialId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!materialRes.ok) throw new Error('Материал не найден')
    material.value = await materialRes.json()

    // Проверяем, есть ли тест для этого материала
    const testRes = await fetch(`http://localhost:8000/tests/by_material/${materialId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (testRes.ok) {
      const tests = await testRes.json()
      hasTest.value = Array.isArray(tests) && tests.length > 0
    } else {
      hasTest.value = false
    }

    const themeRes = await fetch(`http://localhost:8000/themes/${material.value.theme_id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!themeRes.ok) throw new Error('Тема не найдена')
    const theme = await themeRes.json()

    const subjectsRes = await fetch(`http://localhost:8000/subjects/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!subjectsRes.ok) throw new Error('Ошибка загрузки предметов')
    const subjects = await subjectsRes.json()
    const subj = subjects.find(s => String(s.id) === String(theme.subject_id))
    subjectIcon.value = subj ? getSubjectIcon(subj.subject_name) : '📚'
  } catch (e) {
    error.value = e.message || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

const formattedAuthor = computed(() => {
  const name = material.value.created_by_full_name
  if (!name) return ''
  const parts = name.trim().split(' ')
  if (parts.length === 3) {
    return parts[1] + ' ' + parts[2]
  }
  return name
})

function goToThemeTests() {
  // Переход на страницу тестов по теме
  router.push(`/tests/materials/${material.value.theme_id}`)
}

onMounted(fetchMaterial)
</script>

<style scoped>
main {
  margin: 0 auto;
  padding-left: 1.5vw;
  padding-right: 1.5vw;
  padding-top: 6rem;
  padding-bottom: 3rem;
  max-width: 800px;
}

.back-btn {
  padding-top: 0rem;
  margin-bottom: 1rem;
  background: none;
  border: none;
  color: #22223b;
  font-size: 1.1rem;
  cursor: pointer;
  transition: color 0.15s;
}

.material-container {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(34,34,59,0.10);
  padding: 1.5rem;
  border: 1px solid #39395a;
}

.material-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #39395a;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 1rem;
}

.icon {
  font-size: 1.8rem;
  padding: 0.5rem;
  background: #292945;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  flex-shrink: 0;
  color: #fff;
  text-shadow:
    0 2px 8px #181828,
    0 0px 2px #fff,
    0 0 0.5px #fff;
  filter: drop-shadow(0 2px 4px #181828);
}

.meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #bfc0d9;
}

.meta span {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

.meta svg {
  width: 14px;
  height: 14px;
  opacity: 0.8;
  color: #bfc0d9;
}

.title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #fff;
  line-height: 1.3;
  margin: 0;
}

.material-content {
  font-size: 1rem;
  line-height: 1.7;
  color: #e9ecef;
}

.loading,
.error {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-align: center;
  padding: 1.5rem;
  font-size: 1rem;
  color: #fff;
  background: #292945;
  border-radius: 8px;
  margin-top: 1rem;
}

.error {
  color: #fa5252;
  background: #2d2d4d;
}

.error svg {
  width: 18px;
  height: 18px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid #39395a;
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.material-content :deep(h2) {
  font-size: 1.3rem;
  margin: 1.8rem 0 1rem;
  color: #fff;
  font-weight: 600;
  padding-bottom: 0.3rem;
  border-bottom: 1px solid #39395a;
}

.material-content :deep(h3) {
  font-size: 1.15rem;
  margin: 1.5rem 0 0.8rem;
  color: #fff;
  font-weight: 600;
}

.material-content :deep(p) {
  margin: 1rem 0;
  color: #e9ecef;
}

.material-content :deep(ul),
.material-content :deep(ol) {
  margin: 1rem 0;
  padding-left: 1.8rem;
  color: #e9ecef;
}

.material-content :deep(li) {
  margin: 0.5rem 0;
}

.material-content :deep(strong) {
  font-weight: 600;
  color: #fff;
}

.material-content :deep(em) {
  font-style: italic;
}

.material-content :deep(a) {
  color: #fa5252;
  text-decoration: none;
  font-weight: 500;
}

.material-content :deep(a:hover) {
  text-decoration: underline;
}

.material-content :deep(code) {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  background: #292945;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.9em;
  color: #fa5252;
}

.material-content :deep(pre) {
  background: #292945;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.2rem 0;
  border: 1px solid #39395a;
  color: #e9ecef;
}

.material-content :deep(blockquote) {
  border-left: 4px solid #fa5252;
  padding-left: 1rem;
  margin: 1.2rem 0;
  color: #bfc0d9;
  font-style: italic;
  background: #292945;
  border-radius: 6px;
}

.test-link-block {
  display: flex;
  justify-content: center; /* Центрируем кнопку */
  margin-top: 2.5rem;
}

.test-link-btn {
  background: #4a4e69;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.9rem 2.2rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(34,34,59,0.10);
  transition: background 0.18s, color 0.18s;
}
.test-link-btn:hover {
  background: #bb0a21;
  color: #fff;
}
</style>