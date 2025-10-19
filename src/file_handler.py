# src/file_handler.py
import os
import pandas as pd
import requests
from vertexai.generative_models import Part

# NOWA FUNKCJA: Skanuje folder w poszukiwaniu plików .csv
def find_csv_files(input_dir: str) -> list[str]:
    """Skanuje folder wejściowy i zwraca listę ścieżek do plików .csv."""
    csv_paths = []
    if not os.path.isdir(input_dir):
        print(f"❌ BŁĄD: Folder wejściowy '{input_dir}' nie istnieje. Tworzenie folderu...")
        os.makedirs(input_dir)
        return []

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.csv'):
            csv_paths.append(os.path.join(input_dir, filename))
    
    return csv_paths

def load_data_from_csv(csv_path: str) -> pd.DataFrame | None:
    """Wczytuje dane z pliku CSV i zwraca je jako DataFrame pandas."""
    print(f"\n[ŁADOWANIE] Wczytywanie danych z pliku: {csv_path}...")
    try:
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8', on_bad_lines='warn')
        print(f"✅ Pomyślnie wczytano {len(df)} wierszy.")
        return df
    except FileNotFoundError:
        print(f"❌ BŁĄD: Plik '{csv_path}' nie został znaleziony.")
        return None
    except Exception as e:
        print(f"❌ BŁĄD podczas wczytywania pliku CSV: {e}")
        return None

def load_image_from_url(url: str) -> Part | None:
    """Pobiera obraz z URL i zwraca go jako obiekt Part dla API Gemini."""
    print(f"[ŁADOWANIE] Pobieranie obrazu z URL: {url}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '').lower()
        if 'image' not in content_type:
            print(f"  -> ⚠️ Ostrzeżenie: URL nie wskazuje na obraz (Content-Type: {content_type}). Pomijanie.")
            return None
        
        image_bytes = response.content
        
        mime_type = 'image/jpeg'
        if 'png' in content_type: mime_type = 'image/png'
        elif 'webp' in content_type: mime_type = 'image/webp'
        
        print("  -> ✅ Pomyślnie pobrano obraz.")
        return Part.from_data(data=image_bytes, mime_type=mime_type)

    except requests.exceptions.RequestException as e:
        print(f"  -> ❌ Błąd sieciowy podczas pobierania obrazu: {e}")
        return None
    except Exception as e:
        print(f"  -> ❌ Nieoczekiwany błąd podczas pobierania obrazu: {e}")
        return None

