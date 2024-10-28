from src.core.openai_client import get_openai_client
from src.models.schemas import CVSections

GPT_MODEL = "gpt-4o-2024-08-06"

async def get_cv_sections(cv_text: str, job_description: str) -> CVSections:
    prompt = f"""    
    A continuación te proporcionaré un CV y una oferta de trabajo. Realiza el siguiente análisis:
    1. Identifica las secciones clave del CV en español.
    2. Evalua y asigna un puntaje a las Habilidades (máx 100 puntos):
    2.1. Habilidades Técnicas:
        2.1.1. Relevancia: Califica cada habilidad técnica del candidato como relevante (7-10 puntos), complementaria (6-8 puntos) o no relevante (0-5 puntos) en relación a los requisitos de la oferta de trabajo.
        2.1.2. Críticas: Si alguna habilidad técnica crítica no está presente en el CV, asigna -10 puntos.
        2.1.3. Deseadas: Si alguna habilidad técnica deseada no está presente, asigna un puntaje negativo entre -2 y -5 puntos, dependiendo de su importancia.
    2.2. Habilidades Blandas: Asigna un puntaje entre 1 y 5 puntos a las habilidades blandas del candidato, considerando su relevancia para el puesto.
    2.3. Falta de Habilidades: Si identificas alguna habilidad blanda clave que debería estar presente y no lo está, asigna un puntaje negativo entre -1 y -3 puntos.
    3. Formato de Fechas: Utiliza el formato MM/AAAA.
    
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