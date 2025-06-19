<template>
  <main>
    <button class="back-btn" @click="goBack">← Назад</button>
    <div class="themes-grid">
      <div
        v-for="material in sortedMaterials"
        :key="material.id"
        class="tile"
        @click="openMaterial(material.id)"
      >
        <div class="icon">{{ subjectIcon }}📎📄</div>
        <div class="name">{{ material.title }}</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const materials = ref([])
const subjectIcon = ref('📚')

const API_URL = import.meta.env.VITE_API_URL; // добавьте эту строку

// Тот же список иконок, что и в SubjectThemesView.vue
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
  const lower = subjectName?.toLowerCase() || ''
  for (const { keyword, icon } of subjectIcons) {
    if (lower.includes(keyword)) return icon
  }
  return '📚'
}

async function fetchMaterials() {
  const token = getToken()
  if (!token) return
  const themeId = route.params.themeId
  // Получаем материалы
  const res = await fetch(`${API_URL}/materials/by_theme/${themeId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    materials.value = await res.json()
  }
  // Получаем название предмета для иконки (как в SubjectThemesView.vue)
  const resTheme = await fetch(`${API_URL}/themes/${themeId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (resTheme.ok) {
    const theme = await resTheme.json()
    // Получаем все предметы, чтобы найти нужный
    const resSubjects = await fetch(`${API_URL}/subjects/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (resSubjects.ok) {
      const subjects = await resSubjects.json()
      const subj = subjects.find(s => String(s.id) === String(theme.subject_id))
      subjectIcon.value = subj ? getSubjectIcon(subj.subject_name) : '📚'
    }
  }
}

function goBack() {
  router.back()
}

function openMaterial(materialId) {
  router.push(`/materials/${materialId}`)
}

const sortedMaterials = computed(() =>
  [...materials.value].sort((a, b) => b.id - a.id)
)

onMounted(fetchMaterials)
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
    0 2px 8px #181828,
    0 0px 2px #fff,
    0 0 0.5px #fff;
  filter: drop-shadow(0 2px 4px #181828);
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
}
.name {
  font-size: 1.3rem;
  font-weight: 600;
  color: #fff;
  text-align: center;
}
</style>