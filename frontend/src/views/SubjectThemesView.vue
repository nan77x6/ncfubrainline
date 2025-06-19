<template>
  <main>
    <button class="back-btn" @click="goBack">← Назад</button>
    <div class="themes-grid">
      <div
        v-for="theme in sortedThemes"
        :key="theme.id"
        class="tile"
        @click="goToMaterials(theme.id)"
      >
        <div class="icon">{{ subjectIcon }} 📎</div>
        <div class="name">{{ theme.theme_name }}</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const themes = ref([])
const subjectIcon = ref('➗')

// Список иконок как в SubjectsView.vue
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

function getToken() {
  return localStorage.getItem('token')
}

function getSubjectIcon(subjectName) {
  const lower = subjectName.toLowerCase()
  for (const { keyword, icon } of subjectIcons) {
    if (lower.includes(keyword)) return icon
  }
  return '📚'
}

async function fetchThemes() {
  const token = getToken()
  if (!token) return
  const subjectId = route.params.subjectId
  // Получаем темы
  const res = await fetch(`http://localhost:8000/themes/by_subject/${subjectId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    themes.value = await res.json()
  }
  // Получаем название предмета для иконки
  const resSubj = await fetch(`http://localhost:8000/subjects/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (resSubj.ok) {
    const subjects = await resSubj.json()
    const subj = subjects.find(s => String(s.id) === String(subjectId))
    subjectIcon.value = subj ? getSubjectIcon(subj.subject_name) : '📚'
  }
}

function goToMaterials(themeId) {
  router.push(`/themes/${themeId}/materials`)
}

function goBack() {
  router.back()
}

const sortedThemes = computed(() =>
  [...themes.value].sort((a, b) => b.id - a.id)
)

onMounted(fetchThemes)
</script>

<style scoped>
main {
  margin: 0 auto;
  padding-left: 1.5vw;
  padding-right: 1.5vw;
  padding-top: 6rem;
  padding-bottom: 3rem;
}

.back-btn {
  padding-top: 0rem;
  margin-bottom: 1rem;
  background: none;
  border: none;
  color: #23233b;
  font-size: 1.1rem;
  cursor: pointer;
  transition: color 0.15s;
}

.themes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2.5rem;
  justify-content: start;
  margin-top: 0rem;
}
.tile {
  background: #22223b;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(34,34,59,0.10);
  padding: 2rem 2.5rem;
  width: 100%;
  max-width: 350px;
  height: 235px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 0.18s, transform 0.18s, background 0.18s, border 0.18s;
  justify-content: center;
  box-sizing: border-box;
  border: 2px solid #22223b;
}
.tile:hover {
  box-shadow: 0 8px 24px rgba(34,34,59,0.18);
  transform: translateY(-6px) scale(1.04);
  background: #4a4e69;
  border-color: #bb0a21;
}
.icon {
  font-size: 3rem;
  margin-bottom: 1.2rem;
  color: #fff;
  text-shadow:
    0 2px 4px rgba(0, 0, 0, 0.3),
    0 4px 8px rgba(0, 0, 0, 0.2);
}
.name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #fff;
  text-align: center; 
}
</style>