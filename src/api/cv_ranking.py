from fastapi import APIRouter, UploadFile, File, Form
from src.services.cv_processing_service import extract_text_from_cv

router = APIRouter()


@router.post("/rank-cvs/")
async def rank_cvs_endpoint(cvs: list[UploadFile] = File(...), job_offer: str = Form(...)):
    results = []

    for cv in cvs:
        cv_text = await extract_text_from_cv(cv)
        results.append({cv.filename: cv_text})

    return {"job_description": job_offer, "cvs": results}