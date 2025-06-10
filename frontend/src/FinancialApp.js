import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import FinancialSidebar from './components/FinancialSidebar';
import FinancialNERPage from './pages/financial_ner_page';
import FinancialStdPage from './pages/financial_std_page';
import FinancialCorrPage from './pages/financial_corr_page';
import FinancialAbbrPage from './pages/financial_abbr_page';
import FinancialGenPage from './pages/financial_gen_page';

const FinancialWelcomePage = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <img src="/images/financial-img.png" alt="金融文本处理" className="w-96 h-auto mb-8" />
      <h1 className="text-3xl font-bold text-gray-800 mb-4">欢迎使用金融文本处理工具箱</h1>
      <p className="text-xl text-gray-600">请从左侧菜单选择要使用的功能</p>
    </div>
  );
};

const FinancialApp = () => {
  const [sidebarWidth, setSidebarWidth] = useState(250);

  const handleResize = (e) => {
    setSidebarWidth(e.clientX);
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <FinancialSidebar width={sidebarWidth} />
        <div
          className="w-1 cursor-col-resize bg-gray-300 hover:bg-blue-500"
          onMouseDown={() => {
            document.addEventListener('mousemove', handleResize);
            document.addEventListener('mouseup', () => {
              document.removeEventListener('mousemove', handleResize);
            });
          }}
        />
        <main className="flex-1 overflow-y-auto p-5">
          <Routes>
            <Route path="/financial" element={<FinancialWelcomePage />} />
            <Route path="/financial/ner" element={<FinancialNERPage />} />
            <Route path="/financial/std" element={<FinancialStdPage />} />
            <Route path="/financial/corr" element={<FinancialCorrPage />} />
            <Route path="/financial/abbr" element={<FinancialAbbrPage />} />
            <Route path="/financial/gen" element={<FinancialGenPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default FinancialApp; 