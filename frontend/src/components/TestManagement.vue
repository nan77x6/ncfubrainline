<template>
  <div class="test-management">
    <!-- === Добавить/Редактировать тест === -->
    <section class="test-mgmt-section">
      <h2>{{ editingTestId ? 'Редактировать тест' : 'Создать новый тест' }}</h2>
      
      <!-- Выбор предмета, темы и материала -->
      <div class="selection-row">
        <div class="select-group">
          <label>Предмет</label>
          <select v-model="add.subjectId" @change="fetchAddThemes" class="form-select" :disabled="editingTestId">
            <option disabled value="">Выберите предмет</option>
            <option v-for="subj in subjects" :key="subj.id" :value="subj.id">{{ subj.subject_name }}</option>
          </select>
        </div>
        
        <div class="select-group">
          <label>Тема</label>
          <select v-model="add.themeId" @change="fetchAddMaterials" :disabled="!add.subjectId || editingTestId" class="form-select">
            <option disabled value="">Выберите тему</option>
            <option v-for="theme in add.themes" :key="theme.id" :value="theme.id">{{ theme.theme_name }}</option>
          </select>
        </div>
        
        <div class="select-group">
          <label>Материал</label>
          <select v-model="add.materialId" :disabled="!add.themeId || editingTestId" class="form-select">
            <option disabled value="">Выберите материал</option>
            <option v-for="mat in add.materials" :key="mat.id" :value="mat.id">{{ mat.title }}</option>
          </select>
        </div>
      </div>
      
      <!-- Название теста -->
      <div class="form-group">
        <label>Название теста</label>
        <input v-model="add.title" placeholder="Введите название теста" class="form-input" />
      </div>
      
      <!-- Форма вопроса -->
      <div class="question-form">
        <div class="form-group">
          <label>Вопрос</label>
          <textarea v-model="add.currentQuestion.text" placeholder="Введите текст вопроса" class="form-textarea"></textarea>
        </div>
        
        <div class="form-group">
          <label>Тип вопроса</label>
          <select v-model="add.currentQuestion.type" class="form-select">
            <option value="single">Один правильный ответ</option>
            <option value="multiple">Несколько правильных ответов</option>
            <option value="match">Соответствие</option>
          </select>
        </div>
        
        <!-- Варианты ответов -->
        <div v-if="add.currentQuestion.type === 'single' || add.currentQuestion.type === 'multiple'" class="options-container">
          <div class="option-item" v-for="(option, idx) in add.currentQuestion.options" :key="idx">
            <input v-model="option.text" placeholder="Текст варианта" class="form-input option-input" />
            <div class="option-controls">
              <input
                v-if="add.currentQuestion.type === 'single'"
                type="radio"
                :name="'single-correct'"
                v-model="add.currentQuestion.correct"
                :value="idx"
                class="option-checkbox"
              />
              <input
                v-if="add.currentQuestion.type === 'multiple'"
                type="checkbox"
                v-model="option.correct"
                class="option-checkbox"
              />
              <button @click.prevent="removeOption(idx)" class="remove-option-btn" title="Удалить вариант">
                <svg width="16" height="16" viewBox="0 0 16 16"><line x1="3" y1="3" x2="13" y2="13" stroke="currentColor" stroke-width="2"/><line x1="13" y1="3" x2="3" y2="13" stroke="currentColor" stroke-width="2"/></svg>
              </button>
            </div>
          </div>
          <button @click.prevent="addOption" class="add-option-btn">
            <svg width="16" height="16" viewBox="0 0 16 16"><line x1="8" y1="3" x2="8" y2="13" stroke="currentColor" stroke-width="2"/><line x1="3" y1="8" x2="13" y2="8" stroke="currentColor" stroke-width="2"/></svg>
            Добавить вариант
          </button>
        </div>
        
        <!-- Пары соответствия -->
        <div v-if="add.currentQuestion.type === 'match'" class="pairs-container">
          <div v-for="(pair, idx) in add.currentQuestion.pairs" :key="idx" class="pair-item">
            <input v-model="pair.left" placeholder="Левая часть" class="form-input pair-input" />
            <span class="pair-arrow">→</span>
            <input v-model="pair.right" placeholder="Правая часть" class="form-input pair-input" />
            <button @click.prevent="removePair(idx)" class="remove-pair-btn" title="Удалить пару">
              <svg width="16" height="16" viewBox="0 0 16 16"><line x1="3" y1="3" x2="13" y2="13" stroke="currentColor" stroke-width="2"/><line x1="13" y1="3" x2="3" y2="13" stroke="currentColor" stroke-width="2"/></svg>
            </button>
          </div>
          <button @click.prevent="addPair" class="add-pair-btn">
            <svg width="16" height="16" viewBox="0 0 16 16"><line x1="8" y1="3" x2="8" y2="13" stroke="currentColor" stroke-width="2"/><line x1="3" y1="8" x2="13" y2="8" stroke="currentColor" stroke-width="2"/></svg>
            Добавить пару
          </button>
        </div>
        
        <!-- Кнопки управления -->
        <div class="action-buttons">
          <button @click="addQuestion" class="action-btn add-question-btn">
            Добавить вопрос
          </button>
          <button @click="saveTest" :disabled="!canSaveAdd" class="action-btn save-test-btn">
            {{ editingTestId ? 'Сохранить изменения' : 'Сохранить тест' }}
          </button>
          <button v-if="editingTestId" @click="cancelEdit" class="action-btn cancel-btn">
            Отмена
          </button>
        </div>
      </div>
      
      <!-- Список добавленных вопросов -->
      <div v-if="add.questions.length" class="added-questions">
        <h3>Добавленные вопросы:</h3>
        <ul>
          <li v-for="(q, idx) in add.questions" :key="idx" class="question-item">
            <span class="question-text">{{ idx + 1 }}. {{ q.text }}</span>
            <button @click="removeQuestion(idx)" class="remove-question-btn" title="Удалить вопрос">
              <svg width="16" height="16" viewBox="0 0 16 16"><line x1="3" y1="3" x2="13" y2="13" stroke="currentColor" stroke-width="2"/><line x1="13" y1="3" x2="3" y2="13" stroke="currentColor" stroke-width="2"/></svg>
            </button>
          </li>
        </ul>
      </div>
      
      <div v-if="add.result" class="result-message">{{ add.result }}</div>
    </section>

    <!-- Список тестов для выбранного материала -->
    <section v-if="add.materialId && tests.length" class="test-mgmt-section">
      <h2>Тесты для выбранного материала</h2>
      <ul class="tests-list">
        <li v-for="test in tests" :key="test.id" class="test-item">
          <span>{{ test.title }}</span>
          <button @click="editTest(test)" class="edit-btn">Редактировать</button>
          <button @click="deleteTest(test.id)" class="delete-btn">Удалить</button>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'

