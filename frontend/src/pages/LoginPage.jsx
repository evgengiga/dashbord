import { useState } from 'react'
import { authAPI } from '../services/api'
import './LoginPage.css'

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showRegister, setShowRegister] = useState(false)
  const [passwordConfirm, setPasswordConfirm] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (showRegister) {
        // Регистрация (первый вход)
        const response = await authAPI.register(email, password, passwordConfirm)
        
        const userInfo = {
          name: response.user_name,
          email: response.user_email,
        }
        
        onLogin(response.access_token, userInfo)
      } else {
        // Обычный вход
        const response = await authAPI.login(email, password)
        
        if (response.first_login) {
          // Первый вход - показываем форму регистрации
          setShowRegister(true)
          setError('')
        } else {
          // Успешный вход
          const userInfo = {
            name: response.user_name,
            email: response.user_email,
          }
          
          onLogin(response.access_token, userInfo)
        }
      }
    } catch (err) {
      console.error('Login error:', err)
      
      if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else if (err.response?.status === 404) {
        setError('Пользователь не найден в Planfix')
      } else {
        setError('Ошибка при входе. Проверьте подключение к серверу.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <h1>Дашборд HeadCorn</h1>
            <p>Персонализированный дашборд с аналитикой</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                className="input"
                placeholder="example@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">
                {showRegister ? 'Придумайте пароль' : 'Пароль'}
              </label>
              <input
                id="password"
                type="password"
                className="input"
                placeholder={showRegister ? 'Минимум 6 символов' : 'Введите пароль'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
                minLength={6}
              />
            </div>

            {showRegister && (
              <div className="form-group">
                <label htmlFor="passwordConfirm">Повторите пароль</label>
                <input
                  id="passwordConfirm"
                  type="password"
                  className="input"
                  placeholder="Повторите пароль"
                  value={passwordConfirm}
                  onChange={(e) => setPasswordConfirm(e.target.value)}
                  required
                  disabled={loading}
                  minLength={6}
                />
              </div>
            )}

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary btn-large"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner-small"></div>
                  <span>{showRegister ? 'Регистрация...' : 'Вход...'}</span>
                </>
              ) : (
                showRegister ? 'Зарегистрироваться' : 'Войти'
              )}
            </button>
          </form>

          <div className="login-footer">
            <p>Введите свой корпоративный email для входа</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LoginPage


