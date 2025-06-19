<template>
  <main>
    <h1>Тесты по предметам</h1>
    <div class="tests-grid">
      <div
        v-for="subject in sortedSubjectsWithTests"
        :key="subject.id"
        class="test-tile"
        @click="goToSubjectTests(subject.id)"
      >
        <div class="icon">{{ getSubjectIcon(subject.subject_name) }}</div>
        <div class="name">{{ subject.subject_name }}</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const subjectsWithTests = ref([])
const router = useRouter()

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

function getSubjectIcon(name) {
  const lower = name.toLowerCase()
  for (const { keyword, icon } of subjectIcons) {
    if (lower.includes(keyword)) return icon
  }
  return '📚'
}

function getToken() {
  return localStorage.getItem('token')
}

// Получаем предметы с максимальным id теста для сортировки
async function fetchSubjectsWithTests() {
  const token = getToken()
  if (!token) return
  const res = await fetch('http://localhost:8000/subjects/with_tests', {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    // Ожидаем, что бэкенд вернёт [{id, subject_name, max_test_id}]
    subjectsWithTests.value = await res.json()
  }
}

const sortedSubjectsWithTests = computed(() =>
  [...subjectsWithTests.value].sort((a, b) => (b.max_test_id || 0) - (a.max_test_id || 0))
)

function goToSubjectTests(subjectId) {
  router.push(`/tests/subject/${subjectId}`)
}

onMounted(fetchSubjectsWithTests)
</script>

<style scoped>
main {
  margin: 0 auto;
  padding-left: 1.5vw;
  padding-right: 1.5vw;
  padding-top: 6rem;
  padding-bottom: 3rem;
}
h1 {
  font-size: 2.2rem;
  margin-bottom: 2.2rem;
  color: #22223b;
  text-align: center;
}
.tests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2.5rem;
  justify-content: start;
  margin-top: 0rem;
}
.test-tile {
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
.test-tile:hover {
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