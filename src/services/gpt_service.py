from src.core.openai_client import get_openai_client
from src.models.schemas import FinalResponse

GPT_MODEL = "gpt-4o-2024-08-06"

async def get_skills_from_gpt4(cv_text: str, job_description: str) -> FinalResponse:
    prompt = f"""    
    A continuación te proporcionaré un CV y una oferta de trabajo. Quiero que realices lo siguiente:

    1. Extrae las habilidades técnicas y habilidades blandas solo del curriculum proporcionado.
    2. Asigna un puntaje a cada habilidad según el nivel de dominio mostrado en el curriculum:
        - Para las habilidades técnicas y blandas relevantes para la oferta de trabajo, asigna entre **8 y 10 puntos** según el nivel de experiencia del candidato.
        - Para habilidades complementarias que no se mencionan directamente en la oferta, pero que son útiles para el puesto, asigna entre **2 y 7 puntos** dependiendo de su relevancia y dominio.

    type: (soft | technical)
    name: (nombre de la habilidad)
    score: (puntaje asignado)

    Usa los siguientes textos de referencia:

    CV: {cv_text}
    Oferta de Trabajo: {job_description}
    """

    client = get_openai_client()

    try:
        response = client.beta.chat.completions.parse(
            model= GPT_MODEL,
            messages=[
                {"role": "system", "content": "Eres un experto en análisis de habilidades y reclutamiento."},
                {"role": "user", "content": prompt}
            ],
            response_format = FinalResponse
        )

        result = response.choices[0].message.parsed

        if not result:
            raise ValueError("GPT-4 did not return any response")

        return result

    except Exception as e:
        raise ValueError(f"Error calling the OpenAI API: {str(e)}")