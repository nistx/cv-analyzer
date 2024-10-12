import os, re
from fastapi import UploadFile
from pdfminer.high_level import extract_text
from tempfile import NamedTemporaryFile
from fastapi.concurrency import run_in_threadpool

personal_data_storage = {"emails": [], "phones": []}

def clean_text(text: str) -> str:
    special_chars_pattern = re.compile(r'[^\w\s@%_.,-]')
    newlines_pattern = re.compile(r'\s*\n\s*')
    multiple_spaces_pattern = re.compile(r'\s+')

    cleaned_text = special_chars_pattern.sub('', text)
    cleaned_text = newlines_pattern.sub(' ', cleaned_text)
    cleaned_text = multiple_spaces_pattern.sub(' ', cleaned_text)

    return cleaned_text.strip()

def extract_personal_data_and_remove(text: str) -> tuple:
    regex_email = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    regex_phone = r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{3,4}[-.\s]?){2,3}\d{3,4}\b'

    email = re.findall(regex_email, text)
    phone = re.findall(regex_phone, text)

    text_without_email = re.sub(regex_email, '', text)
    cleaned_text = re.sub(regex_phone, '', text_without_email)

    return {"emails": email, "phones": phone}, cleaned_text

def store_personal_data(personal_data: dict):
    personal_data_storage["emails"].extend(personal_data["emails"])
    personal_data_storage["phones"].extend(personal_data["phones"])

async def extract_text_from_cv(cv_file: UploadFile) -> str:
    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await cv_file.read())
            tmp_path = tmp.name

        raw_text = await run_in_threadpool(lambda: extract_text(tmp_path))
        cleaned_text = clean_text(raw_text)

        personal_data, cleaned_text_without_personal = extract_personal_data_and_remove(cleaned_text)

    except Exception as e:
        raise ValueError(f"Error al extraer texto del CV {cv_file.filename}: {str(e)}")

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    return cleaned_text_without_personal