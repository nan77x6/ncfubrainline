<template>
  <main class="test-main" v-if="testLoaded">
    <div class="test-card">
      <button class="back-btn" @click="goBack">← Назад</button>
      <h1 class="test-title">{{ test.title }}</h1>
      <form v-if="questions.length && !finished" @submit.prevent="submitTest" class="test-form">
        <div
          v-for="(q, idx) in questions"
          :key="q.id"
          class="question-block"
        >
          <div class="question-title">
            <span class="question-number">Вопрос {{ idx + 1 }}:</span> {{ q.question_text }}
          </div>
          <!-- Один правильный -->
          <div v-if="q.question_type === 'single'" class="options-list">
            <label
              v-for="(opt, oidx) in q.shuffledOptions"
              :key="oidx"
              class="option-label"
            >
              <input
                type="radio"
                :name="'q' + q.id"
                :value="oidx"
                v-model="answers[q.id]"
                required
              />
              <span class="option-text">{{ opt.option_text }}</span>
            </label>
          </div>
          <!-- Несколько правильных -->
          <div v-else-if="q.question_type === 'multiple'" class="options-list">
            <label
              v-for="(opt, oidx) in q.shuffledOptions"
              :key="oidx"
              class="option-label"
            >
              <input
                type="checkbox"
                :value="oidx"
                v-model="answers[q.id]"
              />
              <span class="option-text">{{ opt.option_text }}</span>
            </label>
          </div>
          <!-- Соответствие -->
          <div v-else-if="q.question_type === 'match'" class="match-list">
            <div
              v-for="(pair, pidx) in q.shuffledPairs"
              :key="pidx"
              class="match-row"
            >
              <span class="match-left">{{ pair.left_text }}</span>
              <select v-model="answers[q.id][pidx]" class="match-select">
                <option disabled value="">Выберите...</option>
                <option
                  v-for="(right, ridx) in q.rightOptions"
                  :key="ridx"
                  :value="right"
                >{{ right }}</option>
              </select>
            </div>
          </div>
        </div>
        <button class="submit-btn" type="submit">Завершить тест</button>
      </form>
      <div v-if="finished" class="result-block">
        <h2 class="result-title">Результат</h2>
        <div class="result-stats">
          <div class="stat-item">
            <span class="stat-label">Правильных ответов:</span>
            <span class="stat-value">{{ correctCount }} из {{ questions.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Процент:</span>
            <span class="stat-value">{{ percent }}%</span>
          </div>
        </div>
        <div v-if="saveResultStatus" class="save-status" :class="{ error: saveResultStatus.includes('Ошибка') }">
          {{ saveResultStatus }}
        </div>
        <button class="back-btn result-back-btn" @click="goBack">Назад</button>
      </div>
    </div>
  </main>
  <div v-else class="loading-block">
    <div class="loading-spinner"></div>
    <p>Загрузка теста...</p>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const testId = route.params.testId

const test = ref({})
const questions = ref([])
const answers = reactive({})
const finished = ref(false)
const correctCount = ref(0)
const percent = ref(0)
const testLoaded = ref(false)
const saveResultStatus = ref('')

function shuffle(arr) {
  return arr
    .map((a) => [Math.random(), a])
    .sort((a, b) => a[0] - b[0])
    .map((a) => a[1])
}

async function fetchTest() {
  const token = localStorage.getItem('token')
  // Получить тест
  const res = await fetch(`http://localhost:8000/tests/${testId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    test.value = await res.json()
  }
  // Получить вопросы
  const qres = await fetch(`http://localhost:8000/tests/questions/${testId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (qres.ok) {
    let qs = await qres.json()
    // Перемешать вопросы
    qs = shuffle(qs)
    // Для каждого вопроса получить варианты/пары и перемешать
    for (const q of qs) {
      if (q.question_type === 'single' || q.question_type === 'multiple') {
        const optRes = await fetch(`http://localhost:8000/test_options/${q.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (optRes.ok) {
          const opts = await optRes.json()
          q.shuffledOptions = shuffle(opts)
        } else {
          q.shuffledOptions = []
        }
        // Инициализация ответов
        if (q.question_type === 'single') {
          answers[q.id] = null
        } else {
          answers[q.id] = []
        }
      } else if (q.question_type === 'match') {
        const pairRes = await fetch(`http://localhost:8000/test_pairs/${q.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (pairRes.ok) {
          const pairs = await pairRes.json()
          q.shuffledPairs = shuffle(pairs)
          // Для селектов справа перемешиваем отдельно
          q.rightOptions = shuffle(pairs.map(p => p.right_text))
        } else {
          q.shuffledPairs = []
          q.rightOptions = []
        }
        answers[q.id] = Array(q.shuffledPairs.length).fill('')
      }
    }
    questions.value = qs
  }
  testLoaded.value = true
}

onMounted(fetchTest)

async function submitTest() {
  finished.value = true
  let correct = 0
  for (const q of questions.value) {
    if (q.question_type === 'single') {
      // Найти правильный вариант
      const idx = q.shuffledOptions.findIndex(o => o.is_correct)
      if (Number(answers[q.id]) === idx) correct++
    } else if (q.question_type === 'multiple') {
      // Сравнить массивы правильных индексов
      const correctIdxs = q.shuffledOptions
        .map((o, i) => (o.is_correct ? i : -1))
        .filter(i => i !== -1)
      const userIdxs = Array.isArray(answers[q.id]) ? answers[q.id].map(Number).sort() : []
      if (
        userIdxs.length === correctIdxs.length &&
        userIdxs.every((v, i) => v === correctIdxs[i])
      ) {
        correct++
      }
    } else if (q.question_type === 'match') {
      let allMatch = true
      for (let i = 0; i < q.shuffledPairs.length; i++) {
        if (answers[q.id][i] !== q.shuffledPairs[i].right_text) {
          allMatch = false
          break
        }
      }
      if (allMatch) correct++
    }
  }
  correctCount.value = correct
  percent.value = Math.round((correct / questions.value.length) * 100)
  await saveResult()
}

async function saveResult() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/test_results/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      test_id: Number(testId),
      correct_answers: correctCount.value,
      total_questions: questions.value.length,
      percent: percent.value
    })
  })
  if (res.ok) {
    saveResultStatus.value = 'Результат сохранён!'
  } else {
    saveResultStatus.value = 'Ошибка при сохранении результата'
  }
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.test-main {
  min-height: 100vh;
  background: #f2e9e4;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.test-card {
  background: #22223b;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(34,34,59,0.18);
  padding: 2.5rem 2rem 2.5rem 2rem;
  margin: 3rem 0;
  max-width: 700px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  border: 2px solid #4a4e69;
}
.back-btn {
  align-self: flex-start;
  margin-bottom: 1.5rem;
  background: none;
  border: none;
  color: #f2e9e4;
  font-size: 1.1rem;
  cursor: pointer;
  transition: color 0.15s, background 0.15s;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}
