# src/image_processor.py
import time
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os

import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image as VertexImage
from google.api_core import exceptions as api_exceptions

# Importujemy słowa kluczowe z naszej konfiguracji
from src.config import KIDS_KEYWORDS, ADULT_KEYWORDS

def setup_vertex_ai_client(location: str, model_name: str) -> GenerativeModel | None:
    """
    Inicjalizuje klienta Vertex AI i zwraca instancję JEDNEGO modelu do generowania obrazów.
    """
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

def prepare_prompt(template_text: str, product_name: str) -> str:
    """
    Przygotowuje finalny prompt, dynamicznie uzupełniając go o kontekst (dzieci/dorośli),
    jeśli szablon tego wymaga.
    """
    # Sprawdzamy, czy szablon zawiera zmienne do dynamicznego wypełnienia
    if '{audience}' in template_text or '{style}' in template_text:
        product_name_lower = product_name.lower()
        
        # Domyślny kontekst
        audience = "grupa radosnych, zróżnicowanych wiekowo ludzi"
        style = "nowoczesnego, jasnego przyjęcia w domu"

        # Sprawdzenie, czy to produkt dla dzieci
        if any(keyword in product_name_lower for keyword in KIDS_KEYWORDS):
            audience = "grupa szczęśliwych dzieci w różnym wieku"
            style = "kolorowego, radosnego przyjęcia urodzinowego dla dziecka"
        # Sprawdzenie, czy to produkt dla dorosłych
        elif any(keyword in product_name_lower for keyword in ADULT_KEYWORDS):
            audience = "grupa młodych dorosłych bawiących się na stylowej imprezie"
            style = "eleganckiego, wieczornego przyjęcia (np. Sylwester, 18. urodziny)"

        return template_text.format(
            product_name=product_name,
            audience=audience,
            style=style
        )
    else:
        # Jeśli szablon nie ma dynamicznych pól, po prostu wstawiamy nazwę produktu
        return template_text.format(product_name=product_name)


def generate_and_save_image(model: GenerativeModel, prompt: str, input_image: VertexImage, output_path: str, max_retries: int, wait_time: int):
    """Generuje obraz na podstawie promptu i obrazu wejściowego, a następnie zapisuje go na dysku."""
    if not input_image:
        print(f"⚠️ Pominięto generowanie dla {os.path.basename(output_path)} - brak obrazu wejściowego.")
        return

    print(f"\n[GENEROWANIE] Tworzenie obrazu: {os.path.basename(output_path)}...")
    print(f"   -> Fragment promptu: {prompt[:120]}...")

    generation_content = [input_image, prompt]
    
    # --- POPRAWKA: Usunęliśmy 'generation_config' ---
    # Nowy model nie akceptuje już parametru 'number_of_results'. Domyślnie generuje jeden obraz.

    for attempt in range(1, max_retries + 1):
        try:
            # --- POPRAWKA: Wywołujemy funkcję bez 'generation_config' ---
            response = model.generate_content(generation_content)
            
            # Sprawdzamy poprawność odpowiedzi
            if not response.candidates:
                 raise ValueError("Odpowiedź z API nie zawiera kandydatów.")
            
            image_bytes = response.candidates[0].content.parts[0].inline_data.data
            
            # Zapisujemy obraz
            pil_image = Image.open(BytesIO(image_bytes))
            pil_image.save(output_path)
            print(f"✅ Pomyślnie zapisano obraz: {output_path}")
            return

        except (api_exceptions.ResourceExhausted, api_exceptions.InternalServerError) as e:
            print(f"⚠️ Próba {attempt}/{max_retries}: Błąd po stronie API ({type(e).__name__}). Czekam {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"❌ Próba {attempt}/{max_retries}: Wystąpił nieoczekiwany błąd: {e}")
            time.sleep(5)

    print(f"❌ Nie udało się wygenerować obrazu {output_path} po {max_retries} próbach.")

