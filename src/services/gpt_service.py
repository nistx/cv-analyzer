from src.core.openai_client import get_openai_client
from src.models.schemas import CVSections

GPT_MODEL = "gpt-4o-2024-08-06"

async def get_cv_sections(cv_text: str, job_description: str) -> CVSections:
    prompt = f"""    
    1. Identifica las secciones clave del CV en español.    
    2. Evalúa las habilidades en función de la oferta de trabajo y asigna puntajes positivos y negativos según los criterios de abajo.
    2.1. Habilidades Técnicas:
        2.1.1. Relevante: Puntaje de +7 a +10.
        2.1.2. Complementaria: Puntaje de +3 a +6.
        2.1.3. No Relevante: Puntaje de 0.
    2.2. Habilidades Blandas:
        2.2.1. Relevante: Puntaje de +1 a +3.
        2.2.2. Complementaria: Puntaje de +1.
        2.2.3. No Relevante: Puntaje de 0.
    2.3. Ausencia de Habilidades (Falta de Requisitos):
        2.3.1. Críticas: Puntaje negativo -10.
        2.3.2. Deseadas: Puntaje negativo -4.
    3.Formato de fechas: Utiliza MM/AAAA.
    4.Genera una justificación general basada en el ajuste del candidato con la oferta de trabajo
    
    Referencia:
    CV: {cv_text}
    Oferta de Trabajo: {job_description}
    """

    client = get_openai_client()

    try:
        response = client.beta.chat.completions.parse(
            model= GPT_MODEL,
            messages=[
                {"role": "system", "content": "Eres un experto en análisis de currículums, habilidades y reclutamiento."},
                {"role": "user", "content": prompt}
            ],
            response_format = CVSections
        )

        result = response.choices[0].message.parsed

        if not result:
            raise ValueError("GPT-4 did not return any response")

        return result

    except Exception as e:
        raise ValueError(f"Error calling the OpenAI API: {str(e)}")