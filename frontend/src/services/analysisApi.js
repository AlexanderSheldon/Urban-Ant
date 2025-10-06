// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Analysis endpoints
export const analysisApi = {
  // Get overall transit metrics
  getMetrics: async (timeframe = 'month', region = 'all') => {
    // TODO: Replace with actual API call
    return mockMetricsResponse;
  },

  // Get accessibility trends data
  getTrends: async (params) => {
    // TODO: Replace with actual API call
    return mockTrendsResponse;
  },

  // Get impact distribution data
  getImpactDistribution: async (params) => {
    // TODO: Replace with actual API call
    return mockDistributionResponse;
  }
};

// Mock responses for development
const mockMetricsResponse = {
  accessibility: { value: '78%', trend: { direction: 'up', value: '+5% from last month' } },
  coverage: { value: '65%', trend: { direction: 'up', value: '+2% from last month' } },
  impact: { value: '250k', trend: { direction: 'up', value: '+10k residents served' } },
  efficiency: { value: '92%', trend: { direction: 'down', value: '-3% from last month' } },
};

const mockTrendsResponse = {
  data: [
    { date: new Date('2025-01-01'), value: 65 },
    { date: new Date('2025-02-01'), value: 68 },
    { date: new Date('2025-03-01'), value: 70 },
    { date: new Date('2025-04-01'), value: 72 },
    { date: new Date('2025-05-01'), value: 75 },
    { date: new Date('2025-06-01'), value: 73 },
    { date: new Date('2025-07-01'), value: 76 },
    { date: new Date('2025-08-01'), value: 78 },
    { date: new Date('2025-09-01'), value: 77 },
    { date: new Date('2025-10-01'), value: 78 }
  ]
};

const mockDistributionResponse = {
  data: [
    { label: 'Bus', value: 45 },
    { label: 'Train', value: 30 },
    { label: 'Light Rail', value: 15 },
    { label: 'Bike Paths', value: 10 }
  ]
};

export default analysisApi;