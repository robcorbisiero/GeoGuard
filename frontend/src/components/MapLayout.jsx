import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png'
});

function ChangeView({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.setView(center, 12, { animate: true });
    }
  }, [center, map]);
  return null;
}

export default function MapLayout({ riskData }) {
  const defaultCenter = [39.8283, -98.5795]; 
  const center = riskData ? [riskData.lat, riskData.lon] : defaultCenter;

  return (
    <MapContainer center={center} zoom={4} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
      />
      <ChangeView center={riskData ? center : null} />
      {riskData && (
        <>
          <Marker position={center}>
            <Popup>
              Assessed Risk Location <br/>
              Elev: {riskData.elevation}m
            </Popup>
          </Marker>
          <Circle 
            center={center} 
            pathOptions={{ color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.2, weight: 1 }} 
            radius={5000} 
          />
        </>
      )}
    </MapContainer>
  );
}
