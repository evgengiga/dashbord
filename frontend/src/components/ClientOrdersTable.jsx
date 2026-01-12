import React, { useState } from 'react';
import './ClientOrdersTable.css';

const ClientOrdersTable = ({ data, details, columns }) => {
  const [expanded, setExpanded] = useState({});

  const toggleExpand = (client) => {
    setExpanded(prev => ({
      ...prev,
      [client]: !prev[client]
    }));
  };

  // Группируем заказы по клиентам
  const ordersByClient = details.reduce((acc, order) => {
    if (!acc[order.client]) {
      acc[order.client] = [];
    }
    acc[order.client].push(order);
    return acc;
  }, {});

  return (
    <div className="client-orders-container">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col, idx) => (
              <th key={idx}>{col}</th>
            ))}
            <th style={{ width: '50px' }}></th>
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
                    <td key={colIndex}>{row[col]}</td>
                  ))}
                  <td>
                    {!isTotal && hasOrders && (
                      <button
                        className="expand-btn"
                        onClick={() => toggleExpand(client)}
                        title={expanded[client] ? 'Скрыть заказы' : 'Показать заказы'}
                      >
                        {expanded[client] ? '▲' : '▼'}
                      </button>
                    )}
                  </td>
                </tr>
                {!isTotal && expanded[client] && hasOrders && (
                  <tr className="details-row">
                    <td colSpan={columns.length + 1}>
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

