import './WaitingSalesTable.css'

function WaitingSalesTable({ data, details }) {
  // Функция для определения класса статуса
  const getStatusClass = (status) => {
    if (!status || status === 'Без статуса') return 'status-default'
    if (status === 'Завершенная' || status === 'Доставлено клиенту') return 'status-completed'
    if (status === 'Нужно прикрепить документы') return 'status-waiting'
    return 'status-active'
  }

  if (!details || details.length === 0) {
    return (
      <div className="no-data">
        <p>Нет данных для отображения</p>
      </div>
    )
  }

  return (
    <div className="waiting-sales-wrapper">
      <div className="task-details">
        <ul className="task-list">
          {details.map((task, idx) => (
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
              <span className="overdue-days">
                Просрочка: <strong>{task.waiting_days || 0}</strong> {task.waiting_days === 1 ? 'день' : task.waiting_days < 5 ? 'дня' : 'дней'}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default WaitingSalesTable

