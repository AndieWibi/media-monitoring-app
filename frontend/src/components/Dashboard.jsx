import React from 'react';

function Dashboard() {
  return (
    <div className="dashboard-header">
      <div className="dashboard-info">
        <h2>Real-time Media Monitoring Dashboard</h2>
        <p>Track CPO pricing trends, RSPO certification updates, and NGO campaigns in real-time</p>
      </div>
      <div className="dashboard-stats">
        <div className="stat">
          <span className="stat-label">Last Updated</span>
          <span className="stat-value" id="last-updated">Just now</span>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;