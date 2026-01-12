import './DataTable.css'

function DataTable({ data, columns }) {
  if (!data || data.length === 0) {
    return (
      <div className="no-data">
        <p>Нет данных для отображения</p>
      </div>
    )
  }

  // Если columns не указаны, берем ключи из первой строки
  const tableColumns = columns || Object.keys(data[0])

  // Функция для форматирования значений
  const formatValue = (value) => {
    if (value === null || value === undefined) {
      return '-'
    }
    
    // Если это число с плавающей точкой, округляем до 2 знаков
    if (typeof value === 'number' && !Number.isInteger(value)) {
      return value.toFixed(2)
    }
    
    // Если это процент (заканчивается на %)
    if (typeof value === 'string' && value.includes('%')) {
      return value
    }
    
    return value
  }

  // Функция для определения цвета ячейки (если это процент)
  const getCellStyle = (value) => {
    if (typeof value === 'string' && value.includes('%')) {
      const percent = parseFloat(value)
      if (percent >= 70) {
        return { backgroundColor: '#c8e6c9' } // Зеленый
      } else if (percent >= 40) {
        return { backgroundColor: '#fff9c4' } // Желтый
      } else if (percent < 40 && percent > 0) {
        return { backgroundColor: '#ffccbc' } // Оранжевый
      }
    }
    return {}
  }

  return (
    <div className="data-table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            {tableColumns.map((column, index) => (
              <th key={index}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {tableColumns.map((column, colIndex) => (
                <td 
                  key={colIndex}
                  style={getCellStyle(row[column])}
                >
                  {formatValue(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default DataTable




