from pydantic import BaseModel
from typing import List, Optional, Literal

class PersonalData(BaseModel):
    email: str
    phone: str

class PersonalDataForAPI(BaseModel):
    name: str
    role: str
    email: str
    phone: str

class Experience(BaseModel):
    company: Optional[str]
    position: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]

class Education(BaseModel):
    institution: str
    degree: str
    start_date: Optional[str]
    graduation_date: Optional[str]
    achievements: Optional[str]

class Skill(BaseModel):
    type: Literal["technical", "soft"]
    name: str
    score: int

class Certification(BaseModel):
    certification: str
    date_obtained: Optional[str]

class Language(BaseModel):
    language: str
    proficiency: Optional[str]

class Project(BaseModel):
    name: str
    description: Optional[str]

class Volunteering(BaseModel):
    organization: Optional[str]
    role: Optional[str]
    description: Optional[str]

class CVSections(BaseModel):
    personal_data: PersonalDataForAPI
    profile_summary: Optional[str]
    experience: Optional[List[Experience]]
    education: List[Education]
    skills: List[Skill]
    certifications: Optional[List[Certification]]
    languages: List[Language]
    projects: Optional[List[Project]]
    volunteering: Optional[List[Volunteering]]