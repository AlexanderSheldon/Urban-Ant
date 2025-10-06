import React, { useState, useEffect } from 'react';
import { Box, Grid, Typography, Paper, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import MetricCard from '../analysis/MetricCard';
import AnalysisChart from '../analysis/AnalysisChart';
import LineChart from '../charts/LineChart';
import DonutChart from '../charts/DonutChart';
import { analysisApi } from '../../services/analysisApi';

// Mock data - replace with API calls later
const mockMetrics = {
  accessibility: { value: '78%', trend: { direction: 'up', value: '+5% from last month' } },
  coverage: { value: '65%', trend: { direction: 'up', value: '+2% from last month' } },
  impact: { value: '250k', trend: { direction: 'up', value: '+10k residents served' } },
  efficiency: { value: '92%', trend: { direction: 'down', value: '-3% from last month' } },
};

function AnalysisView() {
  const [timeframe, setTimeframe] = useState('month');
  const [region, setRegion] = useState('all');
  const [metrics, setMetrics] = useState(mockMetrics);
  const [trendsData, setTrendsData] = useState([]);
  const [distributionData, setDistributionData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsData, trends, distribution] = await Promise.all([
          analysisApi.getMetrics(timeframe, region),
          analysisApi.getTrends({ timeframe, region }),
          analysisApi.getImpactDistribution({ region })
        ]);

        setMetrics(metricsData);
        setTrendsData(trends.data);
        setDistributionData(distribution.data);
      } catch (error) {
        console.error('Error fetching analysis data:', error);
      }
    };

    fetchData();
  }, [timeframe, region]);

  return (
    <Box sx={{ p: 3, height: '100%', overflow: 'auto' }}>
      {/* Header and Filters */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4">Transit Analysis</Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Timeframe</InputLabel>
              <Select
                value={timeframe}
                label="Timeframe"
                onChange={(e) => setTimeframe(e.target.value)}
              >
                <MenuItem value="week">Week</MenuItem>
                <MenuItem value="month">Month</MenuItem>
                <MenuItem value="quarter">Quarter</MenuItem>
                <MenuItem value="year">Year</MenuItem>
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Region</InputLabel>
              <Select
                value={region}
                label="Region"
                onChange={(e) => setRegion(e.target.value)}
              >
                <MenuItem value="all">All Regions</MenuItem>
                <MenuItem value="north">North</MenuItem>
                <MenuItem value="south">South</MenuItem>
                <MenuItem value="east">East</MenuItem>
                <MenuItem value="west">West</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>

        {/* Metrics Grid */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Transit Accessibility Score"
              value={mockMetrics.accessibility.value}
              description="Overall accessibility rating based on coverage and frequency"
              trend={mockMetrics.accessibility.trend}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Area Coverage"
              value={mockMetrics.coverage.value}
              description="Percentage of urban area with transit access"
              trend={mockMetrics.coverage.trend}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="Population Impact"
              value={mockMetrics.impact.value}
              description="Number of residents served by transit"
              trend={mockMetrics.impact.trend}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <MetricCard
              title="System Efficiency"
              value={mockMetrics.efficiency.value}
              description="Overall system performance score"
              trend={mockMetrics.efficiency.trend}
            />
          </Grid>
        </Grid>

        {/* Charts Grid */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <AnalysisChart
              title="Accessibility Trends"
              description="Historical view of transit accessibility scores"
              tags={['Accessibility', 'Historical', 'Trends']}
            >
              <Box sx={{ height: '300px', width: '100%' }}>
                <LineChart
                  data={trendsData}
                  width={800}
                  height={300}
                  margin={{ top: 20, right: 30, bottom: 30, left: 40 }}
                />
              </Box>
            </AnalysisChart>
          </Grid>
          <Grid item xs={12} md={4}>
            <AnalysisChart
              title="Impact Distribution"
              description="Population served by transit type"
              tags={['Demographics', 'Distribution']}
            >
              <Box sx={{ height: '300px', width: '100%' }}>
                <DonutChart
                  data={distributionData}
                  width={400}
                  height={300}
                  margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                />
              </Box>
            </AnalysisChart>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}

export default AnalysisView;