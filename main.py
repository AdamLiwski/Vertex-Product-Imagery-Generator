# main.py
import os
import time
import json
import pandas as pd

from src.config import (
    GCP_LOCATION, ANALYSIS_MODEL_NAME, IMAGE_MODEL_NAME, CSV_FILE_PATH,
    OUTPUT_DIR, PROMPT_TEMPLATES, MAX_RETRIES, WAIT_TIME_SECONDS,
    KIDS_KEYWORDS, ADULT_KEYWORDS
)
from src.file_handler import load_data_from_csv, load_image_from_url
from src.image_processor import (
    setup_vertex_ai_client, run_product_analysis, generate_and_save_image
)

# --- TRYB TESTOWY ---
TEST_MODE = True

def determine_audience(product_name: str, suggested_theme: str) -> str:
    """Określa grupę docelową na podstawie słów kluczowych i sugestii AI."""
    name_lower = product_name.lower()
    theme_lower = suggested_theme.lower()
    
    if any(keyword in name_lower for keyword in ADULT_KEYWORDS) or any(keyword in theme_lower for keyword in ADULT_KEYWORDS):
        return "grupa dorosłych osób"
    
    if any(keyword in name_lower for keyword in KIDS_KEYWORDS):
        return "grupa dzieci"
        
    return "grupa bawiących się osób w różnym wieku"

def apply_hard_rules(analysis_result: dict) -> dict:
    """Stosuje twarde reguły i reaguje na dyrektywy z analizy AI."""
    rules = {
        "size_info": "",
        "physics_info": "",
        "interaction_info": "",
        "quantity_info": "",
        "realism_info": "" # Domyślnie puste
    }
    
    prod_type = analysis_result.get('product_type', '').lower()
    size_cm = analysis_result.get('detected_size_cm', 30)
    quantity = analysis_result.get('detected_quantity', 1)

    # 1. Reguła ilości
    if quantity == 1:
        rules["quantity_info"] = "Pokaż DOKŁADNIE JEDEN (1) produkt."
    else:
        rules["quantity_info"] = f"Pokaż zestaw składający się z około {quantity} sztuk produktu."

    # 2. Reguła rozmiaru
    rules["size_info"] = f"KRYTYCZNE: Produkt to {prod_type} o szacowanym rozmiarze {size_cm} cm."

    # 3. Reguły fizyki (Hel)
    if 'balon foliowy' in prod_type and size_cm < 45:
        rules["physics_info"] = "Fizyka: Ten balon jest za mały, by unosić się na helu. Musi być pokazany na patyczku lub jako część leżącej dekoracji."
    elif 'balon lateksowy' in prod_type and size_cm < 26:
        rules["physics_info"] = "Fizyka: Ten balon jest za mały, by unosić się na helu. Musi być pokazany na patyczku lub jako część leżącej dekoracji."
    elif 'balon' in prod_type:
        rules["physics_info"] = "Fizyka: Ten balon może unosić się na helu lub być wypełniony powietrzem."
        
    # 4. Reguły interakcji
    if 'świecz' in prod_type:
        rules["interaction_info"] = "Interakcja: Świeczki muszą być umieszczone na torcie urodzinowym."
    elif 'talerz' in prod_type or 'kubec' in prod_type or 'słomki' in prod_type:
        rules["interaction_info"] = "Interakcja: Produkt musi być częścią nakrycia stołu."
    elif 'balon' in prod_type:
        rules["interaction_info"] = "Interakcja: Produkt może być trzymany w ręku, być częścią bukietu balonowego lub dekoracji w tle."
    else:
        rules["interaction_info"] = "Interakcja: Pokaż produkt w naturalnym użyciu, zgodnie z jego przeznaczeniem."

    # 5. NOWA, WZMOCNIONA WERSJA: Wykonanie dyrektywy realizmu 3D od AI
    if analysis_result.get('needs_3d_realism') is True:
        print("   -> DYREKTYWA AI: Aktywowano regułę realizmu 3D dla balonu lateksowego.")
        rules["realism_info"] = (
            "NAKAZ REALIZMU 3D (NAJWYŻSZY PRIORYTET): Działaj jak artysta 3D. Obraz wejściowy to tylko PŁASKA TEKSTURA. "
            "Twoim zadaniem jest 'owinąć' tę teksturę wokół w pełni trójwymiarowego, fotorealistycznego, wirtualnego modelu NADMUCHANEGO balonu. "
            "MUSISZ dodać realistyczne oświetlenie, subtelne odbicia (specular highlights), miękkie cienie kontaktowe (contact shadows) i naturalne zagniecenia materiału. "
            "Finalny obiekt MUSI wyglądać jak prawdziwy, fizyczny balon sfotografowany w realnym świecie, a nie jak płaska grafika. "
        )
        
    return rules

def main():
    """Główna funkcja orkiestrująca dwuetapowy proces generowania obrazów."""
    
    models = setup_vertex_ai_client(GCP_LOCATION, ANALYSIS_MODEL_NAME, IMAGE_MODEL_NAME)
    if not models:
        return

    df = load_data_from_csv(CSV_FILE_PATH)
    if df is None:
        return
        
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
            print("⚠️ Pominięto wiersz - brakuje podstawowych danych.")
            continue

        input_image = load_image_from_url(image_url)
        if not input_image:
            continue

        analysis_result = run_product_analysis(models["analysis"], input_image, product_name, description)
        if not analysis_result:
            print("❌ Nie udało się przeprowadzić analizy produktu. Przechodzę do następnego.")
            continue
            
        print(f"✅ Wynik analizy AI: {analysis_result}")

        hard_rules = apply_hard_rules(analysis_result)
        audience = determine_audience(product_name, analysis_result.get('suggested_theme', ''))
        
        prompt_data = {
            "analysis_summary": json.dumps(analysis_result, ensure_ascii=False),
            "suggested_theme": analysis_result.get('suggested_theme', 'przyjęcie urodzinowe'),
            "audience": audience,
            **hard_rules
        }

        for i, (template_key, template_text) in enumerate(PROMPT_TEMPLATES.items()):
            final_prompt = template_text.format(**prompt_data)
            
            output_filename = f"{sku}_{i}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            generate_and_save_image(
                model=models["generation"],
                prompt=final_prompt,
                input_image=input_image,
                output_path=output_path,
                max_retries=MAX_RETRIES,
                wait_time=WAIT_TIME_SECONDS
            )
            print("   -> Krótka pauza...")
            time.sleep(2)

if __name__ == "__main__":
    main()

