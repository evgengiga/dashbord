import { useState, useEffect } from 'react'
import { dashboardAPI } from '../services/api'
import ResponsiveTable from '../components/ResponsiveTable'
import OverdueTasksTable from '../components/OverdueTasksTable'
import ClientOrdersTable from '../components/ClientOrdersTable'
import ProductionTimeTable from '../components/ProductionTimeTable'
import ThemeToggle from '../components/ThemeToggle'
import './DashboardPage.css'

function DashboardPage({ token, userInfo, onLogout, theme, onToggleTheme }) {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [orderStatus, setOrderStatus] = useState('active') // 'active', 'completed', 'all'

  useEffect(() => {
    loadDashboard()
  }, [orderStatus]) // Перезагружаем при изменении статуса

  const loadDashboard = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await dashboardAPI.getDashboard('current', orderStatus)
      console.log('📊 Dashboard data received:', data)
      console.log('📊 Items:', data.items)
      // Логируем просроченные задачи отдельно
      const overdueItem = data.items?.find(item => item.id === 'overdue_tasks')
      if (overdueItem) {
        console.log('📋 Overdue tasks item:', overdueItem)
        console.log('📋 Overdue details:', overdueItem.details)
      }
      // Логируем заказы клиентов
      const clientOrdersItem = data.items?.find(item => item.id === 'client_orders')
      if (clientOrdersItem) {
        console.log('📦 Client orders item:', clientOrdersItem)
        console.log('📦 Client orders details:', clientOrdersItem.details)
      }
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
            <ThemeToggle theme={theme} onToggle={onToggleTheme} />
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
                      
                      {/* Проверяем есть ли данные */}
                      {(() => {
                        // Для просроченных задач data может быть объектом {summary, details}
                        const hasData = item.id === 'overdue_tasks' 
                          ? (item.data && item.data.length > 0)
                          : (item.data && item.data.length > 0);
                        
                        if (!hasData) {
                          return (
                            <div className="no-data">
                              <p>📭 Нет данных для отображения</p>
                            </div>
                          );
                        }
                        
                        // Специальный компонент для просроченных задач
                        if (item.id === 'overdue_tasks') {
                          return (
                            <OverdueTasksTable 
                              data={item.data} 
                              details={item.details || []} 
                            />
                          );
                        }
                        
                        // Специальный компонент для заказов от клиентов
                        if (item.id === 'client_orders') {
                          return (
                            <>
                              {/* Переключатель статуса заказов */}
                              <div className="status-filter-container">
                                <label htmlFor="order-status-filter">Фильтр по статусу:</label>
                                <select 
                                  id="order-status-filter"
                                  value={orderStatus} 
                                  onChange={(e) => setOrderStatus(e.target.value)}
                                  className="status-filter"
                                >
                                  <option value="active">Активные заказы</option>
                                  <option value="completed">Завершенные заказы</option>
                                  <option value="all">Все заказы</option>
                                </select>
                              </div>
                              
                              <ClientOrdersTable 
                                data={item.data} 
                                details={item.details || []} 
                                columns={item.columns}
                              />
                            </>
                          );
                        }
                        
                        // Специальный компонент для среднего времени принятия производства
                        if (item.id === 'production_acceptance_time') {
                          return (
                            <ProductionTimeTable 
                              data={item.data} 
                              columns={item.columns}
                            />
                          );
                        }
                        
                        // Универсальная адаптивная таблица для всех остальных
                        return <ResponsiveTable data={item.data} columns={item.columns} />;
                      })()}
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


