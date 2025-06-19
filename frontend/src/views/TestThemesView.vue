<template>
  <main>
    <button class="back-btn" @click="goBack">← Назад</button>
    <h1>Темы с тестами</h1>
    <div class="themes-grid">
      <div
        v-for="theme in sortedThemesWithTests"
        :key="theme.id"
        class="theme-tile"
        @click="goToThemeMaterials(theme.id)"
      >
        <div class="icon">📎</div>
        <div class="name">{{ theme.theme_name }}</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const themesWithTests = ref([])
const router = useRouter()
const route = useRoute()

async function fetchThemesWithTests() {
  const subjectId = route.params.subjectId
  const token = localStorage.getItem('token')
  if (!subjectId || !token) return
  // Получаем только темы, для которых есть материалы с тестами
  const res = await fetch(`http://localhost:8000/themes/with_tests/${subjectId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    // [{id, theme_name, max_test_id}]
    themesWithTests.value = await res.json()
  }
}

const sortedThemesWithTests = computed(() =>
  [...themesWithTests.value].sort((a, b) => (b.max_test_id || 0) - (a.max_test_id || 0))
)

function goToThemeMaterials(themeId) {
  router.push(`/tests/materials/${themeId}`)
}

function goBack() {
  router.back()
}

onMounted(fetchThemesWithTests)
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
h1 {
  font-size: 2.2rem;
  margin-bottom: 2.2rem;
  color: #22223b;
  text-align: center;
}
.themes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2.5rem;
  justify-content: start;
  margin-top: 0rem;
}
.theme-tile {
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
.theme-tile:hover {
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
}
.name { 
  font-size: 1.5rem;
  font-weight: 600;
  color: #fff;
  text-align: center;
  margin-bottom: 0.7rem;
}
</style>