const API_URL = import.meta.env.VITE_API_URL; // добавьте эту строку

// --- Общие данные ---
const subjects = ref([])
const tests = ref([])
const editingTestId = ref(null)

// --- Добавить/Редактировать тест ---
const add = ref({
  subjectId: '',
  themeId: '',
  materialId: '',
  themes: [],
  materials: [],
  title: '',
  questions: [],
  currentQuestion: {
    text: '',
    type: 'single',
    options: [{ text: '', correct: false }],
    pairs: [{ left: '', right: '' }],
    correct: null
  },
  result: ''
})

function addOption() { add.value.currentQuestion.options.push({ text: '', correct: false }) }
function removeOption(idx) { add.value.currentQuestion.options.splice(idx, 1) }
function addPair() { add.value.currentQuestion.pairs.push({ left: '', right: '' }) }
function removePair(idx) { add.value.currentQuestion.pairs.splice(idx, 1) }

function addQuestion() {
  add.value.questions.push(JSON.parse(JSON.stringify(add.value.currentQuestion)))
  add.value.currentQuestion = {
    text: '',
    type: 'single',
    options: [{ text: '', correct: false }],
    pairs: [{ left: '', right: '' }],
    correct: null
  }
}

function removeQuestion(idx) { add.value.questions.splice(idx, 1) }

