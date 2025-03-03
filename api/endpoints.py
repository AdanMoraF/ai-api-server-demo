import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .schemas import QuestionRequest, QuestionResponse
from .services import OllamaLangsmithModelService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

ollamaService = OllamaLangsmithModelService()

@router.post("/question", response_model=QuestionResponse)
async def predict(request: QuestionRequest):
    try:
        answer = ollamaService.ask_question(request.question)
        return QuestionResponse(**answer)
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
