import React, { useState } from 'react';
import axios from 'axios';
import AddressToRisk from './components/AddressToRisk';
import MapLayout from './components/MapLayout';
import RiskDashboard from './components/RiskDashboard';

function App() {
  const [loading, setLoading] = useState(false);
  const [riskData, setRiskData] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const handleSearch = async (address) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/api/assess-risk`, {
        address,
        land_cover: "Urban"
      });
      setRiskData(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to process risk assessment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <div className="branding">
          <h1 style={{ margin: 0, color: 'var(--accent)' }}>GeoGuard</h1>
          <p style={{ margin: '0.25rem 0', color: 'var(--text-muted)' }}>Geospatial Risk Assessment Engine</p>
        </div>
        
        <AddressToRisk onSearch={handleSearch} loading={loading} />
        
        {error && (
          <div className="error-message" style={{ color: 'var(--danger)', padding: '1rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px' }}>
            {error}
          </div>
        )}

        {riskData && <RiskDashboard data={riskData} />}
      </div>
      <div className="map-container">
        <MapLayout riskData={riskData} />
      </div>
    </div>
  );
}

export default App;
