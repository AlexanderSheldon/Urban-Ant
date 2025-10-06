import React from 'react';
import { Tabs, Tab, AppBar, Box } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import MapIcon from '@mui/icons-material/Map';
import TimelineIcon from '@mui/icons-material/Timeline';
import AnalyticsIcon from '@mui/icons-material/Analytics';

const routes = [
  { path: '/', label: 'Map', icon: <MapIcon /> },
  { path: '/scenarios', label: 'Scenarios', icon: <TimelineIcon /> },
  { path: '/analysis', label: 'Analysis', icon: <AnalyticsIcon /> },
];

function NavTabs() {
  const location = useLocation();
  const navigate = useNavigate();

  const handleChange = (event, newValue) => {
    navigate(newValue);
  };

  return (
    <AppBar 
      position="static" 
      color="default" 
      sx={{ 
        zIndex: (theme) => theme.zIndex.drawer + 1,
        backgroundColor: 'background.paper',
        borderBottom: 1,
        borderColor: 'divider'
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', px: 2 }}>
        <Tabs
          value={location.pathname}
          onChange={handleChange}
          indicatorColor="primary"
          textColor="primary"
          variant="scrollable"
          scrollButtons="auto"
          sx={{ flex: 1 }}
        >
          {routes.map((route) => (
            <Tab
              key={route.path}
              value={route.path}
              label={route.label}
              icon={route.icon}
              iconPosition="start"
              sx={{
                minHeight: 48,
                textTransform: 'none',
                fontSize: '1rem',
              }}
            />
          ))}
        </Tabs>
      </Box>
    </AppBar>
  );
}

export default NavTabs;