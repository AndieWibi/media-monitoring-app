import React from 'react';

function SourceDistribution({ data }) {
  if (!data || !data.data || data.data.length === 0) {
    return <div>No source distribution data available</div>;
  }

  const totalCount = data.data.reduce((sum, item) => sum + item.count, 0);
  
  const sourceColors = {
    national_media: '#3498db',
    regional_media: '#2ecc71',
    international_media: '#e74c3c',
    journal: '#f39c12',
    social_media_linkedin: '#9b59b6',
    social_media_facebook: '#1abc9c',
    social_media_instagram: '#e91e63'
  };

  return (
    <div className="source-distribution">
      <ul className="distribution-list">
        {data.data.map((item, index) => {
          const percentage = (item.count / totalCount) * 100;
          const color = sourceColors[item.source] || '#95a5a6';
          
          return (
            <li key={index} className="distribution-item">
              <span className="distribution-label">{item.source.replace(/_/g, ' ')}</span>
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

export default SourceDistribution;