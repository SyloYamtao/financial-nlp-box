from langchain_community.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import Runnable
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.messages import HumanMessage, SystemMessage
from typing import Dict, Any, List, Optional
import os
import logging
import requests
import json
from services.financial_std_service import FinancialStdService

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepseekLLM(Runnable):
    """Deepseek LLM 实现"""
    
    def __init__(self, model_name: str):
        self.model = "deepseek-chat"  # 使用正确的模型名称
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # 更新API URL
        logger.info(f"初始化DeepseekLLM: model={self.model}, api_key前6位={self.api_key[:6] if self.api_key else 'None'}")
        
    def invoke(self, input: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> str:
        """实现Runnable接口的invoke方法"""
        # 处理不同类型的输入
        if isinstance(input, dict) and "messages" in input:
            messages = input["messages"]
        elif hasattr(input, "messages"):
            messages = input.messages
        else:
            raise ValueError("Invalid input format")
        
        # 转换消息格式
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, (HumanMessage, SystemMessage)):
                formatted_messages.append({
                    "role": "user" if isinstance(msg, HumanMessage) else "system",
                    "content": msg.content
                })
            elif isinstance(msg, tuple):
                formatted_messages.append({
                    "role": msg[0],
                    "content": msg[1]
                })
            elif isinstance(msg, dict):
                formatted_messages.append(msg)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": 0
        }
        
        logger.info("发送请求到Deepseek API:")
        logger.info(f"URL: {self.api_url}")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info(f"Request Data: {json.dumps(data, indent=2)}")
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            logger.info(f"API响应: {json.dumps(result, indent=2)}")
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}")
            logger.error(f"响应状态码: {e.response.status_code if hasattr(e, 'response') else 'N/A'}")
            logger.error(f"响应内容: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            raise

class FinancialAbbrService:
    """
    金融术语缩写服务
    提供金融术语的缩写和展开功能
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
        model = llm_options.get("model", "deepseek-chat")  # 更新默认模型名称
        
        logger.info(f"创建LLM实例: provider={provider}, model={model}")
        
        if provider == "ollama":
            return Ollama(model=model)
        elif provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=0,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "deepseek":
            return DeepseekLLM(model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
            
    def _query_vector_db(self, text: str, embedding_options: dict) -> List[Dict]:
        """
        查询向量数据库获取相似术语
        
        Args:
            text: 查询文本
            embedding_options: 向量数据库配置选项
            
        Returns:
            相似术语列表
        """
        logger.info(f"开始查询向量数据库: text={text}, options={embedding_options}")
        
        try:
            # 初始化标准化服务
            std_service = FinancialStdService(
                provider=embedding_options.get("provider", "huggingface"),
                model=embedding_options.get("model", "BAAI/bge-m3"),
                db_path=f"db/{embedding_options.get('dbName', 'financial_terms_bge_m3')}.db",
                collection_name=embedding_options.get("collectionName", "financial_concepts")
            )
            
            # 查询相似术语
            results = std_service.search_similar_terms(text, limit=5, threshold=0.1)
            logger.info(f"向量数据库查询结果: {json.dumps(results, indent=2)}")
            
            return results
        except Exception as e:
            logger.error(f"向量数据库查询失败: {str(e)}")
            raise
        
    def expand_abbreviations(self, text: str, llm_options: dict, embedding_options: Optional[dict] = None) -> Dict:
        """
        展开文本中的金融术语缩写
        
        Args:
            text: 包含缩写的文本
            llm_options: 语言模型配置选项
            embedding_options: 向量数据库配置选项
            
        Returns:
            包含原始文本和展开后文本的字典
        """
        logger.info(f"开始展开缩写: text={text}, llm_options={llm_options}, embedding_options={embedding_options}")
        
        # 如果提供了向量数据库配置，先查询向量数据库
        if embedding_options:
            similar_terms = self._query_vector_db(text, embedding_options)
            logger.info(f"找到相似术语: {json.dumps(similar_terms, indent=2)}")
            
            # 构建包含相似术语的提示
            context = "已知的相似金融术语：\n" + "\n".join([
                f"- {term['concept_name']}: {term.get('synonyms', '')}"
                for term in similar_terms
            ])
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """你是一个金融术语专家。你的任务是展开文本中的所有金融术语缩写。
                只展开金融相关的缩写，保持其他缩写不变。
                保持原文的格式和标点符号。
                不要添加任何解释性文字，只返回展开后的文本。
                
                {context}"""),
                ("human", "{input}"),
            ])
            
            chain = prompt | self._get_llm(llm_options) | StrOutputParser()
            expanded_text = chain.invoke({
                "input": text,
                "context": context
            })
        else:
            # 使用简单的LLM展开
            prompt = ChatPromptTemplate.from_messages([
                ("system", """你是一个金融术语专家。你的任务是展开文本中的所有金融术语缩写。
                只展开金融相关的缩写，保持其他缩写不变。
                保持原文的格式和标点符号。
                不要添加任何解释性文字，只返回展开后的文本。"""),
                ("human", "{input}"),
            ])
            
            chain = prompt | self._get_llm(llm_options) | StrOutputParser()
            expanded_text = chain.invoke({"input": text})
        
        logger.info(f"缩写展开完成: expanded_text={expanded_text}")
        
        return {
            "input": text,
            "expanded_text": expanded_text,
            "similar_terms": similar_terms if embedding_options else None
        }
        
    def create_abbreviations(self, text: str, llm_options: dict) -> Dict:
        """
        将文本中的金融术语转换为缩写形式
        
        Args:
            text: 需要转换的文本
            llm_options: 语言模型配置选项
            
        Returns:
            包含原始文本和缩写后文本的字典
        """
        logger.info(f"开始创建缩写: text={text}, llm_options={llm_options}")
        
        llm = self._get_llm(llm_options)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个金融术语专家。你的任务是将文本中的金融术语转换为标准缩写形式。
            只转换金融相关的术语，保持其他内容不变。
            保持原文的格式和标点符号。
            不要添加任何解释性文字，只返回转换后的文本。"""),
            ("human", "{input}"),
        ])
        
        chain = prompt | llm | StrOutputParser()
        abbreviated_text = chain.invoke({"input": text})
        
        logger.info(f"缩写创建完成: abbreviated_text={abbreviated_text}")
        
        return {
            "input": text,
            "abbreviated_text": abbreviated_text
        } 