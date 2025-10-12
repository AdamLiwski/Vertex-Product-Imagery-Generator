import os
import re
import base64
import time
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv

# Google Cloud Vertex AI
import vertexai
from vertexai.generative_models import GenerativeModel, Image as VertexImage
from google.api_core import exceptions as api_exceptions

# --- Stałe Konfiguracyjne ---
# ZMIANA #1: Używamy szybszego modelu, który ma lepszy domyślny limit (2 RPM)
IMAGE_GENERATION_MODEL = "gemini-2.5-flash-image" 
GCP_LOCATION = "us-central1" # Lokalizacja dla Vertex AI
MAX_RETRIES = 5
WAIT_TIME_SECONDS = 30 # Skracamy czas oczekiwania po błędzie Quota, bo używamy własnych delayów
INTER_TASK_DELAY = 10 # NOWOŚĆ: Opóźnienie (w sekundach) pomiędzy zadaniami generacji
INPUT_DIR = "zdjecia_do_przerobienia"
OUTPUT_DIR = "gotowe"
IMAGE_FILENAME = "BAF485800_0.png" # Pamiętaj, żeby upewnić się, że to jest .png lub .jpg!


def setup_vertex_ai_client():
    """
    Ładuje Project ID z pliku .env i inicjalizuje klienta Vertex AI.
    """
    load_dotenv()
    project_id = os.getenv("GCLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Nie znaleziono GCLOUD_PROJECT_ID. Upewnij się, że plik .env istnieje i zawiera zmienną GCLOUD_PROJECT_ID.")

    try:
        vertexai.init(project=project_id, location=GCP_LOCATION)
        model_instance = GenerativeModel(IMAGE_GENERATION_MODEL)
        
        print(f"✅ Pomyślnie połączono z Vertex AI dla projektu: {project_id}")
        print(f"🌐 Używany region: {GCP_LOCATION}")
        print(f"🤖 Używany model: {IMAGE_GENERATION_MODEL}")
    except Exception as e:
        raise ConnectionError(f"❌ BŁĄD INICJALIZACJI Vertex AI. Sprawdź: 1. `gcloud auth application-default login` 2. Project ID. Szczegóły: {e}")

    return GenerativeModel(IMAGE_GENERATION_MODEL)


def load_image_from_file(file_path):
    """
    Wczytuje obraz z lokalnego pliku i zwraca go jako obiekt VertexImage.
    """
    print(f"\n[ŁADOWANIE] Wczytywanie obrazu z pliku: {file_path}...")
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku w ścieżce: {file_path}")
            
        return VertexImage.load_from_file(file_path)
    except (FileNotFoundError, UnidentifiedImageError, Exception) as e:
        print(f"❌ Błąd wczytywania obrazu: {type(e).__name__} - {e}")
        return None


def generate_and_save_image(model, prompt, initial_image, output_path):
    """
    Generuje obraz, obsługując błędy, w tym błąd limitu (quota), i zapisuje wynik.
    Obsługuje nową strukturę odpowiedzi dla modeli Gemini 2.5 Flash.
    """
    attempt = 0
    while attempt < MAX_RETRIES:
        attempt += 1
        print(f"\n[GENERACJA] Przetwarzanie (próba {attempt}/{MAX_RETRIES}) dla: {os.path.basename(output_path)}...")
        print(f"  > Prompt: '{prompt}'")

        try:
            response = model.generate_content([initial_image, prompt])

            # 🔍 Obsługa różnych formatów odpowiedzi
            image_bytes = None

            # Gemini 2.5 Flash — inline_data
            try:
                image_bytes = response.candidates[0].content.parts[0].inline_data.data
            except AttributeError:
                pass

            # Imagen fallback — generated_images
            if not image_bytes:
                try:
                    image_bytes = response.generated_images[0].image.image_bytes
                except AttributeError:
                    pass

            if not image_bytes:
                print(f"⚠️ Brak danych obrazu w odpowiedzi. Próba {attempt}.")
                time.sleep(5)
                continue

            result_image_pil = Image.open(BytesIO(image_bytes))
            result_image_pil.save(output_path)

            print(f"✅ Pomyślnie zapisano obraz w: {output_path}")
            return VertexImage.load_from_file(output_path)

        except api_exceptions.ResourceExhausted as e:
            error_msg = e.message.lower()
            if "base model" in error_msg:
                print("\n" + "="*80)
                print("❌ KRYTYCZNY BŁĄD LIMITU: Przekroczony stały limit Quota na poziomie konta/projektu.")
                print("   >>> JEDYNYM TRWAŁYM ROZWIĄZANIEM jest złożenie wniosku o zwiększenie limitu. <<<")
                print(f"   Szczegóły: {e.message}")
                print("="*80 + "\n")
                return None

            print(f"⚠️ Limit quota przekroczony. Czekam {WAIT_TIME_SECONDS} sekund i ponawiam próbę...")
            print(f"   Szczegóły błędu: {e.message}")
            time.sleep(WAIT_TIME_SECONDS)
            continue

        except Exception as e:
            print(f"❌ Wystąpił nieoczekiwany błąd w próbie {attempt}: {type(e).__name__} - {e}")
            return None

    print(f"❌ Nie udało się wygenerować obrazu '{os.path.basename(output_path)}' po maksymalnej liczbie prób.")
    return None




