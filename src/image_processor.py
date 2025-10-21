# src/image_processor.py
import os
import time
import json
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image as VertexImage
from google.api_core import exceptions as api_exceptions

# Importujemy prompty z naszej konfiguracji
from src.config import ANALYSIS_PROMPT

def setup_vertex_ai_client(location: str, analysis_model_name: str, generation_model_name: str) -> dict | None:
    """Inicjalizuje klienta Vertex AI i zwraca słownik z OBA modelami."""
    load_dotenv()
    project_id = os.getenv("GCLOUD_PROJECT_ID")
    if not project_id:
        print("❌ BŁĄD: Zmienna GCLOUD_PROJECT_ID nie została znaleziona w pliku .env.")
        return None

    try:
        vertexai.init(project=project_id, location=location)
        models = {
            "analysis": GenerativeModel(analysis_model_name),
            "generation": GenerativeModel(generation_model_name)
        }
        print(f"✅ Pomyślnie połączono z Vertex AI (projekt: {project_id})")
        print(f"   -> Model Analityczny: {analysis_model_name}")
        print(f"   -> Model Generacyjny: {generation_model_name}")
        return models
    except Exception as e:
        print(f"❌ BŁĄD podczas inicjalizacji Vertex AI: {e}")
        return None

def run_product_analysis(model: GenerativeModel, image: VertexImage, product_name: str, description: str) -> dict | None:
    """Wysyła dane do modelu analitycznego i oczekuje odpowiedzi w formacie JSON."""
    print("\n[ANALIZA] Uruchamianie głębokiej analizy produktu...")
    
    content = [
        image,
        ANALYSIS_PROMPT,
        "\nDANE DO ANALIZY:",
        f"Nazwa produktu: {product_name}",
        f"Opis produktu: {description}"
    ]
    
    try:
        response = model.generate_content(content)
        response_text = response.text
        
        start_index = response_text.find('{')
        end_index = response_text.rfind('}') + 1
        
        if start_index != -1 and end_index != -1:
            json_str = response_text[start_index:end_index]
            analysis_json = json.loads(json_str)
            return analysis_json
        else:
            raise json.JSONDecodeError("Nie znaleziono obiektu JSON w odpowiedzi modelu.", response_text, 0)

    except json.JSONDecodeError as e:
        print("❌ BŁĄD ANALIZY: Model nie zwrócił poprawnego formatu JSON lub nie można go było wyodrębnić.")
        print(f"   -> Otrzymano: {response.text}")
        print(f"   -> Błąd parsera: {e}")
        return None
    except Exception as e:
        print(f"❌ BŁĄD podczas komunikacji z modelem analitycznym: {e}")
        return None

def generate_and_save_image(model: GenerativeModel, prompt: str, input_image: VertexImage, output_path: str, max_retries: int, wait_time: int):
    """Generuje obraz i zapisuje go, z ulepszoną obsługą błędów."""
    print(f"\n[GENEROWANIE] Tworzenie obrazu: {os.path.basename(output_path)}...")
    
    generation_content = [input_image, prompt]
    
    for attempt in range(1, max_retries + 1):
        try:
            response = model.generate_content(generation_content)
            
            if not response.candidates:
                 raise ValueError("Odpowiedź z API nie zawiera kandydatów.")
            
            image_bytes = response.candidates[0].content.parts[0].inline_data.data
            
            # --- POPRAWIONA LOGIKA ---
            # Krok 1: Spróbuj otworzyć obraz w pamięci. Jeśli się nie uda, to znaczy, że dane są uszkodzone.
            pil_image = Image.open(BytesIO(image_bytes))
            
            # Krok 2: Jeśli otwarcie się powiodło, zapisz plik.
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            pil_image.save(output_path)
            
            # Krok 3: Dopiero po pomyślnym zapisie poinformuj o sukcesie i zakończ funkcję.
            print(f"✅ Pomyślnie zapisano obraz: {output_path}")
            return

        except UnidentifiedImageError:
            print(f"❌ BŁĄD Próba {attempt}/{max_retries}: Otrzymano uszkodzone dane obrazu z API. Próbuję ponownie...")
            time.sleep(5)
        except (api_exceptions.ResourceExhausted, api_exceptions.InternalServerError) as e:
            print(f"⚠️ Próba {attempt}/{max_retries}: Błąd po stronie API ({type(e).__name__}). Czekam {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"❌ BŁĄD Próba {attempt}/{max_retries}: Nieoczekiwany błąd: {e}")
            time.sleep(5)
            
    print(f"❌ Nie udało się wygenerować obrazu {os.path.basename(output_path)} po {max_retries} próbach.")

