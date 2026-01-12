import { useState } from 'react'
import { authAPI } from '../services/api'
import './LoginPage.css'

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await authAPI.login(email)
      
      const userInfo = {
        name: response.user_name,
        email: response.user_email,
      }
      
      onLogin(response.access_token, userInfo)
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
                  <span>Вход...</span>
                </>
              ) : (
                'Войти'
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


