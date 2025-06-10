import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { LLMOptions, TextInput } from '../components/shared/ModelOptions';

const FinancialGenPage = () => {
  // 基础状态
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState('');
  
  // 方法选择
  const [method, setMethod] = useState('generate_financial_report');
  const methods = {
    generate_financial_report: '生成金融分析报告',
    generate_market_analysis: '生成市场分析',
    generate_investment_plan: '生成投资计划'
  };

  // 市场信息
  const [marketInfo, setMarketInfo] = useState({
    market: '',
    sector: '',
    period: '',
    marketTrend: ''
  });

  // 技术指标和分析
  const [indicators, setIndicators] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [investmentGoals, setInvestmentGoals] = useState('');
  const [riskProfile, setRiskProfile] = useState('');

  // LLM 选项
  const [llmOptions, setLlmOptions] = useState({
    provider: 'ollama',
    model: 'qwen2.5:7b'
  });

  const handleMarketInfoChange = (e) => {
    const { name, value } = e.target;
    setMarketInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLlmOptionChange = (e) => {
    const { name, value } = e.target;
    setLlmOptions(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleIndicatorsChange = (e) => {
    setIndicators(e.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://172.20.116.213:8000/api/financial/gen', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          market_info: marketInfo,
          indicators: indicators.split('\n').filter(s => s.trim()),
          analysis,
          investment_goals: investmentGoals,
          risk_profile: riskProfile,
          method,
          llmOptions
        }),
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Error:', error);
      setResult('处理请求时发生错误。');
    }
    setIsLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融内容生成 💰</h1>
      
      <div className="grid grid-cols-3 gap-6">
        {/* 左侧面板：输入表单 */}
        <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">市场信息</h2>
          
          {/* 市场基本信息 */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">市场</label>
              <input
                type="text"
                name="market"
                value={marketInfo.market}
                onChange={handleMarketInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">行业</label>
              <input
                type="text"
                name="sector"
                value={marketInfo.sector}
                onChange={handleMarketInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">周期</label>
              <input
                type="text"
                name="period"
                value={marketInfo.period}
                onChange={handleMarketInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">市场趋势</label>
              <input
                type="text"
                name="marketTrend"
                value={marketInfo.marketTrend}
                onChange={handleMarketInfoChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                placeholder="市场趋势描述..."
              />
            </div>
          </div>

          {/* 技术指标输入 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">技术指标（每行一个）</label>
            <TextInput
              value={indicators}
              onChange={handleIndicatorsChange}
              rows={3}
              placeholder="输入技术指标，每行一个..."
            />
          </div>

          {/* 分析信息（仅在生成金融报告时显示） */}
          {method === 'generate_financial_report' && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700">分析</label>
              <input
                type="text"
                value={analysis}
                onChange={(e) => setAnalysis(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                placeholder="输入分析内容..."
              />
            </div>
          )}

          {/* 投资目标和风险偏好（仅在生成投资计划时显示） */}
          {method === 'generate_investment_plan' && (
            <>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">投资目标</label>
                <input
                  type="text"
                  value={investmentGoals}
                  onChange={(e) => setInvestmentGoals(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  placeholder="输入投资目标..."
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">风险偏好</label>
                <select
                  value={riskProfile}
                  onChange={(e) => setRiskProfile(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                >
                  <option value="">选择风险偏好</option>
                  <option value="conservative">保守型</option>
                  <option value="moderate">稳健型</option>
                  <option value="aggressive">激进型</option>
                </select>
              </div>
            </>
          )}

          <button
            onClick={handleSubmit}
            className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 w-full"
            disabled={isLoading}
          >
            {isLoading ? '生成中...' : '生成内容'}
          </button>
        </div>

        {/* 右侧面板：选项 */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">选项</h2>
          
          {/* 方法选择 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">生成方法</label>
            <select
              value={method}
              onChange={(e) => setMethod(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            >
              {Object.entries(methods).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          {/* LLM 选项 */}
          <LLMOptions options={llmOptions} onChange={handleLlmOptionChange} />
        </div>
      </div>

      {/* 结果显示 */}
      {result && (
        <div className="mt-6">
          <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-6" role="alert">
            <p className="font-bold">生成结果：</p>
            <pre className="whitespace-pre-wrap">{result}</pre>
          </div>
        </div>
      )}

      <div className="flex items-center text-yellow-700 bg-yellow-100 p-4 rounded-md mt-6">
        <AlertCircle className="mr-2" />
        <span>这是演示版本, 并非所有功能都可以正常工作。更多功能需要您来增强并实现。</span>
      </div>
    </div>
  );
};

export default FinancialGenPage; 