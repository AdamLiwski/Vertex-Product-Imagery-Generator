# main.py
import os
import time

from src.config import *
from src.file_handler import load_data_from_csv, load_image_from_url
from src.image_processor import setup_vertex_ai_client, prepare_prompt, generate_image_with_reference

def main():
    """Orkiestruje proces generowania spójnego kolorystycznie zestawu 40 obrazów."""
    
    model = setup_vertex_ai_client(GCP_LOCATION, IMAGE_MODEL_NAME)
    if not model: return

    df = load_data_from_csv(CSV_FILE_PATH)
    if df is None: return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- ETAP 0: Przygotowanie danych ---
    print("\n[PRZYGOTOWANIE] Filtrowanie i sortowanie balonów-cyfr (0-9)...")
    df_numbers = df[df['produkt_nazwa'].str.contains("Balon foliowy w kształcie cyfry", na=False)].copy()
    df_numbers['digit'] = df_numbers['produkt_nazwa'].str.extract(r'cyfry (\d)').astype(int)
    df_numbers = df_numbers.sort_values('digit').reset_index(drop=True)

    if len(df_numbers) < 1:
        print("❌ Nie znaleziono żadnych balonów-cyfr w pliku CSV.")
        return
        
    # --- ETAP 1: Stworzenie obrazu referencyjnego ("Złotego Standardu") ---
    print("\n[ETAP 1] Tworzenie obrazu referencyjnego dla spójności kolorów...")
    
    ref_product = df_numbers.iloc[0]
    ref_image_url = str(ref_product['zdjecie']).strip()
    ref_input_image = load_image_from_url(ref_image_url)
    
    if not ref_input_image:
        print("❌ Krytyczny błąd: Nie udało się pobrać obrazu dla produktu referencyjnego. Przerwano.")
        return

    # Używamy prostego promptu do stworzenia czystego packshota, który będzie wzorcem
    ref_prompt = "Ulepsz to zdjęcie produktu do perfekcyjnej jakości e-commerce. Umieść go na idealnie białym tle (#FFFFFF). Zwróć tylko obraz."
    ref_output_path = os.path.join(OUTPUT_DIR, f"{str(ref_product['produkt_sku']).strip()}_packshot.png")
    
    # Generujemy obraz referencyjny (używając tej samej funkcji, ale przekazując ten sam obraz jako referencję i produkt)
    reference_image_part = generate_image_with_reference(model, ref_prompt, ref_input_image, ref_input_image, ref_output_path, MAX_RETRIES, WAIT_TIME_SECONDS)

    if not reference_image_part:
        print("❌ Krytyczny błąd: Nie udało się stworzyć obrazu referencyjnego. Przerwano.")
        return

    # --- ETAP 2: Główna pętla generująca wszystkie 40 obrazów ---
    print(f"\n[ETAP 2] Rozpoczynanie generowania {len(df_numbers) * len(PROMPT_TEMPLATES)} obrazów...")

    for index, row in df_numbers.iterrows():
        sku = str(row['produkt_sku']).strip()
        product_name = str(row['produkt_nazwa']).strip()
        image_url = str(row['zdjecie']).strip()

        print(f"\n--- Przetwarzanie produktu: {product_name} (SKU: {sku}) ---")
        
        product_input_image = load_image_from_url(image_url)
        if not product_input_image:
            print("  -> ⚠️ Pominięto - nie udało się wczytać obrazu produktu.")
            continue

        for template_key, template_text in PROMPT_TEMPLATES.items():
            # Jeśli przetwarzamy pierwszy produkt, jego packshot już stworzyliśmy jako referencję
            if index == 0 and template_key == 'packshot':
                print("  -> Pominięto 'packshot' dla produktu referencyjnego (już istnieje).")
                continue

            output_filename = f"{sku}_{template_key}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            prompt = prepare_prompt(template_text, product_name, CHILDREN_KEYWORDS, ADULT_KEYWORDS)
            
            generate_image_with_reference(
                model=model,
                prompt=prompt,
                reference_image=reference_image_part,
                product_image=product_input_image,
                output_path=output_path,
                max_retries=MAX_RETRIES,
                wait_time=WAIT_TIME_SECONDS
            )
            time.sleep(5) # Krótka pauza między zadaniami dla stabilności

    print(f"\n{'='*30} ZAKOŃCZONO PRACĘ {'='*30}")

if __name__ == "__main__":
    main()

