import React from 'react';
import { MapContainer, TileLayer, ZoomControl } from 'react-leaflet';
import { Box } from '@mui/material';

function MapView() {
  const center = [40.7128, -74.006]; // NYC coordinates
  const zoom = 13;

  return (
    <Box
      sx={{
        width: '100%',
        height: 'calc(100vh - 64px)', // Subtract header height
        position: 'relative',
        '& .leaflet-container': {
          width: '100%',
          height: '100%'
        }
      }}
    >
      <MapContainer
        center={center}
        zoom={zoom}
        scrollWheelZoom={true}
        style={{ height: '100%' }}
        zoomControl={false} // We'll add it manually to control position
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <ZoomControl position="topright" />
      </MapContainer>
    </Box>
  );
}

export default MapView;