from pymilvus import model
from pymilvus import MilvusClient
import pandas as pd
from tqdm import tqdm
import logging
from dotenv import load_dotenv
import os
import pathlib

load_dotenv()
import torch
from pymilvus import MilvusClient, DataType, FieldSchema, CollectionSchema

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化嵌入函数
embedding_function = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='/Users/zhangwufei/hf_model_path/BAAI/bge-m3',
    device='cuda:0' if torch.cuda.is_available() else 'cpu',
    trust_remote_code=True
)

# 文件路径
file_path = "../backend/data/万条金融标准术语_100.csv"
# 全数据文件路径
# file_path = "../backend/data/万条金融标准术语.csv"
db_path = "../backend/db/financial_terms_bge_m3.db"

# 确保数据库目录存在
db_dir = os.path.expanduser(os.path.dirname(db_path))
pathlib.Path(db_dir).mkdir(parents=True, exist_ok=True)

# 连接到 Milvus
client = MilvusClient(db_path)

collection_name = "financial_concepts"

# 加载数据
logging.info("Loading data from CSV")
df = pd.read_csv(file_path,
                 dtype=str,
                 low_memory=False,
                 ).fillna("NA")

# 获取向量维度（使用一个样本文档）
sample_doc = "Sample Text"
sample_embedding = embedding_function([sample_doc])[0]
vector_dim = len(sample_embedding)

# 构造Schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=vector_dim),
    FieldSchema(name="concept_id", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="concept_name", dtype=DataType.VARCHAR, max_length=200),
    FieldSchema(name="domain_id", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="vocabulary_id", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="concept_class_id", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="standard_concept", dtype=DataType.VARCHAR, max_length=1),
    FieldSchema(name="concept_code", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="input_file", dtype=DataType.VARCHAR, max_length=500),
]
schema = CollectionSchema(fields,
                          "Financial Terms Concepts",
                          enable_dynamic_field=True)

# 如果集合不存在，创建集合
if not client.has_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        schema=schema,
    )
    logging.info(f"Created new collection: {collection_name}")

# 创建索引
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="vector",
    index_type="AUTOINDEX",
    metric_type="COSINE",
    params={"nlist": 1024}
)

client.create_index(
    collection_name=collection_name,
    index_params=index_params
)

# 批量处理
batch_size = 1024

for start_idx in tqdm(range(0, len(df), batch_size), desc="Processing batches"):
    end_idx = min(start_idx + batch_size, len(df))
    batch_df = df.iloc[start_idx:end_idx]

    # 准备文档
    docs = []
    for _, row in batch_df.iterrows():
        # 金融术语只需要概念名称
        docs.append(row['A'])

    # 生成嵌入
    try:
        embeddings = embedding_function(docs)
        logging.info(f"Generated embeddings for batch {start_idx // batch_size + 1}")
    except Exception as e:
        logging.error(f"Error generating embeddings for batch {start_idx // batch_size + 1}: {e}")
        continue

    # 准备数据
    data = [
        {
            "vector": embeddings[idx],
            "concept_id": f"FT{idx + start_idx:06d}",  # 生成金融术语ID
            "concept_name": str(row['A']),  # 金融术语名称
            "domain_id": "Financial",  # 领域ID
            "vocabulary_id": "FINTERM",  # 词汇表ID
            "concept_class_id": "Financial Term",  # 概念类别
            "standard_concept": "S",  # 标准概念标记
            "concept_code": f"FT{idx + start_idx:06d}",  # 概念代码
            "input_file": file_path
        } for idx, (_, row) in enumerate(batch_df.iterrows())
    ]

    # 插入数据
    try:
        res = client.insert(
            collection_name=collection_name,
            data=data
        )
        logging.info(f"Inserted batch {start_idx // batch_size + 1}, result: {res}")
    except Exception as e:
        logging.error(f"Error inserting batch {start_idx // batch_size + 1}: {e}")

logging.info("Insert process completed.")

# 测试查询
test_queries = ["股票", "债券", "期货", "期权", "基金"]

for query in test_queries:
    query_embeddings = embedding_function([query])

    # 搜索余弦相似度最高的
    search_result = client.search(
        collection_name=collection_name,
        data=[query_embeddings[0].tolist()],
        limit=5,
        output_fields=["concept_name", "concept_class_id"]
    )
    logging.info(f"Search result for '{query}': {search_result}")

# 查询特定金融术语
query_result = client.query(
    collection_name=collection_name,
    filter="concept_name == '股票'",
    output_fields=["concept_name", "concept_class_id"],
    limit=5
)
logging.info(f"Query result for concept_name == '股票': {query_result}")
