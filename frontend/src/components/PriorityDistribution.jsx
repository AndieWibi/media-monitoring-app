import React from 'react';

function PriorityDistribution({ data }) {
  if (!data || !data.data || data.data.length === 0) {
    return <div>No priority distribution data available</div>;
  }

  const totalCount = data.data.reduce((sum, item) => sum + item.count, 0);
  
  const priorityColors = {
    critical: '#c0392b',
    high: '#e74c3c',
    medium: '#f39c12',
    low: '#27ae60'
  };

  const priorityOrder = ['critical', 'high', 'medium', 'low'];
  const sortedData = data.data.sort((a, b) => {
    return priorityOrder.indexOf(a.priority) - priorityOrder.indexOf(b.priority);
  });

  return (
    <div className="priority-distribution">
      <ul className="distribution-list">
        {sortedData.map((item, index) => {
          const percentage = (item.count / totalCount) * 100;
          const color = priorityColors[item.priority] || '#95a5a6';
          
          return (
            <li key={index} className="distribution-item">
              <span className="distribution-label">{item.priority.toUpperCase()}</span>
              <div className="distribution-bar" style={{
                background: color,
                width: `${percentage}%`,
                minWidth: '50px'
              }}>
                <span className="distribution-count">{percentage.toFixed(1)}%</span>
              </div>
              <span className="distribution-value">{item.count}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default PriorityDistribution;