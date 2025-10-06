import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

function ScenariosView() {
  return (
    <Box sx={{ p: 3, height: '100%', overflow: 'auto' }}>
      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Transit Scenarios
        </Typography>
        <Typography variant="body1" paragraph>
          This section will allow you to model different transit scenarios and analyze their impact on accessibility.
          You'll be able to:
        </Typography>
        <ul>
          <li>Add or modify bus stops</li>
          <li>Extend train lines</li>
          <li>Plan new bike paths</li>
          <li>Analyze cost-benefit ratios</li>
        </ul>
      </Paper>
    </Box>
  );
}

export default ScenariosView;