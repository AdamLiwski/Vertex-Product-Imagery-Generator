# main.py
import os
import time
import json
import pandas as pd

from src.config import (
    GCP_LOCATION, ANALYSIS_MODEL_NAME, IMAGE_MODEL_NAME, CSV_FILE_PATH,
    OUTPUT_DIR, PROMPT_TEMPLATES, MAX_RETRIES, WAIT_TIME_SECONDS
    # Usunięto importy KEYWORDS
)
from src.file_handler import load_data_from_csv, load_image_from_url
from src.image_processor import (
    setup_vertex_ai_client, run_product_analysis, generate_and_save_image
)

TEST_MODE = True

# --- USUNIĘTO FUNKCJĘ determine_audience ---
# Logika została przeniesiona bezpośrednio do modelu analitycznego AI

def apply_hard_rules(analysis_result: dict) -> dict:
    """Stosuje twarde reguły (fizyka) i przekazuje opis skali z AI."""
    rules = {"scale_description": "", "physics_info": "", "interaction_info": "", "quantity_info": ""}
    
    prod_type = analysis_result.get('product_type', '').lower()
    size_cm = analysis_result.get('detected_size_cm', 30)
    quantity = analysis_result.get('detected_quantity', 1)

    rules["quantity_info"] = f"Pokaż DOKŁADNIE JEDEN (1) produkt." if quantity == 1 else f"Pokaż zestaw składający się z DOKŁADNIE {quantity} sztuk produktu."
    
    # Pobieramy opis skali prosto z AI
    default_scale_desc = f"Produkt ma rozmiar {size_cm} cm."
    rules["scale_description"] = analysis_result.get('scale_description', default_scale_desc)

    # Reguły fizyki
    if 'balon foliowy' in prod_type and size_cm < 45:
        rules["physics_info"] = "Fizyka: Ten balon jest za mały, by unosić się na helu. Musi być pokazany na patyczku lub jako część leżącej dekoracji."
    elif 'balon lateksowy' in prod_type and size_cm < 26:
        rules["physics_info"] = "Fizyka: Ten balon jest za mały, by unosić się na helu. Musi być pokazany na patyczku lub jako część leżącej dekoracji."
    
    if 'świecz' in prod_type:
        rules["interaction_info"] = "Interakcja: Świeczki muszą być umieszczone na torcie urodzinowym."
    elif 'talerz' in prod_type or 'kubec' in prod_type or 'słomki' in prod_type:
        rules["interaction_info"] = "Interakcja: Produkt musi być częścią nakrycia stołu."

    return rules

def main():
    """Główna funkcja orkiestrująca proces generowania obrazów."""
    
    models = setup_vertex_ai_client(GCP_LOCATION, ANALYSIS_MODEL_NAME, IMAGE_MODEL_NAME)
    if not models: return

    df = load_data_from_csv(CSV_FILE_PATH)
    if df is None: return
        
    if TEST_MODE:
        print("⚠️ URUCHOMIONO W TRYBIE TESTOWYM: Przetwarzanie tylko pierwszego produktu.")
        df = df.head(1)

    for index, row in df.iterrows():
        sku = row.get('produkt_sku', f'produkt_{index}')
        product_name = row.get('produkt_nazwa', '')
        description = row.get('opis', '')
        image_url = row.get('zdjecie', '')

        print(f"\n{'='*25} Przetwarzanie produktu: {product_name} (SKU: {sku}) {'='*25}")

        if not all([sku, product_name, description, image_url]):
            print("⚠️ Pominięto wiersz - brakuje danych."); continue

        input_image = load_image_from_url(image_url)
        if not input_image: continue

        analysis_result = run_product_analysis(models["analysis"], input_image, product_name, description)
        if not analysis_result: continue
            
        print(f"✅ Wynik analizy AI: {analysis_result}")

        hard_rules = apply_hard_rules(analysis_result)
        
        # --- NOWA LOGIKA PRZYGOTOWANIA DANYCH DO PROMPTU ---
        # Pobieramy dane bezpośrednio z wyniku analizy AI
        suggested_theme = analysis_result.get('suggested_theme', 'impreza')
        suggested_audience = analysis_result.get('suggested_audience', 'ludzie') # Pobieramy nową daną
        
        prompt_data = {
            "suggested_theme": suggested_theme,
            "suggested_audience": suggested_audience, # Używamy nowej zmiennej
            **hard_rules
        }
        # --- KONIEC NOWEJ LOGIKI ---

        for i, (template_key, template_text) in enumerate(PROMPT_TEMPLATES.items()):
            final_prompt = template_text.format(**prompt_data)
            
            generation_content = [final_prompt, input_image]

            output_filename = f"{sku}_{i}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            generate_and_save_image(
                model=models["generation"],
                generation_content=generation_content,
                output_path=output_path,
                max_retries=MAX_RETRIES,
                wait_time=WAIT_TIME_SECONDS
            )
            time.sleep(2)

if __name__ == "__main__":
    main()

