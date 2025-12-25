import { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import DataTable from '../components/DataTable'
import './DashboardPage.css'

function DashboardPage({ token, userInfo, onLogout }) {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await dashboardAPI.getDashboard()
      setDashboardData(data)
    } catch (err) {
      console.error('Dashboard load error:', err)
      setError('Ошибка при загрузке данных дашборда')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard-page">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1 className="header-title">📊 Dashboard</h1>
          </div>
          <div className="header-user">
            <span className="user-name">
              <strong>{userInfo?.name || 'Пользователь'}</strong>
            </span>
            <button onClick={onLogout} className="btn btn-secondary">
              Выйти
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="container">
          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Загрузка данных...</p>
            </div>
          )}

          {error && (
            <div className="error-banner">
              {error}
              <button onClick={loadDashboard} className="btn btn-primary">
                Повторить
              </button>
            </div>
          )}

          {!loading && !error && dashboardData && (
            <>
              <div className="dashboard-welcome">
                <h2>Привет, {dashboardData.user_name}! 👋</h2>
                <p>Ваш персонализированный дашборд с аналитикой</p>
              </div>

              <div className="dashboard-grid">
                {dashboardData.items && dashboardData.items.length > 0 ? (
                  dashboardData.items.map((item) => (
                    <div key={item.id} className="dashboard-item">
                      <h2>{item.title}</h2>
                      {item.description && <p>{item.description}</p>}
                      
                      {item.data && item.data.length > 0 ? (
                        <DataTable data={item.data} columns={item.columns} />
                      ) : (
                        <div className="no-data">
                          <p>📭 Нет данных для отображения</p>
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="no-dashboards">
                    <div className="no-dashboards-content">
                      <h3>📊 Дашборды пока не настроены</h3>
                      <p>
                        SQL-запросы для дашбордов еще не добавлены.
                        <br />
                        Добавьте запросы в <code>backend/app/services/dashboard_service.py</code>
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  )
}

export default DashboardPage


