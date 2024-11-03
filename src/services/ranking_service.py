import math
from src.core.config import constants

from src.models.schemas import Skill


def calculate_ranking(skills: list[Skill]) -> int:
    total_score = sum(skill.score for skill in skills)

    normalized_score = (total_score / 100) * constants.RANKING_MAX

    normalized_score = max(normalized_score, constants.RANKING_MIN)
    normalized_score = min(normalized_score, constants.RANKING_MAX)

    rounded_score = math.floor(normalized_score) if normalized_score % constants.INTEGER_THRESHOLD < constants.ROUNDED_THRESHOLD else math.ceil(normalized_score)

    return rounded_score