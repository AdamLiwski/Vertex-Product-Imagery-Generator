# main.py
import os
import time
# POPRAWKA: Dodajemy brakujący import biblioteki pandas
import pandas as pd

from src.config import *
from src.file_handler import find_csv_files, load_data_from_csv, load_image_from_url
from src.image_processor import setup_vertex_ai_client, prepare_prompt, generate_image_with_reference

def process_csv_file(model, csv_path):
    """Przetwarza pojedynczy plik CSV, generując dla niego spójny zestaw obrazów."""
    
    df = load_data_from_csv(csv_path)
    if df is None: return

    # --- ETAP 0: Przygotowanie danych ---
    print("\n[PRZYGOTOWANIE] Filtrowanie i sortowanie balonów-cyfr (0-9)...")
    df_numbers = df[df['produkt_nazwa'].str.contains("Balon foliowy w kształcie cyfry", na=False)].copy()
    
    # Zabezpieczenie na wypadek, gdyby kolumna z cyfrą nazywała się inaczej
    if 'cyfry' in df.columns and pd.api.types.is_numeric_dtype(df_numbers['cyfry']):
        df_numbers['digit'] = df_numbers['cyfry'].astype(int)
    else:
        df_numbers['digit'] = df_numbers['produkt_nazwa'].str.extract(r'cyfry (\d)').astype(int)

    df_numbers = df_numbers.sort_values('digit').reset_index(drop=True)

    if len(df_numbers) < 1:
        print("⚠️ Nie znaleziono żadnych balonów-cyfr w tym pliku. Przechodzenie do następnego.")
        return
        
    # --- ETAP 1: Stworzenie obrazu referencyjnego ---
    print("\n[ETAP 1] Tworzenie obrazu referencyjnego dla spójności kolorów...")
    
    ref_product = df_numbers.iloc[0]
    ref_sku = str(ref_product['produkt_sku']).strip()
    ref_image_url = str(ref_product['zdjecie']).strip()
    ref_input_image = load_image_from_url(ref_image_url)
    
    if not ref_input_image:
        print("❌ Krytyczny błąd: Nie udało się pobrać obrazu referencyjnego. Pomijanie tego pliku.")
        return

    ref_prompt = "Ulepsz to zdjęcie produktu do perfekcyjnej jakości e-commerce. Umieść go na idealnie białym tle (#FFFFFF). Zwróć tylko obraz."
    ref_output_path = os.path.join(OUTPUT_DIR, f"{ref_sku}_0.png")
    
    reference_image_part = generate_image_with_reference(model, ref_prompt, ref_input_image, ref_input_image, ref_output_path, MAX_RETRIES, WAIT_TIME_SECONDS)

    if not reference_image_part:
        print("❌ Krytyczny błąd: Nie udało się stworzyć obrazu referencyjnego. Pomijanie tego pliku.")
        return

    # --- ETAP 2: Główna pętla generująca ---
    print(f"\n[ETAP 2] Rozpoczynanie generowania obrazów dla pliku {os.path.basename(csv_path)}...")

    for index, row in df_numbers.iterrows():
        sku = str(row['produkt_sku']).strip()
        product_name = str(row['produkt_nazwa']).strip()
        image_url = str(row['zdjecie']).strip()

        print(f"\n--- Przetwarzanie produktu: {product_name} (SKU: {sku}) ---")
        
        product_input_image = load_image_from_url(image_url)
        if not product_input_image:
            print("  -> ⚠️ Pominięto - nie udało się wczytać obrazu produktu.")
            continue

        for i, (template_key, template_text) in enumerate(PROMPT_TEMPLATES.items()):
            if index == 0 and i == 0:
                print(f"  -> Pominięto plik {sku}_0.png (już istnieje jako referencja).")
                continue

            output_filename = f"{sku}_{i}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            prompt = prepare_prompt(template_text, product_name, CHILDREN_KEYWORDS, ADULT_KEYWORDS)
            
            generate_image_with_reference(
                model=model, prompt=prompt, reference_image=reference_image_part,
                product_image=product_input_image, output_path=output_path,
                max_retries=MAX_RETRIES, wait_time=WAIT_TIME_SECONDS
            )
            time.sleep(5) 

def main():
    """Orkiestruje proces, znajdując wszystkie pliki CSV i przetwarzając każdy z nich."""
    
    model = setup_vertex_ai_client(GCP_LOCATION, IMAGE_MODEL_NAME)
    if not model: return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    csv_files = find_csv_files(CSV_INPUT_DIR)
    if not csv_files:
        print(f"⚠️ Nie znaleziono żadnych plików .csv w folderze '{CSV_INPUT_DIR}'.")
        return

    print(f"\n✅ Znaleziono {len(csv_files)} plików CSV do przetworzenia.")
    
    for csv_file in csv_files:
        print(f"\n{'='*20} Rozpoczynanie pracy z plikiem: {os.path.basename(csv_file)} {'='*20}")
        process_csv_file(model, csv_file)

    print(f"\n{'='*30} ZAKOŃCZONO WSZYSTKIE ZADANIA {'='*30}")

if __name__ == "__main__":
    main()

