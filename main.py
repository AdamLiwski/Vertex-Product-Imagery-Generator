# main.py
import os
import re
import time
from src.config import *
from src.file_handler import find_input_images, load_image_from_file
from src.image_processor import setup_vertex_ai_client, generate_and_save_image, analyze_image_theme

def main():
    """Główna funkcja orkiestrująca proces."""
    try:
        model = setup_vertex_ai_client(GCP_LOCATION, IMAGE_GENERATION_MODEL)
    except (ValueError, ConnectionError) as e:
        print(f"Błąd krytyczny: {e}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    images_to_process = find_input_images(INPUT_DIR)
    if not images_to_process:
        print(f"⚠️ Nie znaleziono obrazów w folderze '{INPUT_DIR}'. Umieść tam pliki i spróbuj ponownie.")
        return
        
    print(f"✅ Znaleziono {len(images_to_process)} obrazów do przetworzenia.")

    for source_image_path in images_to_process:
        image_filename = os.path.basename(source_image_path)
        print(f"\n{'='*20} Rozpoczynam przetwarzanie pliku: {image_filename} {'='*20}")
        
        # ZMIANA: Bardziej elastyczny regex, który nie wymaga "_0"
        match = re.match(r'^(.*?)(_0)?\.(jpg|jpeg|png)$', image_filename, re.IGNORECASE)
        sku = match.group(1) if match else os.path.splitext(image_filename)[0]
        print(f"[INFO] Przetwarzanie dla SKU: {sku}")

        source_image = load_image_from_file(source_image_path)
        if not source_image:
            continue

        # --- ZADANIE 1: Poprawa Jakości i Białe Tło ---
        path_1 = os.path.join(OUTPUT_DIR, f"{sku}_0.jpg")
        improved_image = generate_and_save_image(model, PROMPTS["step_1_studio"], source_image, path_1, MAX_RETRIES, WAIT_TIME_SECONDS)
        if not improved_image: continue

        print(f"\n[DELAY] Czekam {INTER_TASK_DELAY}s...")
        time.sleep(INTER_TASK_DELAY)

        # --- ZADANIE 2: Dziecko z Balonem ---
        path_2 = os.path.join(OUTPUT_DIR, f"{sku}_1.jpg")
        generate_and_save_image(model, PROMPTS["step_2_lifestyle_child"], improved_image, path_2, MAX_RETRIES, WAIT_TIME_SECONDS)

        print(f"\n[DELAY] Czekam {INTER_TASK_DELAY}s...")
        time.sleep(INTER_TASK_DELAY)

        # --- ZADANIE 3: Aranżacja Urodzinowa ---
        path_3 = os.path.join(OUTPUT_DIR, f"{sku}_2.jpg")
        generate_and_save_image(model, PROMPTS["step_3_lifestyle_party"], improved_image, path_3, MAX_RETRIES, WAIT_TIME_SECONDS)
        
        print(f"\n[DELAY] Czekam {INTER_TASK_DELAY}s...")
        time.sleep(INTER_TASK_DELAY)

        # --- ZADANIE 4: Inteligentna Aranżacja ---
        balloon_theme = analyze_image_theme(model, improved_image, PROMPTS["step_4a_analyze"])
        themed_prompt = PROMPTS["step_4b_themed_template"].format(theme=balloon_theme)
        path_4 = os.path.join(OUTPUT_DIR, f"{sku}_3.jpg")
        generate_and_save_image(model, themed_prompt, improved_image, path_4, MAX_RETRIES, WAIT_TIME_SECONDS)

    print("\n\n🎉 ZAKOŃCZONO: Pomyślnie przetworzono wszystkie zadania.")

if __name__ == "__main__":
    main()