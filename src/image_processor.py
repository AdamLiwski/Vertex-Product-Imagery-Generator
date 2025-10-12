# src/image_processor.py
import os
import time
import json
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel, Image as VertexImage
from google.api_core import exceptions as api_exceptions

def setup_vertex_ai_client(location: str, analysis_model_name: str, generation_model_name: str) -> dict:
    """Ładuje Project ID z .env i inicjalizuje OBA modele Vertex AI."""
    load_dotenv()
    project_id = os.getenv("GCLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GCLOUD_PROJECT_ID not found in the .env file.")

    try:
        vertexai.init(project=project_id, location=location)
        
        models = {
            "analysis": GenerativeModel(analysis_model_name),
            "generation": GenerativeModel(generation_model_name)
        }
        
        print(f"✅ Pomyślnie połączono z Vertex AI dla projektu: {project_id}")
        print(f"   -> Model Analityczny: {analysis_model_name}")
        print(f"   -> Model Generacyjny: {generation_model_name}")
        return models
    except Exception as e:
        raise ConnectionError(f"❌ ERROR Initializing Vertex AI: {e}")

def analyze_product_and_style(model, image_to_analyze, prompt):
    """Asks the AI to analyze the product and return a description and suggested style."""
    print("\n[ANALYSIS] Identifying product and suggesting style...")
    try:
        response = model.generate_content([image_to_analyze, prompt],
                                          generation_config={"response_mime_type": "application/json"})
        
        analysis_result = json.loads(response.text)
        print(f"✅ Analysis complete: Desc='{analysis_result['product_description']}', Style='{analysis_result['suggested_style']}'")
        return analysis_result
    except Exception as e:
        print(f"❌ Error during image analysis: {e}. Using default values.")
        return {"product_description": "product", "suggested_style": "commercial"}

def generate_and_save_image(model, prompt, initial_image, output_path, max_retries, wait_time):
    """
    Generuje obraz, obsługując błędy i limity, a następnie zapisuje wynik.
    ZMIANA: Ta wersja jest bardziej odporna i sprawdza, czy odpowiedź AI nie jest tekstem.
    """
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        print(f"\n[GENERATION] Attempt {attempt}/{max_retries} for: {os.path.basename(output_path)}...")
        print(f"  > Prompt: '{prompt[:80]}...'")

        try:
            response = model.generate_content([initial_image, prompt])
            
            # ZMIANA: Dodajemy solidną weryfikację odpowiedzi
            part = response.candidates[0].content.parts[0]

            # Krok 1: Sprawdź, czy model nie odpowiedział tekstem (co oznacza błąd)
            if hasattr(part, 'text') and part.text:
                print(f"⚠️ AI returned a text error instead of an image: '{part.text.strip()}'")
                print("   Retrying...")
                time.sleep(5)
                continue

            # Krok 2: Jeśli nie ma tekstu, spróbuj pobrać dane obrazu
            image_bytes = part.inline_data.data
            
            result_image_pil = Image.open(BytesIO(image_bytes))
            result_image_pil.save(output_path)

            print(f"✅ Successfully saved image to: {output_path}")
            return VertexImage.load_from_file(output_path)

        except api_exceptions.ResourceExhausted as e:
            print(f"⚠️ Quota limit reached. Waiting {wait_time}s...")
            time.sleep(wait_time)
            continue
        except (AttributeError, IndexError) as e:
             print(f"⚠️ Incorrect response structure from AI. Retrying... Details: {e}")
             time.sleep(5)
             continue
        except Exception as e:
            print(f"❌ Unexpected error on attempt {attempt}: {e}")
            # W przypadku błędu Pillow, nie próbujemy ponownie
            if isinstance(e, Image.UnidentifiedImageError):
                print("   This was an image identification error. Stopping retries for this task.")
                return None
            time.sleep(5)

    print(f"❌ Failed to generate image after {max_retries} attempts.")
    return None