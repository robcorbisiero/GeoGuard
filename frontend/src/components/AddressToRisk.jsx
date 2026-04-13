import React, { useState } from 'react';
import { Search } from 'lucide-react';

export default function AddressToRisk({ onSearch, loading }) {
  const [address, setAddress] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (address.trim()) {
      onSearch(address);
    }
  };

  return (
    <div className="search-container">
      <h2>Address-to-Risk Scan</h2>
      <form onSubmit={handleSubmit} className="search-form">
        <input 
          type="text" 
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="Enter a street address..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !address.trim()}>
          {loading ? 'Scanning...' : <><Search size={18} /> Analyze Risk</>}
        </button>
      </form>
    </div>
  );
}
