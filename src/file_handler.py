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
        
        # Sprawdzenie, czy kluczowe kolumny istnieją
        required_columns = ['produkt_sku', 'produkt_nazwa', 'zdjecie']
        if not all(col in df.columns for col in required_columns):
            print(f"❌ BŁĄD: Plik CSV musi zawierać kolumny: {required_columns}")
            return None
            
        print(f"✅ Pomyślnie wczytano {len(df)} wierszy.")
        return df
    except FileNotFoundError:
        print(f"❌ BŁĄD: Nie znaleziono pliku {csv_path}. Upewnij się, że plik istnieje.")
        return None
    except Exception as e:
        print(f"❌ BŁĄD podczas wczytywania pliku CSV: {e}")
        return None

def load_image_from_url(url: str) -> VertexImage | None:
    """Pobiera obraz z URL i konwertuje go do formatu VertexImage."""
    print(f"[ŁADOWANIE] Pobieranie obrazu z URL: {url[:80]}...")
    try:
        # Dodajemy User-Agent, aby uniknąć blokowania przez niektóre serwery
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()  # Sprawdza, czy zapytanie się powiodło
        return VertexImage.from_bytes(response.content)
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd podczas pobierania obrazu: {e}")
        return None
    except UnidentifiedImageError:
        print(f"❌ Błąd: Pobrane dane z URL nie są rozpoznawalnym formatem obrazu.")
        return None
