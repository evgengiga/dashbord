import React from 'react';
import './CompactTable.css';

const CompactTable = ({ data, columns, isMobile }) => {
  // Сокращаем названия колонок для мобильных
  const getMobileColumnName = (col) => {
    const shortenMap = {
      'Кол-во КП': 'КП',
      'Кол-во образцов': 'Образцы',
      'Кол-во производств': 'Произв.',
      'Конверсия': 'Конв.,%',
      'Период': 'Период'
    };
    return isMobile && shortenMap[col] ? shortenMap[col] : col;
  };

  // Сокращаем значения периодов для мобильных
  const shortenPeriodValue = (value) => {
    if (!isMobile || typeof value !== 'string') return value;
    
    // "Текущий квартал (01.01.2026 - 31.03.2026)" → "Тек. кв. (01.01-31.03)"
    if (value.includes('Текущий квартал')) {
      const match = value.match(/\((\d{2}\.\d{2})\.(\d{4}) - (\d{2}\.\d{2})\.(\d{4})\)/);
      if (match) return `Тек. кв. (${match[1]}-${match[3]})`;
    }
    
    // "Прошлый квартал (01.07.2025 - 30.09.2025)" → "Прош. кв. (01.07-30.09)"
    if (value.includes('Прошлый квартал')) {
      const match = value.match(/\((\d{2}\.\d{2})\.(\d{4}) - (\d{2}\.\d{2})\.(\d{4})\)/);
      if (match) return `Прош. кв. (${match[1]}-${match[3]})`;
    }
    
    // "Финансовый год (01.03.2025 - 28.02.2026)" → "Фин. год (03.25-02.26)"
    if (value.includes('Финансовый год')) {
      const match = value.match(/\((\d{2})\.(\d{2})\.(\d{4}) - (\d{2})\.(\d{2})\.(\d{4})\)/);
      if (match) return `Фин. год (${match[2]}.${match[3].slice(-2)}-${match[5]}.${match[6].slice(-2)})`;
    }
    
    return value;
  };

  return (
    <div className={`compact-table-wrapper ${isMobile ? 'mobile' : ''}`}>
      <table className="compact-table">
        <thead>
          <tr>
            {columns.map((col, idx) => (
              <th key={idx}>{getMobileColumnName(col)}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((col, colIndex) => (
                <td key={colIndex} className={colIndex === 0 ? 'period-col' : ''}>
                  {colIndex === 0 ? shortenPeriodValue(row[col]) : row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CompactTable;

