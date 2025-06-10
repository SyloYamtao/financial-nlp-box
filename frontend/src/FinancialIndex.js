import React from 'react';
import ReactDOM from 'react-dom/client';
import './FinancialIndex.css';
import FinancialApp from './FinancialApp';
import reportFinancialWebVitals from './FinancialReportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <FinancialApp />
  </React.StrictMode>
);

// 性能监控
reportFinancialWebVitals(); 