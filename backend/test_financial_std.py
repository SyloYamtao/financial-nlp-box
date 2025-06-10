from services.financial_std_service import FinancialStdService
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_financial_std_service():
    """
    测试金融标准化服务的功能
    """
    try:
        # 初始化服务
        service = FinancialStdService(
            provider="huggingface",
            model="BAAI/bge-m3",
            db_path="db/financial_terms.db",
            collection_name="financial_concepts"
        )
        
        # 加载金融术语
        csv_path = os.path.join("data", "万条金融标准术语.csv")
        service.load_financial_terms(csv_path)
        
        # 测试搜索功能
        test_queries = [
            "股票",
            "债券",
            "期货",
            "期权",
            "基金"
        ]
        
        for query in test_queries:
            logger.info(f"\n搜索查询: {query}")
            results = service.search_financial_terms(query, limit=3)
            
            for i, result in enumerate(results, 1):
                logger.info(f"结果 {i}:")
                logger.info(f"  概念名称: {result['concept_name']}")
                logger.info(f"  概念代码: {result['concept_code']}")
                logger.info(f"  相似度: {1 - result['distance']:.4f}")
                logger.info("---")
                
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    test_financial_std_service() 