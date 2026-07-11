import React from 'react';

function TrendingKeywords({ data }) {
  if (!data || !data.data || data.data.length === 0) {
    return <div>No trending keywords data available</div>;
  }

  const maxCount = Math.max(...data.data.map(item => item.count));

  return (
    <div className="trending-keywords">
      <ul className="keywords-list">
        {data.data.map((item, index) => (
          <li key={index} className="keyword-item">
            <span className="keyword-rank">#{index + 1}</span>
            <span className="keyword-name">{item.keyword}</span>
            <div className="keyword-bar" style={{width: `${(item.count / maxCount) * 100}%`}}>
              <span className="keyword-count">{item.count}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TrendingKeywords;