import React, { useState } from 'react';
import './ClientOrdersTable.css';

const ClientOrdersTable = ({ data, details, columns }) => {
  const [expanded, setExpanded] = useState({});

  // Debug logging
  console.log('📦 ClientOrdersTable received:');
  console.log('   data:', data);
  console.log('   details:', details);
  console.log('   columns:', columns);

  const toggleExpand = (client) => {
    setExpanded(prev => ({
      ...prev,
      [client]: !prev[client]
    }));
  };

  // Группируем заказы по клиентам
  const ordersByClient = (details || []).reduce((acc, order) => {
    if (!acc[order.client]) {
      acc[order.client] = [];
    }
    acc[order.client].push(order);
    return acc;
  }, {});

  console.log('   ordersByClient:', ordersByClient);

  return (
    <div className="client-orders-container">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col, idx) => (
              <th key={idx}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => {
            const client = row['Клиент'];
            const isTotal = client === 'ИТОГО';
            const hasOrders = ordersByClient[client] && ordersByClient[client].length > 0;

            return (
              <React.Fragment key={rowIndex}>
                <tr className={isTotal ? 'total-row' : ''}>
                  {columns.map((col, colIndex) => (
                    <td key={colIndex}>
                      {colIndex === 0 ? (
                        // Первая колонка: добавляем стрелочку перед названием клиента
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          {!isTotal && hasOrders && (
                            <button
                              className="expand-btn"
                              onClick={() => toggleExpand(client)}
                              title={expanded[client] ? 'Скрыть заказы' : 'Показать заказы'}
                            >
                              {expanded[client] ? '▲' : '▼'}
                            </button>
                          )}
                          <span>{row[col]}</span>
                        </div>
                      ) : (
                        // Остальные колонки: просто значение
                        row[col]
                      )}
                    </td>
                  ))}
                </tr>
                {!isTotal && expanded[client] && hasOrders && (
                  <tr className="details-row">
                    <td colSpan={columns.length}>
                      <div className="details-content">
                        <h4>Заказы от клиента: {client}</h4>
                        <ul className="orders-list">
                          {ordersByClient[client].map((order, idx) => (
                            <li key={idx}>
                              <a
                                href={`https://megamindru.planfix.ru/task/${order.task_id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="order-link"
                              >
                                {order.order_name}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default ClientOrdersTable;

