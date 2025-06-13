import React from 'react';

// LLM选项组件
export const LLMOptions = ({ options, onChange }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700">大语言模型</label>
      <div className="mt-1 grid grid-cols-2 gap-2">
        <div>
          <label className="block text-xs text-gray-500">供应商</label>
          <select
            name="provider"
            value={options.provider}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          >
            <option value="deepseek">DeepSeek</option>
          </select>
        </div>
        <div>
          <label className="block text-xs text-gray-500">模型</label>
          <select
            name="model"
            value={options.model}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          >
            <option value="deepseek-v3">DeepSeek-V3</option>
          </select>
        </div>
      </div>
    </div>
  );
};

// 向量数据库选项组件
export const EmbeddingOptions = ({ options, onChange }) => {
  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700">向量数据库</label>
      <div className="mt-1 grid grid-cols-2 gap-2">
        <div>
          <label className="block text-xs text-gray-500">供应商</label>
          <select
            name="provider"
            value={options.provider}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          >
            <option value="huggingface">HuggingFace</option>
          </select>
        </div>
        <div>
          <label className="block text-xs text-gray-500">模型</label>
          <select
            name="model"
            value={options.model}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          >
            <option value="BAAI/bge-m3">BAAI/bge-m3</option>
          </select>
        </div>
        <div>
          <label className="block text-xs text-gray-500">数据库名称</label>
          <input
            type="text"
            name="dbName"
            value={options.dbName}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label className="block text-xs text-gray-500">集合名称</label>
          <input
            type="text"
            name="collectionName"
            value={options.collectionName}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
      </div>
    </div>
  );
};

// 通用输入文本区域组件
export const TextInput = ({ value, onChange, placeholder, rows = 4 }) => {
  return (
    <div className="mb-4">
      <textarea
        value={value}
        onChange={onChange}
        rows={rows}
        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
        placeholder={placeholder}
      />
    </div>
  );
}; 