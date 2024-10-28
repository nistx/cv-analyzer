from fastapi import APIRouter, UploadFile, File, Form
from src.services.cv_processing_service import extract_text_from_cv
from src.services.gpt_service import get_cv_sections
from src.services.ranking_service import calculate_ranking
from src.core.config import constants
import uuid

router = APIRouter()

@router.post("/rank-cvs/")
async def rank_cvs_endpoint(cvs: list[UploadFile] = File(...), job_offer: str = Form(...)):
    results = []

    for cv in cvs:
        personal_data, clean_text = await extract_text_from_cv(cv)
        cv_sections = await get_cv_sections(clean_text, job_offer)

        cv_sections.personal_data.email = personal_data.email
        cv_sections.personal_data.phone = personal_data.phone

        ranking = calculate_ranking(cv_sections.skills)
        qualification_status = True if ranking >= constants.QUALIFIED_THRESHOLD else False
        candidate_id = str(uuid.uuid4())

        results.append({
            # "clean_text": clean_text,
            "id": candidate_id,
            **cv_sections.model_dump(),
            "ranking": ranking,
            "qualification_status": qualification_status
        })

    return {"job_description": job_offer, "cvs": results}