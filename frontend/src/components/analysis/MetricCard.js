import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

function MetricCard({ title, value, description, trend }) {
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" color="textSecondary" gutterBottom>
          {title}
        </Typography>
        <Typography variant="h4" component="div">
          {value}
        </Typography>
        {trend && (
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
            <Typography 
              variant="body2" 
              color={trend.direction === 'up' ? 'success.main' : 'error.main'}
            >
              {trend.value}
            </Typography>
          </Box>
        )}
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          {description}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default MetricCard;