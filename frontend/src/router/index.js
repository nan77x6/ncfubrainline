import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SubjectsView from '../views/SubjectsView.vue'
import TestsView from '../views/TestsView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import TestManagement from '../components/TestManagement.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  { path: '/', name: 'home', component: HomeView },
  { path: '/subjects', name: 'subjects', component: SubjectsView },
  { path: '/tests', name: 'tests', component: TestsView },
  { path: '/profile/admin', name: 'admin-profile', component: ProfileView },
  { path: '/profile/teacher', name: 'teacher-profile', component: ProfileView },
  { path: '/profile/student', name: 'student-profile', component: ProfileView },
  {
    path: '/subjects/:subjectId/themes',
    name: 'SubjectThemes',
    component: () => import('@/views/SubjectThemesView.vue')
  },
  { 
    path: '/themes/:themeId/materials', 
    component: () => import('@/views/ThemeMaterialsView.vue') 
  },
  {
    path: '/materials/:materialId',
    name: 'MaterialView',
    component: () => import('@/views/MaterialView.vue')
  },
  {
    path: '/test-management',
    name: 'TestManagement',
    component: TestManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/tests/subject/:subjectId',
    name: 'TestThemesView',
    component: () => import('@/views/TestThemesView.vue')
  },
  {
    path: '/tests/pass/:testId',
    name: 'TestPassView',
    component: () => import('@/views/TestPassView.vue')
  },
  {
    path: '/tests/materials/:themeId',
    name: 'TestMaterialsView',
    component: () => import('@/views/TestMaterialsView.vue')
  },
  {
    path: '/media',
    name: 'MediaView',
    component: () => import('@/views/MediaView.vue')
  },
  {
    path: '/media/subject/:subjectId',
    name: 'MediaThemesView',
    component: () => import('@/views/MediaThemesView.vue')
  },
  {
    path: '/media/materials/:themeId',
    name: 'MediaMaterialsView',
    component: () => import('@/views/MediaMaterialsView.vue')
  },
  {
    path: '/media/material/:materialId',
    name: 'MediaDisplayView',
    component: () => import('@/views/MediaDisplayView.vue')
  },
  
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Глобальный guard для авторизации
router.beforeEach((to, from, next) => {
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)
  const token = localStorage.getItem('token')
  if (authRequired && !token) {
    return next('/login')
  }
  if (to.path === '/login' && token) {
    // Если уже авторизован, не пускать на /login, а сразу на главную
    return next('/')
  }
  next()
})

export default router
