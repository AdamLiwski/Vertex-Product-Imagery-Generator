# src/config.py

# --- Konfiguracja Połączenia z Google Cloud ---
GCP_LOCATION = "us-central1"
# ZMIANA: Model z Twojego skryptu, który działa.
IMAGE_GENERATION_MODEL = "gemini-2.5-flash-image"

# --- Konfiguracja Procesu ---
MAX_RETRIES = 5
WAIT_TIME_SECONDS = 30  # Czas oczekiwania po błędzie Quota
INTER_TASK_DELAY = 10   # Opóźnienie pomiędzy zadaniami generacji

# --- Konfiguracja Ścieżek ---
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# --- Paczka Promptów ---
# Tutaj definiujemy wszystkie kroki przetwarzania
PROMPTS = {
    "step_1_studio": (
        "Popraw to zdjęcie produktowe. Popraw cienie, oraz światło, aby produkt wyglądał atrakcyjniej. "
        "Ważne: zachowaj oryginalny, niezmieniony kolor i kształt produktu. "
        "Umieść finalny produkt na idealnie białym tle (#FFFFFF), zgodnie ze standardami dla sklepów internetowych. "
        "**Zwróć wynik jako obraz. Nie odpowiadaj tekstem.**"
    ),
    "step_2_lifestyle_child": (
        "Na podstawie tego poprawionego zdjęcia balonu, stwórz nową scenę. "
        "Dodaj uśmiechnięte dziecko (w wieku 4–6 lat), które trzyma balon obiema rękami i wychyla się zza niego. "
        "Upewnij się, że dziecko jest widoczne w całości — z nogami, stopami i naturalną postawą. "
        "Zachowaj oryginalny, niezmieniony kształt balonu. "
        "Całość umieść na idealnie białym tle (#FFFFFF), zgodnie ze standardami zdjęć produktowych. "
        "Zwróć wynik jako obraz. Nie odpowiadaj tekstem."
    ),
    "step_3_lifestyle_party": (
        "Na podstawie tego poprawionego zdjęcia balonu, stwórz piękną, lifestylową aranżację. "
        "Balon powinien być napełniony helem. Uśmiechnięte dziecko trzyma go na wstążce. "
        "Ważne: zachowaj oryginalny, niezmieniony kształt balonu. "
        "Tło powinno być jasne, estetyczne i pasujące do motywu urodzinowego, "
        "na przykład w pokoju dziecięcym podczas przyjęcia."
    ),
    # Prompt do analizy motywu dla kroku 4
    "step_4a_analyze": (
        "Analyze this image of a foil balloon. In 1-5 words, describe the main character or theme. "
        "Examples: 'cute deer', 'dinosaur', 'blue number three', 'red heart'."
    ),
    # Szablon promptu dla inteligentnej aranżacji
    "step_4b_themed_template": (
        "Based on the improved balloon photo, create a stunning, high-quality lifestyle arrangement. "
        "The main theme of the balloon is '{theme}'. The entire scene should match this theme. "
        "For example, if the theme is 'cute deer', the setting should be a forest party; if 'dinosaur', a prehistoric party. "
        "Show the balloon as the central element of the decoration. Maintain the original shape and design of the balloon. "
        "The overall atmosphere should be joyful and magical. **Return only the image.**"
    )
}