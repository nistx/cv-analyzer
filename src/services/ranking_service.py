import math

from src.models.schemas import SkillsExtraction


def calculate_ranking(skills: list[SkillsExtraction]) -> int:
    total_score = sum(skill.score for skill in skills)

    normalized_score = (total_score / 100) * 5

    normalized_score = max(normalized_score, 0)
    normalized_score = min(normalized_score, 5)

    rounded_score = math.floor(normalized_score) if normalized_score % 1 < 0.5 else math.ceil(normalized_score)

    return rounded_score