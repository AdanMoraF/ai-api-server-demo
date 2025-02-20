from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .schemas import PredictRequest, PredictResponse
import json


router = APIRouter()

@router.post("/model/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    pass

@router.get("/model")
def helloworld():
    return JSONResponse(content=jsonable_encoder({"hola"}))