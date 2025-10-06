import React from 'react';
import { Box } from '@mui/material';
import NavTabs from '../navigation/NavTabs';

function PageLayout({ children }) {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100vh',
      width: '100vw',
      overflow: 'hidden'
    }}>
      <NavTabs />
      <Box component="main" sx={{ 
        flexGrow: 1,
        position: 'relative',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {children}
      </Box>
    </Box>
  );
}

export default PageLayout;