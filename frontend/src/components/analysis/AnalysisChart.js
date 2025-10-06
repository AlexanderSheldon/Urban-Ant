import React from 'react';
import { Paper, Box, Typography, Chip } from '@mui/material';

function AnalysisChart({ title, description, tags, children }) {
  return (
    <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
      <Box sx={{ mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body2" color="textSecondary" paragraph>
          {description}
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {tags?.map((tag, index) => (
            <Chip
              key={index}
              label={tag}
              size="small"
              color="primary"
              variant="outlined"
            />
          ))}
        </Box>
      </Box>
      <Box sx={{ height: 'calc(100% - 100px)' }}>
        {children}
      </Box>
    </Paper>
  );
}

export default AnalysisChart;