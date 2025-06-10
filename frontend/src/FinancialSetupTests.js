// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// 添加金融领域特定的测试配置
beforeAll(() => {
  // 设置金融领域特定的测试环境
  process.env.REACT_APP_FINANCIAL_API_URL = 'http://172.20.116.213:8000/api/financial';
});

afterAll(() => {
  // 清理测试环境
  delete process.env.REACT_APP_FINANCIAL_API_URL;
}); 