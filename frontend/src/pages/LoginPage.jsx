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
  const [showPassword, setShowPassword] = useState(false)
  const [showPasswordConfirm, setShowPasswordConfirm] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    e.stopPropagation() // Предотвращаем всплытие события
    
    // Предотвращаем отправку формы браузером
    if (e.target && e.target.tagName === 'FORM') {
      e.target.setAttribute('novalidate', 'novalidate')
    }
    
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

          <form onSubmit={handleSubmit} className="login-form" noValidate>
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
              <div className="password-input-wrapper">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  className="input"
                  placeholder={showRegister ? 'От 6 до 72 символов' : 'Введите пароль'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={loading}
                  minLength={6}
                  maxLength={72}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  tabIndex={-1}
                  aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
                >
                  {showPassword ? (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                      <line x1="1" y1="1" x2="23" y2="23"></line>
                    </svg>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {showRegister && (
              <div className="form-group">
                <label htmlFor="passwordConfirm">Повторите пароль</label>
                <div className="password-input-wrapper">
                  <input
                    id="passwordConfirm"
                    type={showPasswordConfirm ? "text" : "password"}
                    className="input"
                    placeholder="Повторите пароль"
                    value={passwordConfirm}
                    onChange={(e) => setPasswordConfirm(e.target.value)}
                    required
                    disabled={loading}
                    minLength={6}
                    maxLength={72}
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPasswordConfirm(!showPasswordConfirm)}
                    tabIndex={-1}
                    aria-label={showPasswordConfirm ? "Скрыть пароль" : "Показать пароль"}
                  >
                    {showPasswordConfirm ? (
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                        <line x1="1" y1="1" x2="23" y2="23"></line>
                      </svg>
                    ) : (
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    )}
                  </button>
                </div>
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


