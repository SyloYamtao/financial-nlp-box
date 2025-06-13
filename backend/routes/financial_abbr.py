from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from services.financial_abbr_service import FinancialAbbrService

router = APIRouter()
abbr_service = FinancialAbbrService()

class AbbrInput(BaseModel):
    text: str
    context: Optional[str] = ""
    method: str
    llmOptions: Dict[str, str]
    embeddingOptions: Optional[Dict[str, str]] = None

@router.post("/api/financial/abbr")
async def expand_abbreviations(input: AbbrInput):
    try:
        if input.method == "simple_ollama":
            return abbr_service.expand_abbreviations(input.text, input.llmOptions)
        elif input.method == "llm_rank_query_db":
            # 这里需要实现数据库查询和重排序的逻辑
            return abbr_service.expand_abbreviations(input.text, input.llmOptions)
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 