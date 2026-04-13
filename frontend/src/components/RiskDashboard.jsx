import React from 'react';

export default function RiskDashboard({ data }) {
  if (!data) return null;

  return (
    <div className="risk-dashboard">
      <div className="stats-grid">
        <div className="stat-box">
          <div className="stat-value">{data.elevation}m</div>
          <div className="stat-label">Elevation</div>
        </div>
        <div className="stat-box">
          <div className="stat-value">{data.historical_rainfall_mm}mm</div>
          <div className="stat-label">Yearly Precip</div>
        </div>
        <div className="stat-box" style={{ gridColumn: 'span 2' }}>
          <div className="stat-value">{data.historical_max_temp_c}°C</div>
          <div className="stat-label">Max Historical Temp</div>
        </div>
      </div>

      <div className="recommendation-box">
        <h3>AI Resilience Recommendation</h3>
        <p>{data.recommendation}</p>
      </div>
    </div>
  );
}
