import { useState, useEffect } from 'react'
import './App.css'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'

function App() {
  const [token, setToken] = useState(null)
  const [userInfo, setUserInfo] = useState(null)
  const [theme, setTheme] = useState(() => {
    // Загружаем тему из localStorage или используем светлую по умолчанию
    return localStorage.getItem('theme') || 'light'
  })

  // Применяем тему к document.documentElement
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  // Проверяем наличие токена при загрузке
  useEffect(() => {
    const savedToken = localStorage.getItem('authToken')
    const savedUser = localStorage.getItem('userInfo')
    
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUserInfo(JSON.parse(savedUser))
    }
  }, [])

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light')
  }

  const handleLogin = (authToken, user) => {
    setToken(authToken)
    setUserInfo(user)
    localStorage.setItem('authToken', authToken)
    localStorage.setItem('userInfo', JSON.stringify(user))
  }

  const handleLogout = () => {
    setToken(null)
    setUserInfo(null)
    localStorage.removeItem('authToken')
    localStorage.removeItem('userInfo')
  }

  return (
    <div className="app">
      {!token ? (
        <LoginPage onLogin={handleLogin} />
      ) : (
        <DashboardPage 
          token={token} 
          userInfo={userInfo} 
          onLogout={handleLogout}
          theme={theme}
          onToggleTheme={toggleTheme}
        />
      )}
    </div>
  )
}

export default App


