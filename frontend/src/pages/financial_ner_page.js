import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import { TextInput } from '../components/shared/ModelOptions';

const color_map = {
  'ORG': "#FF9800", // 组织
  'MISC': "#E91E63", // 其他
  'FINANCIAL_TERM': "#FF0000", // 金融术语
  'STOCK': "#673AB7", // 股票
  'INDEX': "#3F51B5", // 指数
  'CURRENCY': "#2196F3", // 货币
  'MARKET': "#03A9F4", // 市场
  'SECTOR': "#00BCD4", // 行业
  'INVESTMENT': "#009688", // 投资
  'RISK': "#4CAF50", // 风险
  'RETURN': "#8BC34A", // 收益
  'VOLATILITY': "#CDDC39", // 波动性
  'RATING': "#FFEB3B", // 评级
  'BOND': "#FFC107", // 债券
  'DERIVATIVE': "#FF9800", // 衍生品
  'COMMODITY': "#FF5722", // 商品
  'EXCHANGE': "#795548", // 交易所
  'REGULATOR': "#607D8B", // 监管机构
  'ECONOMIC_INDICATOR': "#D32F2F", // 经济指标
  'FINANCIAL_RATIO': "#C2185B", // 财务比率
  'ACCOUNTING_TERM': "#7B1FA2", // 会计术语
  'TAX_TERM': "#512DA8", // 税务术语
  'INSURANCE_TERM': "#303F9F", // 保险术语
  'BANKING_TERM': "#1976D2", // 银行术语
  'INVESTMENT_STRATEGY': "#0288D1", // 投资策略
  'PORTFOLIO': "#0097A7", // 投资组合
  'ASSET_CLASS': "#00796B", // 资产类别
  'MARKET_SENTIMENT': "#388E3C", // 市场情绪
  'TRADING_TERM': "#689F38", // 交易术语
  'RISK_METRIC': "#AFB42B", // 风险指标
  'PERFORMANCE_METRIC': "#FBC02D", // 表现指标
  'MARKET_INDEX': "#FFA000", // 市场指数
  'ECONOMIC_SECTOR': "#F57C00", // 经济部门
  'FINANCIAL_INSTRUMENT': "#E64A19", // 金融工具
  'MARKET_ANALYSIS': "#5D4037", // 市场分析
  'INVESTMENT_PHILOSOPHY': "#616161", // 投资理念
  'OTHER_ENTITY': "#455A64", // 其他实体
  'OTHER_EVENT': "#C62828", // 其他事件
  'COMBINED_FINANCIAL_TERM': "#FF4500", // 合并金融术语
};

const FinancialNERPage = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [coloredResult, setColoredResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [termTypes, setTermTypes] = useState({
    stock: false,
    index: false,
    financialTerm: false,
    allFinancialTerms: false,
  });
  const [options, setOptions] = useState({
    combineFinancialTerms: false,
  });

  const handleTermTypeChange = (e) => {
    const { name, checked } = e.target;
    if (name === 'allFinancialTerms') {
      setTermTypes({
        stock: false,
        index: false,
        financialTerm: false,
        allFinancialTerms: checked,
      });
    } else {
      setTermTypes({ ...termTypes, [name]: checked });
    }
  };

  const handleOptionChange = (e) => {
    setOptions({ ...options, [e.target.name]: e.target.checked });
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://172.20.116.213:8000/api/financial/ner', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input, options, termTypes }),
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
      setColoredResult(generateColoredResult(data.text, data.entities));
    } catch (error) {
      console.error('Error:', error);
      setResult('处理请求时发生错误。');
      setColoredResult('');
    }
    setIsLoading(false);
  };

  const generateColoredResult = (text, entities) => {
    let result = text;
    entities.sort((a, b) => b.start - a.start);
    
    for (const entity of entities) {
      const color = color_map[entity.entity_group] || '#000000';
      let highlightedEntity;
      
      if (entity.entity_group === 'COMBINED_FINANCIAL_TERM' && entity.original_entities) {
        const [term1, term2] = entity.original_entities;
        highlightedEntity = `<span style="background-color: ${color}; padding: 2px; border-radius: 3px;">
          <span style="border-bottom: 2px solid ${color_map[term1.entity_group]};">${term1.word}</span> 
          <span style="border-bottom: 2px solid ${color_map[term2.entity_group]};">${term2.word}</span>
          <sub>${term1.entity_group}+${term2.entity_group}</sub>
        </span>`;
      } else {
        highlightedEntity = `<span style="background-color: ${color}; padding: 2px; border-radius: 3px;">
          ${entity.word}<sub>${entity.entity_group}</sub>
        </span>`;
      }
      
      result = result.slice(0, entity.start) + highlightedEntity + result.slice(entity.end);
    }
    
    return result;
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">金融实体识别 💰</h1>
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">输入金融文本</h2>
        <TextInput
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={4}
          placeholder="请输入需要进行实体识别的金融文本..."
        />
        
        <h3 className="text-lg font-semibold mb-2">金融术语类型</h3>
        <div className="mb-4">
          <label>
            <input
              type="checkbox"
              name="stock"
              checked={termTypes.stock}
              onChange={handleTermTypeChange}
            />
            股票
          </label>
          <label className="ml-4">
            <input
              type="checkbox"
              name="index"
              checked={termTypes.index}
              onChange={handleTermTypeChange}
            />
            指数
          </label>
          <label className="ml-4">
            <input
              type="checkbox"
              name="financialTerm"
              checked={termTypes.financialTerm}
              onChange={handleTermTypeChange}
            />
            金融术语
          </label>
          <label className="ml-4">
            <input
              type="checkbox"
              name="allFinancialTerms"
              checked={termTypes.allFinancialTerms}
              onChange={handleTermTypeChange}
            />
            所有金融术语
          </label>
        </div>

        <h3 className="text-lg font-semibold mb-2">选项</h3>
        <div className="mb-4">
          <label>
            <input
              type="checkbox"
              name="combineFinancialTerms"
              checked={options.combineFinancialTerms}
              onChange={handleOptionChange}
            />
            合并相关金融术语
          </label>
        </div>

        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className={`bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isLoading ? '处理中...' : '识别实体'}
        </button>
      </div>
      {coloredResult && (
        <div className="bg-white shadow-md rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">识别结果</h2>
          <div 
            dangerouslySetInnerHTML={{ __html: coloredResult }} 
            style={{
              lineHeight: '2',
              wordBreak: 'break-word'
            }}
          />
        </div>
      )}
      {result && (
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-6" role="alert">
          <p className="font-bold">JSON 结果：</p>
          <pre>{result}</pre>
        </div>
      )}
      <div className="flex items-center text-yellow-700 bg-yellow-100 p-4 rounded-md">
        <AlertCircle className="mr-2" />
        <span>这是演示版本, 并非所有功能都可以正常工作。更多功能需要您来增强并实现。</span>
      </div>
    </div>
  );
};

export default FinancialNERPage; 