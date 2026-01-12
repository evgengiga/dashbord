import axios from 'axios'

// Используем переменную окружения или определяем автоматически
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api' 
    : `${window.location.origin}/api`)

// Создаем экземпляр axios с базовыми настройками
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Добавляем токен к каждому запросу
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Обработка ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Токен истек или невалидный
      localStorage.removeItem('authToken')
      localStorage.removeItem('userInfo')
      window.location.reload()
    }
    return Promise.reject(error)
  }
)

/**
 * API для аутентификации
 */
export const authAPI = {
  login: async (email) => {
    const response = await api.post('/auth/login', { email })
    return response.data
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

/**
 * API для дашборда
 */
export const dashboardAPI = {
  getDashboard: async (fiscalYear = 'current', orderStatus = 'active') => {
    const response = await api.get('/dashboard/', {
      params: { 
        fiscal_year: fiscalYear,
        order_status: orderStatus
      }
    })
    return response.data
  },
  
  getDashboardItems: async (fiscalYear = 'current') => {
    const response = await api.get('/dashboard/items', {
      params: { fiscal_year: fiscalYear }
    })
    return response.data
  },
}

/**
 * Проверка здоровья сервиса
 */
export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api

