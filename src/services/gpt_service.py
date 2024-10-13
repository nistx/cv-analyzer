from src.core.openai_client import get_openai_client
from src.models.schemas import FinalResponse

GPT_MODEL = "gpt-4o-2024-08-06"

async def get_skills_from_gpt4(cv_text: str, job_description: str) -> FinalResponse:
    prompt = f"""    
    Extrae las habilidades técnicas y blandas del CV. Evalúa cada habilidad según la relevancia para la oferta de trabajo, con un puntaje máximo de 100 puntos, distribuidos de la siguiente manera:

    1. Habilidades técnicas clave (máx. 70 puntos):
        - Alta relevancia (7-10 puntos): Si es una habilidad crítica y está bien desarrollada.
        - Baja relevancia (0-5 puntos): Si falta o es deficiente.
    
    2. Habilidades técnicas complementarias:
        - Relevantes (máx. 20 puntos): 6-8 puntos si se relacionan indirectamente con el puesto.
        - No relevantes (máx. 5 puntos): 1-5 puntos si no están directamente relacionadas pero son útiles.
    
    3. Habilidades blandas (máx. 5 puntos):
        - 1-5 puntos según su importancia en la oferta.
    
    Deducciones:
    Las deducciones se expresan con un puntaje negativo y deben incluir la habilidad faltante.
        - Falta de una habilidad técnica crítica, reduce 10-15 puntos.
        - Falta de una habilidad técnica deseada, reduce 2-5 puntos.
        - Falta de una habilidad blanda clave, reduce 1-3 puntos.
   
    type: (soft | technical)  
    name: (nombre de la habilidad)  
    score: (puntaje asignado)

    
    Referencia:
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