# src/config.py

# --- Konfiguracja Połączenia z Google Cloud ---
GCP_LOCATION = "us-central1"
# ZMIANA: Używamy dwóch najnowszych, wyspecjalizowanych modeli Flash
TEXT_MODEL_NAME = "gemini-2.5-flash"  # Model do analizy i zadań tekstowych
IMAGE_MODEL_NAME = "gemini-2.5-flash-image" # Model zoptymalizowany do generowania obrazów

# --- Konfiguracja Procesu ---
MAX_RETRIES = 3
WAIT_TIME_SECONDS = 20
# Usunęliśmy IMAGES_PER_PRODUCT, ponieważ teraz liczba zdjęć zależy od liczby promptów

# --- Konfiguracja Ścieżek ---
CSV_FILE_PATH = "lista zdjec do poprawienia csv.csv"
OUTPUT_DIR = "output" # Folder na wygenerowane obrazy

# --- Słowa Kluczowe do Analizy Nazwy Produktu ---
# Ta logika pozostaje, aby dynamicznie określać grupę docelową w promptach lifestyle
KIDS_KEYWORDS = ["dziecka", "roczek", "chrzest", "urodziny chłopca", "urodziny dziewczynki", "baby shower", "dla dzieci"]
ADULT_KEYWORDS = ["panieński", "kawalerski", "18-stka", "sylwester", "dla dorosłych", "wódki", "alkohol", "impreza firmowa"]

# --- NOWOŚĆ: Paczka zróżnicowanych promptów do generowania różnych typów zdjęć ---
PROMPT_TEMPLATES = {
    # 1. Czyste zdjęcie produktowe (packshot)
    "packshot": (
        "Zadanie: Ulepsz to zdjęcie produktu e-commerce do perfekcyjnej jakości. "
        "Popraw kąty, aby uzyskać profesjonalny, centralny widok. "
        "Wzmocnij kolory i oświetlenie, zachowując naturalny wygląd produktu. "
        "Umieść finalny, niezmieniony produkt na idealnie białym tle (#FFFFFF). "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),

    # 2. Zdjęcie studyjne z rekwizytami
    "studio_props": (
        "Zadanie: Stwórz profesjonalne zdjęcie studyjne produktu: '{product_name}'. "
        "Umieść go w otoczeniu tematycznych rekwizytów imprezowych (np. serpentyny, konfetti, prezenty). "
        "Tło powinno być proste, w pastelowym kolorze, a oświetlenie studyjne, miękkie i komercyjne. "
        "Kompozycja musi być estetyczna i nowoczesna. "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),

    # 3. Główna scena lifestyle (dynamicznie dopasowywana)
    "lifestyle_scene": (
        "Zadanie: Stwórz fotorealistyczne, dynamiczne zdjęcie lifestylowe. "
        "Pokaż produkt '{product_name}' w użyciu podczas {style}. "
        "Na zdjęciu powinna być {audience}, naturalnie i radośnie bawiąca się, z produktem jako centralnym elementem. "
        "Ważne: Rozmiar produktu musi być realistycznie dopasowany do wielkości postaci. "
        "Estetyka: Scena powinna wyglądać jak z profesjonalnej sesji zdjęciowej. Użyj naturalnego, jasnego oświetlenia. "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    
    # 4. Zbliżenie na detal w użyciu
    "lifestyle_detail": (
        "Zadanie: Stwórz artystyczne, zbliżeniowe zdjęcie lifestylowe produktu '{product_name}'. "
        "Skup się na detalu produktu trzymanego przez osobę (widoczna tylko część dłoni/ramienia) z tłem '{style}' w miękkim rozmyciu (bokeh). "
        "Oświetlenie powinno być naturalne i podkreślać teksturę produktu. "
        "Scena ma być aspiracyjna i estetyczna. {audience} jest tylko subtelnym tłem. "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    )
}

