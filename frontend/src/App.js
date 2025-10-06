import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline, ThemeProvider } from '@mui/material';
import MapView from './components/MapView';
import ScenariosView from './components/views/ScenariosView';
import AnalysisView from './components/views/AnalysisView';
import PageLayout from './components/layout/PageLayout';
import theme from './theme';
import './App.css';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <PageLayout>
          <Routes>
            <Route path="/" element={<MapView />} />
            <Route path="/scenarios" element={<ScenariosView />} />
            <Route path="/analysis" element={<AnalysisView />} />
          </Routes>
        </PageLayout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
