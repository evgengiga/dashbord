import React, { useState, useEffect } from 'react';
import './ResponsiveTable.css';

const ResponsiveTable = ({ data, columns, className = '' }) => {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (!data || data.length === 0) {
    return (
      <div className="no-data">
        <p>📭 Нет данных для отображения</p>
      </div>
    );
  }

  // Определяем индекс столбца "Изменение" (case-insensitive, с trim)
  const changeColumnIndex = columns.findIndex(col => {
    const normalized = String(col).trim().toLowerCase();
    return normalized === 'изменение';
  });

  // Отладочный вывод (можно убрать после проверки)
  if (changeColumnIndex !== -1) {
    console.log('✅ ResponsiveTable: Найдена колонка "Изменение" на индексе', changeColumnIndex);
    console.log('✅ ResponsiveTable: Все колонки:', columns);
  } else {
    console.warn('⚠️ ResponsiveTable: Колонка "Изменение" не найдена. Доступные колонки:', columns);
  }

  // Функция для определения класса CSS ячейки
  const getCellClassName = (colIndex, value) => {
    // Если это столбец "Изменение" и значение существует
    if (colIndex === changeColumnIndex && value !== null && value !== undefined && value !== '') {
      const numValue = parseFloat(value);
      if (!isNaN(numValue)) {
        if (numValue < 0) {
          return 'change-positive'; // Отрицательное изменение = зелёный (хорошо)
        } else if (numValue > 0) {
          return 'change-negative'; // Положительное изменение = красный (плохо)
        }
      }
    }
    return '';
  };

  // Функция для форматирования значений
  const formatCellValue = (colIndex, value) => {
    if (value === null || value === undefined || value === '') {
      return '-';
    }
    
    // Если это столбец "Изменение", добавляем знак + для положительных значений
    if (colIndex === changeColumnIndex) {
      const numValue = parseFloat(value);
      if (!isNaN(numValue)) {
        const prefix = numValue > 0 ? '+' : '';
        return `${prefix}${value}`;
      }
    }
    
    return value;
  };

  return (
    <div className={`responsive-table-wrapper ${isMobile ? 'mobile' : ''} ${className}`}>
      <table className="responsive-table">
        <thead>
          <tr>
            {columns.map((col, idx) => (
              <th key={idx}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((col, colIndex) => (
                <td 
                  key={colIndex} 
                  data-label={col}
                  className={getCellClassName(colIndex, row[col])}
                >
                  {formatCellValue(colIndex, row[col])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResponsiveTable;


