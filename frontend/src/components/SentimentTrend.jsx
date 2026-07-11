import React from 'react';

function SentimentTrend({ data }) {
  if (!data || !data.data) {
    return <div>No sentiment data available</div>;
  }

  // Convert data to array format for display
  const timePoints = Object.keys(data.data).sort();
  
  // Get sentiment categories
  const sentiments = new Set();
  timePoints.forEach(time => {
    Object.keys(data.data[time]).forEach(sentiment => {
      sentiments.add(sentiment);
    });
  });

  const colors = {
    positive: '#27ae60',
    negative: '#e74c3c',
    neutral: '#95a5a6',
    mixed: '#f39c12'
  };

  return (
    <div className="sentiment-trend">
      <div className="chart-container">
        <div className="sentiment-summary">
          {Array.from(sentiments).map(sentiment => {
            const totalCount = timePoints.reduce((sum, time) => {
              return sum + (data.data[time][sentiment] || 0);
            }, 0);
            
            return (
              <div key={sentiment} className="sentiment-bar" style={{borderLeftColor: colors[sentiment]}}>
                <span className="sentiment-name">{sentiment}</span>
                <span className="sentiment-count">{totalCount}</span>
              </div>
            );
          })}
        </div>
      </div>
      <div className="data-points">
        {timePoints.slice(-12).map(time => (
          <div key={time} className="time-point">
            <span className="time">{new Date(time).toLocaleTimeString()}</span>
            <div className="sentiments-at-time">
              {Array.from(sentiments).map(sentiment => (
                <div key={sentiment} className="sentiment-indicator" style={{backgroundColor: colors[sentiment]}}>
                  <span title={sentiment}>{data.data[time][sentiment] || 0}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SentimentTrend;