def main():
    """
    Główna funkcja orkiestrująca proces modyfikacji zdjęć.
    """
    # 1. Konfiguracja
    try:
        model = setup_vertex_ai_client()
    except (ValueError, ConnectionError) as e:
        print(f"Błąd krytyczny: {e}")
        return

    # 2. Przygotowanie folderów
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    # 3. Weryfikacja pliku
    source_image_path = os.path.join(INPUT_DIR, IMAGE_FILENAME)
    if not os.path.exists(source_image_path):
        print("\n" + "="*80)
        print(f"🚨 BŁĄD: Plik obrazu nie istnieje w lokalizacji: {source_image_path}")
        print(f"   Włóż plik '{IMAGE_FILENAME}' do folderu '{INPUT_DIR}' i spróbuj ponownie.")
        print("="*80 + "\n")
        return
    
    # 4. Parsowanie SKU
    # Używamy regex, aby dopasować .png lub .jpg
    match = re.match(r'^(.*?)_0\.(jpg|jpeg|png)$', IMAGE_FILENAME, re.IGNORECASE)
    if not match:
        print(f"❌ Nie udało się wyodrębnić SKU z nazwy pliku: {IMAGE_FILENAME}")
        return
    sku = match.group(1)
    print(f"\n[INFO] Zaczynam przetwarzanie dla SKU: {sku}")

    # 5. Wczytanie obrazu źródłowego
    source_image = load_image_from_file(source_image_path)
    if not source_image:
        return

    # ------------------- ZADANIE 1: Poprawa Jakości i Białe Tło -------------------
    prompt_1 = (
        "Popraw to zdjęcie produktowe. Wzmocnij kolory, popraw cienie, aby produkt wyglądał atrakcyjniej. "
        "Ważne: zachowaj oryginalny, niezmieniony kształt produktu. "
        "Umieść finalny produkt na idealnie białym tle (#FFFFFF), zgodnie ze standardami dla sklepów internetowych."
        "**Zwróć wynik jako obraz. Nie odpowiadaj tekstem.**"
    )
    # Zmieniamy rozszerzenie wyjściowe na .jpg (częstsze w e-commerce)
    path_1 = os.path.join(OUTPUT_DIR, f"{sku}_0.jpg")
    improved_image_vertex = generate_and_save_image(model, prompt_1, source_image, path_1)

    if not improved_image_vertex:
        print("❌ Nie udało się wygenerować pierwszego obrazu. Dalsze przetwarzanie zostało zatrzymane.")
        return

    # ------------------- DELAY 1: Oczekiwanie na kolejny interwał Quota (1 minuta) -------------------
    print(f"\n[DELAY] Osiągnięto limit 1/3 zadań. Czekam {INTER_TASK_DELAY} sekund, aby uniknąć limitu Quota...")
    time.sleep(INTER_TASK_DELAY)


    # ------------------- ZADANIE 2: Scena Lifestylowa 1 - Dziecko Zza Balonu -------------------
    prompt_2 = (
    "Na podstawie tego poprawionego zdjęcia balonu, stwórz nową scenę. "
    "Dodaj uśmiechnięte dziecko (w wieku 4–6 lat), które trzyma balon obiema rękami i wychyla się zza niego. "
    "Upewnij się, że dziecko jest widoczne w całości — z nogami, stopami i naturalną postawą. "
    "Zachowaj oryginalny, niezmieniony kształt balonu. "
    "Całość umieść na idealnie białym tle (#FFFFFF), zgodnie ze standardami zdjęć produktowych. "
    "Zwróć wynik jako obraz. Nie odpowiadaj tekstem."
)
    path_2 = os.path.join(OUTPUT_DIR, f"{sku}_1.jpg")
    image_2 = generate_and_save_image(model, prompt_2, improved_image_vertex, path_2)
    
    if not image_2:
        print("❌ Nie udało się wygenerować drugiego obrazu. Dalsze przetwarzanie zostało zatrzymane.")
        return


    # ------------------- DELAY 2: Oczekiwanie na kolejny interwał Quota (1 minuta) -------------------
    print(f"\n[DELAY] Osiągnięto limit 2/3 zadań. Czekam {INTER_TASK_DELAY} sekund, aby uniknąć limitu Quota...")
    time.sleep(INTER_TASK_DELAY)


    # ------------------- ZADANIE 3: Scena Lifestylowa 2 - Aranżacja Urodzinowa -------------------
    prompt_3 = (
        "Na podstawie tego poprawionego zdjęcia balonu, stwórz piękną, lifestylową aranżację. "
        "Balon powinien być napełniony helem. Uśmiechnięte dziecko trzyma go na wstążce. "
        "Ważne: zachowaj oryginalny, niezmieniony kształt balonu. "
        "Tło powinno być jasne, estetyczne i pasujące do motywu urodzinowego, "
        "na przykład w pokoju dziecięcym podczas przyjęcia."
    )
    path_3 = os.path.join(OUTPUT_DIR, f"{sku}_2.jpg")
    generate_and_save_image(model, prompt_3, improved_image_vertex, path_3)

    print("\n\n🎉 ZAKOŃCZONO: Pomyślnie przetworzono wszystkie zadania dla SKU:", sku)


if __name__ == "__main__":
    main()