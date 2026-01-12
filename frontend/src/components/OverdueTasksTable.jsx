import { useState } from 'react'
import './OverdueTasksTable.css'

function OverdueTasksTable({ data, details }) {
  const [expandedCategory, setExpandedCategory] = useState(null)

  if (!data || data.length === 0) {
    return (
      <div className="no-data">
        <p>Нет данных для отображения</p>
      </div>
    )
  }

  const toggleCategory = (category) => {
    setExpandedCategory(expandedCategory === category ? null : category)
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

  return (
    <div className="overdue-tasks-wrapper">
      <table className="data-table overdue-tasks-table">
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
            const isExpanded = expandedCategory === category

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
                        <h4>Просроченные задачи ({category}):</h4>
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
                              <span className="overdue-days">
                                Просрочка: <strong>{task.prosr_day}</strong> {task.prosr_day === 1 ? 'день' : task.prosr_day < 5 ? 'дня' : 'дней'}
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

export default OverdueTasksTable



