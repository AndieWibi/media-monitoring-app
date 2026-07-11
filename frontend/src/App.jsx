import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import SentimentTrend from './components/SentimentTrend';
import TrendingKeywords from './components/TrendingKeywords';
import SourceDistribution from './components/SourceDistribution';
import PriorityDistribution from './components/PriorityDistribution';

function App() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch initial metrics
    const fetchInitialMetrics = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/dashboard/metrics/current');
        if (!response.ok) throw new Error('Failed to fetch metrics');
        const data = await response.json();
        setMetrics(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchInitialMetrics();
  }, []);

  useEffect(() => {
    // Connect to WebSocket for real-time updates
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//localhost:8000/api/dashboard/ws/metrics`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnected(true);
      // Send initial subscription message
      ws.send(JSON.stringify({ type: 'subscribe', metric_type: 'all' }));
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'metrics_update') {
          // Update metrics from WebSocket broadcast
          const newMetrics = {};
          data.metrics.forEach(metric => {
            newMetrics[metric.type] = metric;
          });
          setMetrics(prev => ({ ...prev, ...newMetrics }));
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    ws.onerror = (err) => {
      console.error('WebSocket error:', err);
      setConnected(false);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setConnected(false);
      // Attempt to reconnect after 3 seconds
      setTimeout(() => {
        console.log('Attempting to reconnect...');
      }, 3000);
    };

    return () => ws.close();
  }, []);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>🌴 Palm Oil Media Monitor</h1>
        <div className="status">
          <span className={`status-indicator ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? '🟢 Live' : '🔴 Offline'}
          </span>
        </div>
      </header>

      <main className="dashboard-container">
        <Dashboard />
        
        <div className="metrics-grid">
          <section className="metric-card">
            <h2>📈 Sentiment Trend (Last Hour)</h2>
            {metrics?.sentiment_trend && <SentimentTrend data={metrics.sentiment_trend} />}
          </section>

          <section className="metric-card">
            <h2>🔥 Trending Keywords</h2>
            {metrics?.trending_keywords && <TrendingKeywords data={metrics.trending_keywords} />}
          </section>

          <section className="metric-card">
            <h2>📰 Source Distribution</h2>
            {metrics?.source_distribution && <SourceDistribution data={metrics.source_distribution} />}
          </section>

          <section className="metric-card">
            <h2>⚠️ Priority Distribution</h2>
            {metrics?.priority_distribution && <PriorityDistribution data={metrics.priority_distribution} />}
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;