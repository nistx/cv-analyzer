from pydantic import BaseModel

class SkillsExtraction(BaseModel):
    type: str
    name: str
    score: int

class FinalResponse(BaseModel):
    skills: list[SkillsExtraction]