from transformers import pipeline
import torch
import logging
from pymilvus import model
from pymilvus import MilvusClient
import os
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialNERService:
    """
    金融术语命名实体识别服务
    使用预训练模型和金融术语数据库进行金融文本的实体识别
    """
    def __init__(self):
        # 初始化 NER 模型，使用 GPU 如果可用
        self.pipe = pipeline("token-classification", 
                           model="dslim/bert-base-NER",
                           aggregation_strategy='simple',
                           device=0 if torch.cuda.is_available() else -1)
        
        # 初始化金融术语数据库
        load_dotenv()
        db_path = os.path.join(os.path.dirname(__file__), "../db/financial_terms_bge_m3.db")
        self.client = MilvusClient(db_path)
        
        # 初始化嵌入函数
        self.embedding_function = model.dense.SentenceTransformerEmbeddingFunction(
            model_name='/Users/zhangwufei/hf_model_path/BAAI/bge-m3',
            device='cuda:0' if torch.cuda.is_available() else 'cpu',
            trust_remote_code=True
        )
  
    def process(self, text, options, term_types):
        """
        处理输入文本，识别金融术语实体
        
        Args:
            text: 输入文本
            options: 处理选项
            term_types: 需要识别的术语类型
            
        Returns:
            包含识别出的实体和原始文本的字典
        """
        logger.info(f"开始处理文本: {text}")
        logger.info(f"选项: {options}")
        logger.info(f"术语类型: {term_types}")
        
        # 使用模型进行实体识别
        ner_result = self.pipe(text)
        logger.info(f"NER模型结果: {ner_result}")
        
        # 确保结果是实体列表
        if isinstance(ner_result, dict):
            ner_result = ner_result.get('entities', [])
            
        # 使用金融术语数据库进行匹配
        db_result = self._search_financial_terms(text)
        logger.info(f"数据库匹配结果: {db_result}")
        
        # 合并 NER 和数据库的结果
        combined_result = self._combine_results(ner_result, db_result, text)
        logger.info(f"合并后的结果: {combined_result}")
        
        # 合并相关实体
        combined_result = self._combine_entities(combined_result, text, options)
        logger.info(f"合并相关实体后的结果: {combined_result}")
        
        # 移除重叠实体
        non_overlapping_result = self._remove_overlapping_entities(combined_result)
        logger.info(f"移除重叠实体后的结果: {non_overlapping_result}")
        
        # 根据术语类型过滤实体
        filtered_result = self._filter_entities(non_overlapping_result, term_types)
        logger.info(f"最终过滤后的结果: {filtered_result}")
        
        return {
            "text": text,
            "entities": filtered_result
        }

    def _search_financial_terms(self, text):
        """
        在金融术语数据库中搜索匹配的术语
        """
        try:
            logger.info(f"开始搜索金融术语: {text}")
            
            # 生成文本的嵌入向量
            text_embedding = self.embedding_function([text])[0]
            logger.info("成功生成文本嵌入向量")
            
            # 在数据库中搜索相似术语
            search_result = self.client.search(
                collection_name="financial_concepts",
                data=[text_embedding.tolist()],
                limit=5,
                output_fields=["concept_name", "concept_class_id"]
            )
            logger.info(f"数据库搜索结果: {search_result}")
            
            # 将搜索结果转换为实体格式
            entities = []
            if search_result and len(search_result) > 0:
                for hit in search_result[0]:
                    # 检查 hit 是否为字典类型
                    if isinstance(hit, dict):
                        # 使用 distance 作为相似度分数
                        distance = hit.get('distance', 1.0)
                        # 对于完全匹配的情况，直接使用 1.0 作为分数
                        score = 1.0 if distance > 0.99 else (1.0 - distance)
                        entity_data = hit.get('entity', {})
                    else:
                        distance = getattr(hit, 'distance', 1.0)
                        score = 1.0 if distance > 0.99 else (1.0 - distance)
                        entity_data = getattr(hit, 'entity', {})
                    
                    logger.info(f"处理搜索结果: distance={distance}, score={score}, entity_data={entity_data}")
                    
                    # 使用较低的阈值
                    if score > 0.2:  # 降低阈值
                        concept_name = entity_data.get('concept_name', '')
                        if concept_name:
                            # 对于完全匹配的情况，直接使用整个文本作为实体
                            if distance > 0.99:
                                entity = {
                                    'entity_group': 'FINANCIAL_TERM',
                                    'word': text,
                                    'start': 0,
                                    'end': len(text),
                                    'score': 1.0
                                }
                                entities.append(entity)
                                logger.info(f"添加完全匹配实体: {entity}")
                            else:
                                start_pos = text.find(concept_name)
                                if start_pos != -1:  # 只在找到匹配时添加实体
                                    entity = {
                                        'entity_group': 'FINANCIAL_TERM',
                                        'word': concept_name,
                                        'start': start_pos,
                                        'end': start_pos + len(concept_name),
                                        'score': float(score)
                                    }
                                    entities.append(entity)
                                    logger.info(f"添加部分匹配实体: {entity}")
            
            logger.info(f"最终识别的实体列表: {entities}")
            return entities
        except Exception as e:
            logger.error(f"Error in financial terms search: {str(e)}")
            return []

    def _combine_results(self, ner_result, db_result, text):
        """
        合并 NER 和数据库的结果
        """
        combined = []
        
        # 添加 NER 结果
        for entity in ner_result:
            if isinstance(entity, dict):
                entity['score'] = float(entity.get('score', 0))
                combined.append(entity)
            
        # 添加数据库结果
        for entity in db_result:
            if isinstance(entity, dict):
                # 检查是否与现有实体重叠
                is_overlapping = False
                for existing in combined:
                    if (entity['start'] <= existing['end'] and entity['end'] >= existing['start']):
                        is_overlapping = True
                        break
                if not is_overlapping:
                    combined.append(entity)
                    
        return combined

    def _combine_entities(self, result, text, options):
        """
        合并相关的实体
        """
        combined_result = []
        i = 0
        while i < len(result):
            entity = result[i]
            entity['score'] = float(entity['score'])

            if options.get('combineFinancialTerms', False) and entity['entity_group'] in ['ORG', 'MISC']:
                # 检查并合并金融术语
                combined_entity = self._try_combine_with_financial_term(result, i, text)
                if combined_entity:
                    combined_result.append(combined_entity)
                    i += 1
                    continue
            combined_result.append(entity)
            i += 1
        return combined_result

    def _try_combine_with_financial_term(self, result, i, text):
        """
        尝试将当前实体与金融术语实体合并
        """
        # 检查前一个实体
        if i > 0 and result[i-1]['entity_group'] in ['ORG', 'MISC']:
            return self._create_combined_entity(result[i-1], result[i], text)
        # 检查后一个实体
        elif i < len(result) - 1 and result[i+1]['entity_group'] in ['ORG', 'MISC']:
            return self._create_combined_entity(result[i], result[i+1], text)
        return None

    def _create_combined_entity(self, entity1, entity2, text):
        """
        创建合并后的实体
        """
        start = min(entity1['start'], entity2['start'])
        end = max(entity1['end'], entity2['end'])
        word = text[start:end]
        return {
            'entity_group': 'FINANCIAL_TERM',
            'word': word,
            'start': start,
            'end': end,
            'score': (entity1['score'] + entity2['score']) / 2,
            'original_entities': [entity1, entity2]
        }

    def _remove_overlapping_entities(self, entities):
        """
        移除重叠的实体，保留得分最高的实体
        """
        # 按开始位置、结束位置（降序）和得分（降序）排序
        sorted_entities = sorted(entities, key=lambda x: (x['start'], -x['end'], -x['score']))
        non_overlapping = []
        last_end = -1

        i = 0
        while i < len(sorted_entities):
            current = sorted_entities[i]
            
            # 如果当前实体与之前的实体不重叠，直接添加
            if current['start'] >= last_end:
                non_overlapping.append(current)
                last_end = current['end']
                i += 1
            else:
                # 处理重叠实体
                same_span = [current]
                j = i + 1
                while j < len(sorted_entities) and sorted_entities[j]['start'] == current['start'] and sorted_entities[j]['end'] == current['end']:
                    same_span.append(sorted_entities[j])
                    j += 1
                
                # 选择得分最高的实体
                best_entity = max(same_span, key=lambda x: x['score'])
                if best_entity['end'] > last_end:
                    non_overlapping.append(best_entity)
                    last_end = best_entity['end']
                
                i = j

        return non_overlapping

    def _filter_entities(self, entities, term_types):
        """
        根据术语类型过滤实体
        """
        filtered_result = []
        for entity in entities:
            if term_types.get('allFinancialTerms', False):
                filtered_result.append(entity)
            elif (term_types.get('stock', False) and entity['entity_group'] == 'ORG') or \
                 (term_types.get('index', False) and entity['entity_group'] == 'MISC') or \
                 (term_types.get('financialTerm', False) and entity['entity_group'] == 'FINANCIAL_TERM'):
                filtered_result.append(entity)
        return filtered_result 