import { useState } from 'react'
import './WaitingSalesTable.css'

function WaitingSalesTable({ data, details }) {
  // По умолчанию все категории развернуты
  const [expandedCategories, setExpandedCategories] = useState(() => {
    const categories = new Set()
    if (details && details.length > 0) {
      details.forEach(task => {
        if (task.category) {
          categories.add(task.category)
        }
      })
    }
    return categories
  })

  if (!data || data.length === 0) {
    return (
      <div className="no-data">
        <p>Нет данных для отображения</p>
      </div>
    )
  }

  const toggleCategory = (category) => {
    setExpandedCategories(prev => {
      const newSet = new Set(prev)
      if (newSet.has(category)) {
        newSet.delete(category)
      } else {
        newSet.add(category)
      }
      return newSet
    })
  }

  // Группируем детали по категориям
  const groupedDetails = {}
  if (details && details.length > 0) {
    details.forEach(task => {
      const category = task.category
      if (!groupedDetails[category]) {
        groupedDetails[category] = []
      }
      groupedDetails[category].push(task)
    })
  }

  // Функция для определения класса статуса
  const getStatusClass = (status) => {
    if (!status || status === 'Без статуса') return 'status-default'
    if (status === 'Завершенная' || status === 'Доставлено клиенту') return 'status-completed'
    if (status === 'Нужно прикрепить документы') return 'status-waiting'
    return 'status-active'
  }

  return (
    <div className="waiting-sales-wrapper">
      <table className="data-table waiting-sales-table">
        <thead>
          <tr>
            <th>Категория</th>
            <th>Кол-во</th>
            <th>Ср. дней</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => {
            const category = row['Категория']
            const hasDetails = groupedDetails[category] && groupedDetails[category].length > 0
            const isExpanded = expandedCategories.has(category)

            return (
              <>
                <tr 
                  key={rowIndex}
                  className={hasDetails ? 'clickable-row' : ''}
                  onClick={() => hasDetails && toggleCategory(category)}
                  style={{ cursor: hasDetails ? 'pointer' : 'default' }}
                >
                  <td>
                    {hasDetails && (
                      <span className="expand-icon">
                        {isExpanded ? '▼' : '▶'}
                      </span>
                    )}
                    {' '}
                    {category}
                  </td>
                  <td>{row['Кол-во']}</td>
                  <td>{row['Ср. дней']}</td>
                </tr>
                
                {/* Раскрывающийся список задач */}
                {isExpanded && hasDetails && (
                  <tr className="details-row">
                    <td colSpan="3">
                      <div className="task-details">
                        <h4>Задачи, ожидающие документов ({category}):</h4>
                        <ul className="task-list">
                          {groupedDetails[category].map((task, idx) => (
                            <li key={idx} className="task-item">
                              <a 
                                href={`https://megamindru.planfix.ru/task/${task.task_id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="task-link"
                              >
                                {task.task_name || `Задача #${task.task_id}`}
                              </a>
                              {task.status && (
                                <span className={`task-status ${getStatusClass(task.status)}`}>
                                  {task.status}
                                </span>
                              )}
                              <span className="waiting-days">
                                Ожидание: <strong>{task.waiting_days || 0}</strong> {task.waiting_days === 1 ? 'день' : task.waiting_days < 5 ? 'дня' : 'дней'}
                              </span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </td>
                  </tr>
                )}
              </>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default WaitingSalesTable

