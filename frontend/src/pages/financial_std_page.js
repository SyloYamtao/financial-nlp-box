import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { EmbeddingOptions, TextInput } from '../components/shared/ModelOptions';

const FinancialStdPage = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  // 重新组织选项结构，默认选中所有选项
  const [options, setOptions] = useState({
    stock: true,
    index: true,
    currency: true,
    market: true,
    sector: true,
    investment: true,
    risk: true,
    return: true,
    volatility: true,
    rating: true,
    bond: true,
    derivative: true,
    commodity: true,
    exchange: true,
    regulator: true,
    economicIndicator: true,
    financialRatio: true,
    accountingTerm: true,
    taxTerm: true,
    insuranceTerm: true,
    bankingTerm: true,
    investmentStrategy: true,
    portfolio: true,
    assetClass: true,
    marketSentiment: true,
    tradingTerm: true,
    riskMetric: true,
    performanceMetric: true,
    marketIndex: true,
    economicSector: true,
    financialInstrument: true,
    marketAnalysis: true,
    investmentPhilosophy: true,
    allFinancialTerms: true,
  });

  const [embeddingOptions, setEmbeddingOptions] = useState({
    provider: 'huggingface',
    model: 'BAAI/bge-m3',
    dbName: 'financial_terms_bge_m3',
    collectionName: 'financial_concepts'
  });

  const handleOptionChange = (e) => {
    const { name, checked } = e.target;
    
    if (name === 'allFinancialTerms') {
      // 如果选择 allFinancialTerms，则设置所有选项为相同状态
      setOptions(prevOptions => {
        const newOptions = {};
        Object.keys(prevOptions).forEach(key => {
          newOptions[key] = checked;
        });
        return newOptions;
      });
    } else {
      // 更新单个选项
      setOptions(prevOptions => ({
        ...prevOptions,
        [name]: checked,
        // 如果取消选择任何一个选项，allFinancialTerms 也取消选择
        allFinancialTerms: checked && 
          Object.entries(prevOptions)
            .filter(([key]) => key !== 'allFinancialTerms' && key !== name)
            .every(([, value]) => value)
      }));
    }
  };

  const handleEmbeddingOptionChange = (e) => {
    const { name, value } = e.target;
    setEmbeddingOptions(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setError('');
    setResult('');
    try {
      const response = await fetch('http://172.20.116.213:8000/api/financial/std', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: input, 
          options,
          embeddingOptions 
        }),
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
    } catch (error) {
      console.error('Error:', error);
      setError(`发生错误: ${error.message}`);
    }
    setIsLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融术语标准化 💰</h1>
      <div className="grid grid-cols-3 gap-6">
        {/* 左侧面板：文本输入和嵌入选项 */}
        <div className="col-span-2 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">输入金融术语</h2>
          <TextInput
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={4}
            placeholder="请输入需要标准化的金融术语..."
          />
          
          <EmbeddingOptions options={embeddingOptions} onChange={handleEmbeddingOptionChange} />

          <button
            onClick={handleSubmit}
            className="bg-purple-500 text-white px-4 py-2 rounded-md hover:bg-purple-600 w-full"
            disabled={isLoading}
          >
            {isLoading ? '处理中...' : '标准化术语'}
          </button>
        </div>

        {/* 右侧面板：选项列表 */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">术语类型</h2>
          <div className="space-y-3">
            {[
              ['stock', '股票'],
              ['index', '指数'],
              ['currency', '货币'],
              ['market', '市场'],
              ['sector', '行业'],
              ['investment', '投资'],
              ['risk', '风险'],
              ['return', '收益'],
              ['volatility', '波动性'],
              ['rating', '评级'],
              ['bond', '债券'],
              ['derivative', '衍生品'],
              ['commodity', '商品'],
              ['exchange', '交易所'],
              ['regulator', '监管机构'],
              ['economicIndicator', '经济指标'],
              ['financialRatio', '财务比率'],
              ['accountingTerm', '会计术语'],
              ['taxTerm', '税务术语'],
              ['insuranceTerm', '保险术语'],
              ['bankingTerm', '银行术语'],
              ['investmentStrategy', '投资策略'],
              ['portfolio', '投资组合'],
              ['assetClass', '资产类别'],
              ['marketSentiment', '市场情绪'],
              ['tradingTerm', '交易术语'],
              ['riskMetric', '风险指标'],
              ['performanceMetric', '表现指标'],
              ['marketIndex', '市场指数'],
              ['economicSector', '经济部门'],
              ['financialInstrument', '金融工具'],
              ['marketAnalysis', '市场分析'],
              ['investmentPhilosophy', '投资理念'],
            ].map(([key, label]) => (
              <div key={key} className="flex items-center">
                <input
                  type="checkbox"
                  id={key}
                  name={key}
                  checked={options[key]}
                  onChange={handleOptionChange}
                  className="mr-2"
                />
                <label htmlFor={key}>{label}</label>
              </div>
            ))}
            
            <div className="flex items-center pt-4 border-t">
              <input
                type="checkbox"
                id="allFinancialTerms"
                name="allFinancialTerms"
                checked={options.allFinancialTerms}
                onChange={handleOptionChange}
                className="mr-2"
              />
              <label htmlFor="allFinancialTerms" className="font-semibold">所有金融术语</label>
            </div>
          </div>
        </div>
      </div>
      
      {/* 结果显示区域 */}
      {(error || result) && (
        <div className="mt-6">
          {error && (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
              <p className="font-bold">错误：</p>
              <p>{error}</p>
            </div>
          )}
          {result && (
            <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
              <p className="font-bold">结果：</p>
              <pre>{result}</pre>
            </div>
          )}
        </div>
      )}

      <div className="flex items-center text-yellow-700 bg-yellow-100 p-4 rounded-md mt-6">
        <AlertCircle className="mr-2" />
        <span>这是演示版本, 并非所有功能都可以正常工作。更多功能需要您来增强并实现。</span>
      </div>
    </div>
  );
};

export default FinancialStdPage; 