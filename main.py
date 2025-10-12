# main.py
import os
import time
from src.config import * # Importuje teraz obie nazwy modeli
from src.file_handler import find_input_images, load_image_from_file
from src.image_processor import setup_vertex_ai_client, generate_and_save_image, analyze_product_and_style

def main():
    """Główna funkcja orkiestrująca uniwersalny proces generowania obrazów."""
    try:
        # ZMIANA: Inicjalizujemy oba modele
        models = setup_vertex_ai_client(GCP_LOCATION, ANALYSIS_MODEL_NAME, IMAGE_GENERATION_MODEL)
        analysis_model = models["analysis"]
        generation_model = models["generation"]
    except (ValueError, ConnectionError) as e:
        print(f"Błąd krytyczny: {e}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    images_to_process = find_input_images(INPUT_DIR)
    
    if not images_to_process:
        print(f"⚠️ Nie znaleziono obrazów w folderze '{INPUT_DIR}'.")
        return
        
    print(f"✅ Znaleziono {len(images_to_process)} obrazów do przetworzenia.")

    for source_image_path in images_to_process:
        base_filename = os.path.splitext(os.path.basename(source_image_path))[0]
        print(f"\n{'='*20} Rozpoczynam przetwarzanie: {base_filename} {'='*20}")

        source_image = load_image_from_file(source_image_path)
        if not source_image:
            continue

        # --- ETAP 1: Analiza produktu i stylu (używa modelu analitycznego) ---
        analysis = analyze_product_and_style(analysis_model, source_image, PROMPT_TEMPLATES["analysis"])
        
        print(f"\n[DELAY] Czekam {INTER_TASK_DELAY}s...")
        time.sleep(INTER_TASK_DELAY)

        # --- ETAP 2: Poprawa jakości (używa modelu generacyjnego) ---
        path_enhanced = os.path.join(OUTPUT_DIR, f"{base_filename}_enhanced.jpg")
        enhanced_image = generate_and_save_image(generation_model, PROMPT_TEMPLATES["enhancement"], source_image, path_enhanced, MAX_RETRIES, WAIT_TIME_SECONDS)
        if not enhanced_image: continue

        print(f"\n[DELAY] Czekam {INTER_TASK_DELAY}s...")
        time.sleep(INTER_TASK_DELAY)

        # --- ETAP 3: Studio z rekwizytami (używa modelu generacyjnego) ---
        prompt_studio = PROMPT_TEMPLATES["studio_with_props"].format(**analysis)
        path_studio = os.path.join(OUTPUT_DIR, f"{base_filename}_studio.jpg")
        generate_and_save_image(generation_model, prompt_studio, enhanced_image, path_studio, MAX_RETRIES, WAIT_TIME_SECONDS)
        
        print(f"\n[DELAY] Czekam {INTER_TASK_DELAY}s...")
        time.sleep(INTER_TASK_DELAY)

        # --- ETAP 4: Produkt w użyciu (używa modelu generacyjnego) ---
        prompt_in_use = PROMPT_TEMPLATES["lifestyle_in_use"].format(**analysis)
        path_in_use = os.path.join(OUTPUT_DIR, f"{base_filename}_lifestyle_1.jpg")
        generate_and_save_image(generation_model, prompt_in_use, enhanced_image, path_in_use, MAX_RETRIES, WAIT_TIME_SECONDS)
        
        print(f"\n[DELAY] Czekam {INTER_TASK_DELAY}s...")
        time.sleep(INTER_TASK_DELAY)
        
        # --- ETAP 5: Alternatywna aranżacja (używa modelu generacyjnego) ---
        prompt_alternative = PROMPT_TEMPLATES["lifestyle_alternative"].format(**analysis)
        path_alternative = os.path.join(OUTPUT_DIR, f"{base_filename}_lifestyle_2.jpg")
        generate_and_save_image(generation_model, prompt_alternative, enhanced_image, path_alternative, MAX_RETRIES, WAIT_TIME_SECONDS)

    print("\n\n🎉 ZAKOŃCZONO: Pomyślnie przetworzono wszystkie zadania.")

if __name__ == "__main__":
    main()