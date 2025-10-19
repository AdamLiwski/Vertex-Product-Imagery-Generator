# main.py
import os
import time
import pandas as pd

# Importujemy naszą zaktualizowaną konfigurację
from src.config import (
    GCP_LOCATION, IMAGE_MODEL_NAME, CSV_FILE_PATH,
    OUTPUT_DIR, PROMPT_TEMPLATES, MAX_RETRIES, WAIT_TIME_SECONDS
)
# Importujemy nasze zaktualizowane funkcje pomocnicze
from src.file_handler import load_data_from_csv, load_image_from_url
from src.image_processor import setup_vertex_ai_client, prepare_prompt, generate_and_save_image

# --- TRYB TESTOWY ---
# Ustaw na True, aby przetworzyć tylko pierwszy wiersz z pliku CSV
# Ustaw na False, aby przetworzyć cały plik
TEST_MODE = True

def main():
    """Główna funkcja orkiestrująca proces generowania ZESTAWU obrazów z pliku CSV."""
    
    # Inicjalizacja klienta Vertex AI dla modelu generującego obrazy
    model = setup_vertex_ai_client(GCP_LOCATION, IMAGE_MODEL_NAME)
    if not model:
        print("Zakończono program z powodu błędu inicjalizacji.")
        return

    # Wczytanie danych z pliku CSV
    df = load_data_from_csv(CSV_FILE_PATH)
    if df is None:
        print("Zakończono program z powodu błędu odczytu pliku CSV.")
        return

    # Utworzenie folderu wyjściowego, jeśli nie istnieje
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Decyzja, czy przetwarzamy cały plik, czy tylko próbkę
    if TEST_MODE:
        print("\n⚠️ URUCHOMIONO W TRYBIE TESTOWYM: Przetwarzanie tylko pierwszego produktu.")
        processing_df = df.head(1)
    else:
        print(f"\n🚀 URUCHOMIONO W TRYBIE PRODUKCYJNYM: Przetwarzanie {len(df)} produktów.")
        processing_df = df

    # Główna pętla przetwarzająca produkty
    for index, row in processing_df.iterrows():
        sku = str(row.get('produkt_sku', f'produkt_{index}')).strip()
        product_name = str(row.get('produkt_nazwa', 'Nieznany produkt')).strip()
        image_url = str(row.get('zdjecie', '')).strip()

        print(f"\n{'='*25} Przetwarzanie produktu: {product_name} (SKU: {sku}) {'='*25}")

        if not image_url:
            print("⚠️ Pominięto - brak adresu URL zdjęcia w pliku CSV.")
            continue
        
        # Pobranie obrazu wejściowego z URL (robimy to raz na produkt)
        input_image = load_image_from_url(image_url)
        if not input_image:
            print("⚠️ Pominięto cały produkt - nie udało się pobrać obrazu wejściowego.")
            continue

        # --- POPRAWKA: Używamy enumerate do numerowania plików wyjściowych ---
        for i, (template_key, template_text) in enumerate(PROMPT_TEMPLATES.items()):
            
            # 1. Przygotowanie unikalnego promptu dla danego typu zdjęcia
            prompt = prepare_prompt(template_text, product_name)
            
            # 2. Stworzenie unikalnej, numerowanej nazwy pliku wyjściowego
            output_filename = f"{sku}_{i}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            # 3. Wygenerowanie i zapisanie obrazu
            generate_and_save_image(
                model=model,
                prompt=prompt,
                input_image=input_image,
                output_path=output_path,
                max_retries=MAX_RETRIES,
                wait_time=WAIT_TIME_SECONDS
            )
            # Mała pauza, aby nie przeciążać API
            print("   -> Krótka pauza...")
            time.sleep(5) 
            
    print(f"\n{'='*30} ZAKOŃCZONO PRACĘ {'='*30}")

if __name__ == "__main__":
    main()