const canSaveAdd = computed(() =>
  add.value.materialId && add.value.title.trim() && add.value.questions.length
)

async function saveTest() {
  add.value.result = ''
  const token = localStorage.getItem('token')
  const url = editingTestId.value
    ? `${API_URL}/tests/full/${editingTestId.value}`
    : `${API_URL}/tests/full`
  const method = editingTestId.value ? 'PUT' : 'POST'
  const res = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({
      material_id: add.value.materialId,
      title: add.value.title,
      questions: add.value.questions
    })
  })
  if (res.ok) {
    add.value.result = editingTestId.value
      ? 'Тест успешно обновлён'
      : 'Тест успешно добавлен'
    add.value.title = ''
    add.value.questions = []
    editingTestId.value = null
    // Обновить список тестов
    if (add.value.materialId) {
      await fetchTestsForMaterial(add.value.materialId)
    }
  } else {
    add.value.result = 'Ошибка при сохранении теста'
  }
}

async function fetchAddThemes() {
  add.value.themeId = ''
  add.value.materialId = ''
  add.value.themes = []
  add.value.materials = []
  if (!add.value.subjectId) return
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/themes/by_subject/${add.value.subjectId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) add.value.themes = await res.json()
}

async function fetchAddMaterials() {
  add.value.materialId = ''
  add.value.materials = []
  if (!add.value.themeId) return
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/materials/by_theme/${add.value.themeId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  if (res.ok) add.value.materials = await res.json()
}

// --- Получение тестов для выбранного материала ---
async function fetchTestsForMaterial(materialId) {
  tests.value = []
  if (!materialId) return
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/tests/by_material/${materialId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) tests.value = await res.json()
}

watch(() => add.value.materialId, (val) => {
  if (val) fetchTestsForMaterial(val)
  else tests.value = []
})

// --- Редактирование теста ---
async function editTest(test) {
  editingTestId.value = test.id
  add.value.result = ''
  // Получить сам тест
  add.value.title = test.title
  // Получить вопросы теста
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/tests/questions/${test.id}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const questions = await res.json()
    // Для каждого вопроса получить варианты/пары
    const detailedQuestions = []
    for (const q of questions) {
      let options = []
      let pairs = []
      let correct = null
      if (q.question_type === 'single' || q.question_type === 'multiple') {
        // Получить варианты
        const optRes = await fetch(`${API_URL}/test_options/${q.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (optRes.ok) {
          options = await optRes.json()
          if (q.question_type === 'single') {
            correct = options.findIndex(o => o.is_correct)
          }
        }
      }
      if (q.question_type === 'match') {
        // Получить пары
        const pairRes = await fetch(`${API_URL}/test_pairs/${q.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (pairRes.ok) pairs = await pairRes.json()
      }
      detailedQuestions.push({
        text: q.question_text,
        type: q.question_type,
        options: options.map(o => ({ text: o.option_text, correct: !!o.is_correct })),
        pairs: pairs.map(p => ({ left: p.left_text, right: p.right_text })),
        correct
      })
    }
    add.value.questions = detailedQuestions
  }
}

function cancelEdit() {
  editingTestId.value = null
  add.value.title = ''
  add.value.questions = []
  add.value.result = ''
}

// --- Удаление теста ---
async function deleteTest(testId) {
  if (!confirm('Удалить тест?')) return
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/tests/${testId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    tests.value = tests.value.filter(t => t.id !== testId)
    if (editingTestId.value === testId) {
      cancelEdit()
    }
  }
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  const res = await fetch(`${API_URL}/subjects/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) subjects.value = await res.json()
})
</script>

<style scoped>
.test-management, 
.test-management * {
  font-family: 'Montserrat', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.test-management {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.test-mgmt-section {
  background: #22223b;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.12);
  padding: 2rem;
  margin-bottom: 2rem;  
}

.test-mgmt-section h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #f2e9e4;
  font-size: 1.5rem;
  font-weight: 600;
}

.selection-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.select-group {
  flex: 1;
  min-width: 200px;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #c9ada7;
  font-size: 0.9rem;
}

.form-select, .form-input, .form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #9a8c98;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background-color: #22223b;
  color: #f2e9e4;
}

.form-select:focus, .form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #4a4e69;
  box-shadow: 0 0 0 2px #4a4e6933;
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.question-form {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #9a8c98;
}

.options-container, .pairs-container {
  margin: 1.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.option-item, .pair-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  width: 100%;
}

.option-input, .pair-input {
  flex: 1;
  background: #22223b;
  color: #f2e9e4;
  border: 1px solid #c9ada7;
}

.option-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.option-checkbox {
  width: 22px;
  height: 22px;
  accent-color: #4a4e69;
  cursor: pointer;
  margin: 0 2px;
}

.remove-option-btn, .remove-pair-btn, .remove-question-btn {
  background: none;
  border: none;
  color: #bb0a21;
  cursor: pointer;
  padding: 0.18rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.18s;
  outline: none;
}
.remove-option-btn:focus, .remove-pair-btn:focus, .remove-question-btn:focus {
  outline: none;
  background: none;
}
.remove-option-btn:hover, .remove-pair-btn:hover, .remove-question-btn:hover {
  background: #4a4e6922;
}
.remove-option-btn svg,
.remove-pair-btn svg,
.remove-question-btn svg {
  width: 18px;
  height: 18px;
  stroke: #bb0a21;
  color: #bb0a21;
  display: block;
  margin: auto;
  pointer-events: none;
}

.pair-arrow {
  color: #c9ada7;
  font-weight: bold;
}

.add-option-btn, .add-pair-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #4a4e69;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: #f2e9e4;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
  align-self: center;
}
.add-option-btn:hover, .add-pair-btn:hover {
  background: #22223b;
  color: #f2e9e4;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: center;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  font-family: inherit;
}

.add-question-btn {
  background: #4a4e69;
  color: #f2e9e4;
}
.add-question-btn:hover {
  background: #22223b;
  color: #f2e9e4;
}

.save-test-btn {
  background: #bb0a21;
  color: #fff;
}
.save-test-btn:hover:not(:disabled) {
  background: #9a0a1a;
}
.save-test-btn:disabled {
  background: #9a8c98;
  color: #f2e9e4;
  cursor: not-allowed;
}

.cancel-btn {
  background: #9a8c98;
  color: #22223b;
}
.cancel-btn:hover {
  background: #4a4e69;
  color: #fff;
}

.added-questions {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #9a8c98;
}

.added-questions h3 {
  font-size: 1.1rem;
  color: #c9ada7;
  margin-bottom: 1rem;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border-radius: 8px;
  background: #4a4e69;
  margin-bottom: 0.5rem;
}

.question-text {
  flex: 1;
  color: #f2e9e4;
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

.tests-list {
  margin-top: 1.5rem;
  padding: 0;
  list-style: none;
}

.test-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #4a4e69;
  color: #f2e9e4;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  margin-bottom: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.4rem 1rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.18s;
}
.edit-btn {
  background: #4a4e69;
  color: #fff;
}
.edit-btn:hover {
  background: #22223b;
}
.delete-btn {
  background: #bb0a21;
  color: #fff;
}
.delete-btn:hover {
  background: #9a0a1a;
}

@media (max-width: 768px) {
  .selection-row {
    flex-direction: column;
    gap: 1rem;
  }
  .select-group {
    width: 100%;
  }
  .action-buttons {
    flex-direction: column;
    gap: 0.75rem;
  }
  .action-btn {
    width: 100%;
  }
}
</style>