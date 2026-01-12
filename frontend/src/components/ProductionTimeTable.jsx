import React, { useState, useEffect } from 'react';
import './ProductionTimeTable.css';

const ProductionTimeTable = ({ data, columns }) => {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Определяем индекс столбца "Изменение"
  const changeColumnIndex = columns.findIndex(col => col === 'Изменение');

  const getCellClassName = (colIndex, value) => {
    // Если это столбец "Изменение" и значение существует
    if (colIndex === changeColumnIndex && value !== null && value !== undefined && value !== '') {
      const numValue = parseFloat(value);
      if (!isNaN(numValue)) {
        if (numValue < 0) {
          return 'change-negative'; // Отрицательное изменение = красный
        } else if (numValue > 0) {
          return 'change-positive'; // Положительное изменение = зелёный
        }
      }
    }
    return '';
  };

  const formatCellValue = (colIndex, value) => {
    // Если это столбец "Изменение" и значение существует
    if (colIndex === changeColumnIndex && value !== null && value !== undefined && value !== '') {
      const numValue = parseFloat(value);
      if (!isNaN(numValue)) {
        const prefix = numValue > 0 ? '+' : '';
        return `${prefix}${value}`;
      }
    }
    return value ?? '-';
  };

  return (
    <div className={`production-time-table ${isMobile ? 'mobile' : ''}`}>
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
                  className={getCellClassName(colIndex, row[col])}
                  data-label={col}
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

export default ProductionTimeTable;

