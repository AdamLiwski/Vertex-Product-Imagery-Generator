# src/image_processor.py
import os
import time
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.api_core import exceptions as api_exceptions

def setup_vertex_ai_client(location: str, model_name: str) -> GenerativeModel | None:
    """Inicjalizuje klienta Vertex AI."""
    load_dotenv()
    project_id = os.getenv("GCLOUD_PROJECT_ID")
    if not project_id:
        print("❌ BŁĄD: Zmienna GCLOUD_PROJECT_ID nie została znaleziona w pliku .env.")
        return None
    try:
        vertexai.init(project=project_id, location=location)
        model = GenerativeModel(model_name)
        print(f"✅ Pomyślnie połączono z Vertex AI (projekt: {project_id}, model: {model_name})")
        return model
    except Exception as e:
        print(f"❌ BŁĄD podczas inicjalizacji Vertex AI: {e}")
        return None

def prepare_prompt(template_text: str, product_name: str, children_kw: list, adult_kw: list) -> str:
    """Przygotowuje prompt, dynamicznie dobierając grupę docelową i styl imprezy."""
    audience = "grupa dorosłych osób"
    style = "eleganckiej imprezie dla dorosłych"

    # Sprawdzamy słowa kluczowe w nazwie produktu
    product_name_lower = product_name.lower()
    if any(keyword in product_name_lower for keyword in children_kw):
        audience = "grupa dzieci"
        style = "przyjęciu urodzinowym dla dziecka"
    elif any(keyword in product_name_lower for keyword in adult_kw):
        audience = "grupa młodych dorosłych"
        style = "hucznej imprezie, np. na 18-stkę"

    # Używamy try-except, aby uniknąć błędu, jeśli szablon nie ma wszystkich kluczy
    try:
        return template_text.format(product_name=product_name, style=style, audience=audience)
    except KeyError:
        return template_text.format(product_name=product_name)


# --- NOWA, KLUCZOWA FUNKCJA ---
def generate_image_with_reference(model: GenerativeModel, prompt: str, reference_image: Part, product_image: Part, output_path: str, max_retries: int, wait_time: int) -> Part | None:
    """
    Generuje obraz, używając obrazu referencyjnego do zachowania spójności.
    Zwraca obiekt 'Part' wygenerowanego obrazu, aby mógł stać się nową referencją.
    """
    
    # Tworzymy zawartość zapytania: prompt, obraz referencyjny, obraz główny
    generation_content = [prompt, reference_image, product_image]
    
    print(f"[GENEROWANIE] Tworzenie: {os.path.basename(output_path)}...")
    
    for attempt in range(1, max_retries + 1):
        try:
            response = model.generate_content(generation_content, generation_config={"response_modalities": ["IMAGE"]})
            
            # Sprawdzamy, czy odpowiedź jest poprawna
            if not response.candidates or not response.candidates[0].content.parts:
                raise ValueError("Odpowiedź z API jest pusta lub ma nieprawidłową strukturę.")
                
            image_part = response.candidates[0].content.parts[0]
            image_bytes = image_part.inline_data.data
            
            pil_image = Image.open(BytesIO(image_bytes))
            pil_image.save(output_path)
            
            print(f"  -> ✅ Pomyślnie zapisano: {output_path}")
            # Zwracamy obiekt obrazu, aby móc go użyć jako referencję w pierwszym etapie
            return image_part

        except (api_exceptions.ResourceExhausted, api_exceptions.InternalServerError, api_exceptions.ServiceUnavailable) as e:
            print(f"  -> ❌ Próba {attempt}/{max_retries}: Błąd po stronie API ({type(e).__name__}). Czekam {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"  -> ❌ Próba {attempt}/{max_retries}: Nieoczekiwany błąd: {e}")
            time.sleep(5)
            
    print(f"❌ Nie udało się wygenerować obrazu {output_path} po {max_retries} próbach.")
    return None

