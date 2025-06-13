from langchain_community.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict
import os
import logging
import requests

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialCorrService:
    """
    金融文本拼写纠正服务
    提供金融术语拼写错误纠正功能
    """
    def __init__(self):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"
        
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
        provider = llm_options.get("provider", "deepseek")
        model = llm_options.get("model", "deepseek-chat")
        
        if provider == "deepseek":
            if not self.deepseek_api_key:
                raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
            return self._call_deepseek_api
        elif provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=0,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def _call_deepseek_api(self, prompt: str) -> str:
        """
        调用 Deepseek API
        
        Args:
            prompt: 输入提示
            
        Returns:
            API 响应文本
        """
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个金融术语专家。你的任务是纠正文本中的所有拼写错误。特别注意金融术语的拼写。保持所有缩写不变。保持原文的格式和标点符号。不要添加任何解释性文字，只返回纠正后的文本。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }
        
        try:
            response = requests.post(self.deepseek_api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Error calling Deepseek API: {str(e)}")
            raise
        
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
        
        if llm_options.get("provider") == "deepseek":
            corrected_text = llm(text)
        else:
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
            corrected_text = result.content if hasattr(result, 'content') else str(result)
        
        return {
            "input": text,
            "corrected_text": corrected_text
        } 