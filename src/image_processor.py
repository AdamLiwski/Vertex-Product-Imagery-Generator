# src/image_processor.py
import os
import time
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel, Image as VertexImage
from google.api_core import exceptions as api_exceptions

def setup_vertex_ai_client(location: str, model_name: str):
    """Ładuje Project ID z .env i inicjalizuje klienta Vertex AI."""
    load_dotenv()
    project_id = os.getenv("GCLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Nie znaleziono GCLOUD_PROJECT_ID w pliku .env.")

    try:
        vertexai.init(project=project_id, location=location)
        model_instance = GenerativeModel(model_name)
        print(f"✅ Pomyślnie połączono z Vertex AI dla projektu: {project_id}")
        return model_instance
    except Exception as e:
        raise ConnectionError(f"❌ BŁĄD INICJALIZACJI Vertex AI: {e}")

def generate_and_save_image(model, prompt, initial_image, output_path, max_retries, wait_time):
    """Generuje obraz, obsługując błędy i limity, a następnie zapisuje wynik."""
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        print(f"\n[GENERACJA] Próba {attempt}/{max_retries} dla: {os.path.basename(output_path)}...")
        print(f"  > Prompt: '{prompt[:80]}...'")

        try:
            response = model.generate_content([initial_image, prompt])
            image_bytes = response.candidates[0].content.parts[0].inline_data.data
            
            result_image_pil = Image.open(BytesIO(image_bytes))
            result_image_pil.save(output_path)

            print(f"✅ Pomyślnie zapisano obraz w: {output_path}")
            return VertexImage.load_from_file(output_path)

        except api_exceptions.ResourceExhausted as e:
            print(f"⚠️ Limit quota przekroczony. Czekam {wait_time}s...")
            time.sleep(wait_time)
            continue
        except (AttributeError, IndexError):
             print(f"⚠️ Błędna struktura odpowiedzi od AI. Ponawiam próbę...")
             time.sleep(5)
             continue
        except Exception as e:
            print(f"❌ Nieoczekiwany błąd w próbie {attempt}: {e}")
            return None

    print(f"❌ Nie udało się wygenerować obrazu po {max_retries} próbach.")
    return None

def analyze_image_theme(model, image_to_analyze, prompt):
    """Prosi AI o zidentyfikowanie głównego motywu obrazu."""
    print("\n[ANALIZA] Rozpoznawanie motywu balonu...")
    try:
        response = model.generate_content([image_to_analyze, prompt])
        theme = response.text.strip()
        print(f"✅ Rozpoznany motyw: '{theme}'")
        return theme
    except Exception as e:
        print(f"❌ Błąd podczas analizy motywu: {e}")
        return "birthday party"