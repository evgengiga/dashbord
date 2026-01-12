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
                <td key={colIndex} data-label={col}>
                  {row[col]}
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

