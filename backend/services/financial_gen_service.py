from langchain_community.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, List
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialGenService:
    """
    金融文本生成服务
    提供金融报告、分析报告等金融文本的生成功能
    """
    def __init__(self):
        pass
        
    def _get_llm(self, llm_options: dict):
        """
        根据配置获取语言模型实例
        
        Args:
            llm_options: 语言模型配置选项
            
        Returns:
            配置好的语言模型实例
            
        Raises:
            ValueError: 当提供不支持的模型提供商时
        """
        provider = llm_options.get("provider", "ollama")
        model = llm_options.get("model", "llama3.1:8b")
        
        if provider == "ollama":
            return Ollama(model=model)
        elif provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate_financial_report(self, 
                                market_info: Dict,
                                indicators: List[str],
                                analysis: str,
                                llm_options: dict) -> Dict:
        """
        生成结构化的金融分析报告
        
        Args:
            market_info: 市场信息
            indicators: 技术指标列表
            analysis: 分析结果
            llm_options: 语言模型配置选项
            
        Returns:
            包含输入信息和生成的金融报告的字典
        """
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的金融分析师。
            生成一份详细的金融分析报告，包括以下部分：
            1. 市场概况
            2. 技术指标分析
            3. 基本面分析
            4. 风险评估
            5. 投资建议
            
            使用专业的金融术语，保持客观专业的分析态度。"""),
            ("human", """
            市场信息：
            {market_info}
            
            技术指标：
            {indicators}
            
            分析结果：
            {analysis}
            """)
        ])
        
        chain = prompt | llm
        result = chain.invoke({
            "market_info": str(market_info),
            "indicators": "\n".join(indicators),
            "analysis": analysis
        })
        
        return {
            "input": {
                "market_info": market_info,
                "indicators": indicators,
                "analysis": analysis
            },
            "output": result.content if hasattr(result, 'content') else str(result)
        }

    def generate_market_analysis(self,
                               market_data: Dict,
                               llm_options: dict) -> Dict:
        """
        根据市场数据生成市场分析
        
        Args:
            market_data: 市场数据
            llm_options: 语言模型配置选项
            
        Returns:
            包含输入数据和生成的市场分析的字典
        """
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个金融市场分析师。
            根据提供的市场数据，生成一份详细的市场分析报告。
            包括：
            1. 市场趋势分析
            2. 关键指标解读
            3. 市场情绪分析
            4. 潜在风险提示
            5. 未来展望
            
            使用专业的金融术语，保持客观专业的分析态度。"""),
            ("human", "市场数据：\n{market_data}")
        ])
        
        chain = prompt | llm
        result = chain.invoke({
            "market_data": str(market_data)
        })
        
        return {
            "input": {
                "market_data": market_data
            },
            "output": result.content if hasattr(result, 'content') else str(result)
        }

    def generate_investment_plan(self,
                               investment_goals: Dict,
                               risk_profile: str,
                               llm_options: dict) -> Dict:
        """
        生成投资计划
        
        Args:
            investment_goals: 投资目标
            risk_profile: 风险偏好
            llm_options: 语言模型配置选项
            
        Returns:
            包含输入信息和生成的投资计划的字典
        """
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的投资顾问。
            生成一份全面的投资计划，包括：
            1. 资产配置建议
            2. 投资组合构建
            3. 风险控制措施
            4. 定期评估方案
            5. 调整策略
            
            考虑投资者的风险偏好和投资目标。"""),
            ("human", """
            投资目标：{investment_goals}
            风险偏好：{risk_profile}
            """)
        ])
        
        chain = prompt | llm
        result = chain.invoke({
            "investment_goals": str(investment_goals),
            "risk_profile": risk_profile
        })
        
        return {
            "input": {
                "investment_goals": investment_goals,
                "risk_profile": risk_profile
            },
            "output": result.content if hasattr(result, 'content') else str(result)
        } 