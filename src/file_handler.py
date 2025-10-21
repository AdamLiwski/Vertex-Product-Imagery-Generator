# src/file_handler.py
import os
import pandas as pd
import requests
from vertexai.generative_models import Image as VertexImage
from PIL import UnidentifiedImageError

def load_data_from_csv(csv_path: str) -> pd.DataFrame | None:
    """Wczytuje dane z pliku CSV i zwraca je jako DataFrame."""
    print(f"\n[ŁADOWANIE] Wczytywanie danych z pliku: {csv_path}...")
    try:
        df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')
        required_columns = ['produkt_sku', 'produkt_nazwa', 'opis', 'zdjecie']
        if not all(col in df.columns for col in required_columns):
            print(f"❌ BŁĄD: Plik CSV musi zawierać kolumny: {required_columns}")
            return None
        print(f"✅ Pomyślnie wczytano {len(df)} wierszy.")
        return df
    except FileNotFoundError:
        print(f"❌ BŁĄD: Nie znaleziono pliku {csv_path}.")
        return None
    except Exception as e:
        print(f"❌ BŁĄD podczas wczytywania pliku CSV: {e}")
        return None

def load_image_from_url(url: str) -> VertexImage | None:
    """Pobiera obraz z URL i konwertuje go do formatu VertexImage."""
    print(f"[ŁADOWANIE] Pobieranie obrazu z URL: {url[:80]}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()
        return VertexImage.from_bytes(response.content)
    except (requests.exceptions.RequestException, UnidentifiedImageError, Exception) as e:
        print(f"❌ BŁĄD podczas pobierania obrazu z URL: {e}")
        return None

# NOWOŚĆ: Funkcja do wczytywania lokalnego obrazu
def load_image_from_file(path: str) -> VertexImage | None:
    """Wczytuje obraz z lokalnej ścieżki."""
    print(f"[ŁADOWANIE] Wczytywanie lokalnego obrazu wzorcowego: {path}...")
    try:
        return VertexImage.load_from_file(path)
    except (FileNotFoundError, UnidentifiedImageError, Exception) as e:
        print(f"❌ KRYTYCZNY BŁĄD: Nie można wczytać obrazu wzorcowego '{path}': {e}")
        return None