.back-btn:hover {
  color: #bb0a21;
  background: #4a4e69;
}
.test-title {
  color: #f2e9e4;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 700;
  padding-bottom: 1rem;
  border-bottom: 2px solid #c9ada7;
}
.test-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.question-block {
  background-color: #4a4e69;
  border-radius: 14px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(34, 34, 59, 0.10);
  margin-bottom: 1.5rem;
  border: 1px solid #9a8c98;
}
.question-title {
  font-size: 1.2rem;
  color: #f2e9e4;
  margin-bottom: 1.2rem;
  line-height: 1.4;
}
.question-number {
  font-weight: 600;
  color: #c9ada7;
}
.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}
.option-label {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1rem;
  background-color: #f2e9e4;
  border-radius: 8px;
  border: 1px solid #c9ada7;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #22223b;
}
.option-label:hover {
  background-color: #c9ada7;
  border-color: #bb0a21;
  color: #22223b;
}
.option-text {
  flex: 1;
}
input[type="radio"],
input[type="checkbox"] {
  width: 1.2rem;
  height: 1.2rem;
  accent-color: #bb0a21;
}
.match-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.match-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}
.match-left {
  min-width: 150px;
  font-weight: 500;
  color: #f2e9e4;
}
.match-select {
  flex: 1;
  min-width: 200px;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: 1px solid #c9ada7;
  background-color: #f2e9e4;
  color: #22223b;
  font-size: 1rem;
}
.match-select:focus {
  outline: none;
  border-color: #bb0a21;
  box-shadow: 0 0 0 2px rgba(187, 10, 33, 0.13);
}
.submit-btn {
  margin: 1rem auto 0;
  padding: 0.8rem 2.5rem;
  background-color: #bb0a21;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s;
}
.submit-btn:hover {
  background-color: #9a8c98;
  color: #22223b;
}
.result-block {
  background-color: #4a4e69;
  border-radius: 14px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(34, 34, 59, 0.1);
  margin-top: 2rem;
  border: 1px solid #9a8c98;
}
.result-title {
  color: #f2e9e4;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}
.result-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-item {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}
.stat-label {
  color: #c9ada7;
  font-weight: 500;
}
.stat-value {
  color: #f2e9e4;
  font-weight: 600;
}
.save-status {
  margin: 1.5rem 0;
  padding: 0.8rem;
  border-radius: 6px;
  background-color: #f2e9e4;
  color: #4a4e69;
  font-weight: 500;
}
.save-status.error {
  background-color: rgba(187, 10, 33, 0.1);
  color: #bb0a21;
}
.result-back-btn {
  margin: 0 auto;
  background-color: #c9ada7;
  color: #22223b;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 2rem;
  font-size: 1rem;
  margin-top: 1.5rem;
  transition: background 0.18s, color 0.18s;
}
.result-back-btn:hover {
  background-color: #bb0a21;
  color: #fff;
}
.loading-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: #4a4e69;
}
.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f2e9e4;
  border-top-color: #4a4e69;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>