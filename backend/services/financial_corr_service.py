from langchain_community.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialCorrService:
    """
    金融文本拼写纠正服务
    提供金融术语拼写错误纠正功能
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
                temperature=0,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
    def correct_spelling(self, text: str, llm_options: dict) -> Dict:
        """
        使用语言模型纠正文本中的拼写错误
        
        Args:
            text: 需要纠正的文本
            llm_options: 语言模型配置选项
            
        Returns:
            包含原始文本和纠正后文本的字典
        """
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个金融术语专家。你的任务是纠正文本中的所有拼写错误。
            特别注意金融术语的拼写。
            保持所有缩写不变。
            保持原文的格式和标点符号。
            不要添加任何解释性文字，只返回纠正后的文本。"""),
            ("human", "{input}"),
        ])
        
        chain = prompt | llm
        result = chain.invoke({"input": text})
        
        # 处理可能的AIMessage对象
        corrected_text = result.content if hasattr(result, 'content') else str(result)
        
        return {
            "input": text,
            "corrected_text": corrected_text
        } 