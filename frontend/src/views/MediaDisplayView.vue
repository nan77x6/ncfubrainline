<template>
  <main class="media-display-main">
    <button class="back-btn" @click="goBack">← Назад</button>
    <h1>{{ materialTitle }}</h1>
    <div v-if="loading" class="loading-block">
      <div class="loading-spinner"></div>
      <p>Загрузка медиа...</p>
    </div>
    <div v-else class="media-content">
      <!-- Галерея изображений -->
      <div v-if="images.length" class="media-section">
        <h2>Изображения</h2>
        <div class="media-gallery">
          <div 
            v-for="(img, index) in images" 
            :key="img.id" 
            class="media-img-card"
            @click="openModal(index)"
          >
            <img :src="img.url" :alt="'Изображение ' + (index + 1)" class="media-img" />
            <div class="img-overlay">Нажмите для просмотра</div>
          </div>
        </div>
      </div>
      <!-- Галерея видео -->
      <div v-if="videos.length" class="media-section">
        <h2>Видео</h2>
        <div class="media-gallery">
          <div v-for="(vid, idx) in videos" :key="vid.id" class="media-video-card">
            <video
              :src="vid.url"
              controls
              class="media-video"
              preload="metadata"
            ></video>
            <div class="video-title">Видео {{ idx + 1 }}</div>
          </div>
        </div>
      </div>
      
      <!-- Список других файлов -->
      <div v-if="others.length" class="media-section">
        <h2>Другие файлы</h2>
        <div class="media-other-list">
          <div v-for="other in others" :key="other.id" class="other-file">
            <div class="file-icon">
              <span v-if="other.type === 'pdf'">📄</span>
              <span v-else-if="other.type === 'doc' || other.type === 'docx'">📝</span>
              <span v-else-if="other.type === 'zip' || other.type === 'rar'">🗜️</span>
              <span v-else>📁</span>
            </div>
            <a 
              :href="other.url" 
              target="_blank" 
              class="file-link"
              :download="other.url.split('/').pop()"
            >
              {{ other.url.split('/').pop() }}
              <span class="file-size">({{ formatFileSize(other.size) }})</span>
            </a>
          </div>
        </div>
      </div>
      
      <div v-if="!images.length && !videos.length && !others.length" class="empty-state">
        <div class="empty-icon">📷</div>
        <p>Нет медиафайлов для этого материала.</p>
      </div>
    </div>

    <!-- Модальное окно для просмотра изображений -->
    <div v-if="showModal" class="image-modal" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">×</button>
        <img :src="currentImage.url" class="modal-image" :alt="'Изображение ' + (currentImageIndex + 1)" />
        <div class="modal-nav">
          <button @click="prevImage" :disabled="currentImageIndex === 0">←</button>
          <span>{{ currentImageIndex + 1 }} / {{ images.length }}</span>
          <button @click="nextImage" :disabled="currentImageIndex === images.length - 1">→</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const materialId = route.params.materialId

const loading = ref(true)
const materialTitle = ref('Медиа')
const images = ref([])
const videos = ref([])
const others = ref([])

const API_URL = import.meta.env.VITE_API_URL; // добавьте эту строку

// Для модального окна изображений
const showModal = ref(false)
const currentImageIndex = ref(0)
const currentImage = ref(null)

async function fetchMedia() {
  loading.value = true
  const token = localStorage.getItem('token')
  
  // Получаем название материала
  const matRes = await fetch(`${API_URL}/materials/${materialId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (matRes.ok) {
    const mat = await matRes.json()
    materialTitle.value = mat.title
  }
  
  // Получаем медиа
  const res = await fetch(`${API_URL}/media/by_material/${materialId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    const media = await res.json()
    images.value = media.filter(m => m.type === 'image')
    videos.value = media.filter(m => m.type === 'video')
    others.value = media.filter(m => m.type !== 'image' && m.type !== 'video')
  }
  loading.value = false
}

function goBack() {
  router.back()
}

// Функции для модального окна изображений
function openModal(index) {
  currentImageIndex.value = index
  currentImage.value = images.value[index]
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  showModal.value = false
  document.body.style.overflow = 'auto'
}

function prevImage() {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
    currentImage.value = images.value[currentImageIndex.value]
  }
}

function nextImage() {
  if (currentImageIndex.value < images.value.length - 1) {
    currentImageIndex.value++
    currentImage.value = images.value[currentImageIndex.value]
  }
}

// Форматирование размера файла
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

onMounted(fetchMedia)
</script>

<style scoped>
.media-display-main {
  min-height: 80vh;
  padding: 2rem 5vw;
  background: #f2e9e4;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.back-btn {
  align-self: flex-start;
  margin-bottom: 1.5rem;
  padding: 0.5rem 1rem;
  background: #4a4e69;
  border: none;
  border-radius: 6px;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #22223b;
}

h1 {
  font-size: 2rem;
  color: #22223b;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 700;
  padding-bottom: 1rem;
  border-bottom: 2px solid #4a4e69;
  width: 100%;
  max-width: 1100px;
}

.loading-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
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

.media-content {
  width: 100%;
  max-width: 1200px;
}

.media-section {
  margin-bottom: 3rem;
  background: #22223b;
  border-radius: 16px;
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.18);
}

.media-section h2 {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #c9ada7;
}

.media-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.media-img-card {
  position: relative;
  background: #22223b;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(34, 34, 59, 0.18);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  aspect-ratio: 16/9;
}

.media-img-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(34, 34, 59, 0.22);
}

.media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.img-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(34, 34, 59, 0.7);
  color: #fff;
  padding: 0.8rem;
  text-align: center;
  font-size: 0.9rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.media-img-card:hover .img-overlay {
  opacity: 1;
}

.media-video-card {
  background: #22223b;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(34, 34, 59, 0.18);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.media-video {
  width: 100%;
  height: auto;
  display: block;
  background: #181828;
  border-radius: 10px 10px 0 0;
}

.video-title {
  padding: 0.8rem;
  color: #fff;
  text-align: center;
  background: #4a4e69;
  font-size: 1rem;
  border-radius: 0 0 10px 10px;
  width: 100%;
}

.media-other-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.other-file {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #22223b;
  border-radius: 8px;
  transition: background 0.2s;
}

.other-file:hover {
  background: #4a4e69;
}

.file-icon {
  font-size: 1.5rem;
  color: #fff;
}

.file-link {
  flex: 1;
  color: #fff;
  text-decoration: none;
  word-break: break-all;
}

.file-link:hover {
  text-decoration: underline;
  color: #c9ada7;
}

.file-size {
  color: #c9ada7;
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: #22223b;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(34, 34, 59, 0.18);
  color: #fff;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #4a4e69;
}

/* Модальное окно для изображений */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(34, 34, 59, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  background: #22223b;
  border-radius: 10px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #bb0a21;
  color: #fff;
  border: none;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.close-btn:hover {
  background: #9a091b;
}

.modal-image {
  max-width: 80vw;
  max-height: 80vh;
  object-fit: contain;
  display: block;
  border-radius: 6px;
}

.modal-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 1.5rem;
  color: #fff;
}

.modal-nav button {
  background: #4a4e69;
  color: #fff;
  border: none;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.2s;
}

.modal-nav button:hover:not(:disabled) {
  background: #22223b;
}

.modal-nav button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .media-gallery {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
  
  .media-section {
    padding: 1rem;
  }
  
  h1 {
    font-size: 1.5rem;
  }
}
</style>