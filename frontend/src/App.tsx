import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ReactQueryProvider } from './lib/react-query';
import { ThemeProvider } from './lib/theme-provider';
import { ToastProvider } from './lib/toast-provider';
import Dashboard from './pages/Dashboard';
import { Workflows } from './pages/Workflows';
import { NewWorkflow } from './pages/NewWorkflow';
import { WorkflowDetail } from './pages/WorkflowDetail';
import { Agents } from './pages/Agents';

function App() {
  return (
    <ReactQueryProvider>
      <ThemeProvider>
        <ToastProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/workflows" element={<Workflows />} />
              <Route path="/workflows/new" element={<NewWorkflow />} />
              <Route path="/workflows/:workflowId" element={<WorkflowDetail />} />
              <Route path="/agents" element={<Agents />} />
            </Routes>
          </BrowserRouter>
        </ToastProvider>
      </ThemeProvider>
    </ReactQueryProvider>
  );
}

export default App;
