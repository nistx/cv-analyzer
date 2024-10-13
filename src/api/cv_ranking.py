from fastapi import APIRouter, UploadFile, File, Form
from src.services.cv_processing_service import extract_text_from_cv
from src.services.gpt_service import get_skills_from_gpt4

router = APIRouter()


@router.post("/rank-cvs/")
async def rank_cvs_endpoint(cvs: list[UploadFile] = File(...), job_offer: str = Form(...)):
    results = []

    for cv in cvs:
        clean_text = await extract_text_from_cv(cv)
        skills = await get_skills_from_gpt4(clean_text, job_offer)

        results.append({
            "cv_name": cv.filename,
            "clean_text": clean_text,
            **skills.model_dump()
        })

    return {"job_description": job_offer, "cvs": results}