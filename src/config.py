# src/config.py

# --- Konfiguracja Połączenia z Google Cloud ---
GCP_LOCATION = "us-central1"
IMAGE_MODEL_NAME = "gemini-2.5-flash-image"

# --- Konfiguracja Procesu ---
MAX_RETRIES = 3
WAIT_TIME_SECONDS = 20 # Dajemy modelowi trochę więcej czasu na złożone zadania

# --- Konfiguracja Ścieżek ---
CSV_FILE_PATH = "czarny.csv"
OUTPUT_DIR = "output_czarny_zestaw" # Nowy, dedykowany folder wyjściowy

# --- Słowa Kluczowe do Analizy Stylu ---
CHILDREN_KEYWORDS = ['roczek', 'urodziny dziecka', 'chrzest']
ADULT_KEYWORDS = ['panieński', 'kawalerski', '18-stka', 'osiemnastka', 'rocznica']

# --- NOWOŚĆ: Prompty zmodyfikowane do pracy z obrazem referencyjnym ---
PROMPT_TEMPLATES = {
    # 1. Czyste zdjęcie produktowe (packshot)
    "packshot": (
        "To jest obraz referencyjny dla stylu, koloru i ogólnego oświetlenia. "
        "Twoim zadaniem jest zastosować ten sam spójny styl do drugiego, głównego obrazu produktu. "
        "Ulepsz go do perfekcyjnej jakości e-commerce, poprawiając wszelkie niedoskonałości cieni i światła, "
        "aby produkt był idealnie wyeksponowany i ostry. "
        "Umieść finalny, niezmieniony produkt, którym jest **duży balon foliowy (100 cm)**, "
        "na idealnie białym tle (#FFFFFF). "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),

    # 2. Zdjęcie studyjne z rekwizytami
    "studio_props": (
        "To jest obraz referencyjny dla spójności koloru i stylu. Zastosuj go do drugiego, "
        "głównego obrazu produktu. Stwórz profesjonalne zdjęcie studyjne produktu: '{product_name}'. "
        "Umieść go w otoczeniu tematycznych rekwizytów imprezowych (np. serpentyny, konfetti, prezenty, balony w tle). "
        "Tło powinno być proste, w pastelowym kolorze, a oświetlenie studyjne, miękkie i komercyjne. "
        "Kompozycja musi być estetyczna i nowoczesna. Produkt to **duży balon foliowy (100 cm)**. "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),

    # 3. Główna scena lifestyle (dynamicznie dopasowywana)
    "lifestyle_scene": (
        "To jest obraz referencyjny dla spójności koloru i stylu. Zastosuj go do drugiego, "
        "głównego obrazu produktu. Stwórz fotorealistyczne, dynamiczne zdjęcie lifestylowe. "
        "Pokaż produkt '{product_name}' w użyciu podczas {style}. "
        "Na zdjęciu powinna być {audience}, naturalnie i radośnie bawiąca się, z produktem jako centralnym elementem. "
        "Ważne: Produkt to **duży balon foliowy (100 cm)** i jego rozmiar musi być realistycznie dopasowany do wielkości postaci. "
        "Estetyka: Scena powinna wyglądać jak z profesjonalnej sesji zdjęciowej. Użyj naturalnego, jasnego oświetlenia. "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    
    # 4. Zbliżenie na detal w użyciu
    "lifestyle_detail": (
        "To jest obraz referencyjny dla spójności koloru i stylu. Zastosuj go do drugiego, "
        "głównego obrazu produktu. Stwórz artystyczne, zbliżeniowe zdjęcie lifestylowe produktu '{product_name}'. "
        "Skup się na detalu produktu (którym jest **duży balon foliowy 100 cm**) trzymanego przez osobę "
        "(widoczna tylko część dłoni/ramienia) z tłem '{style}' w miękkim rozmyciu (bokeh). "
        "Oświetlenie powinno być naturalne i podkreślać teksturę produktu. "
        "Scena ma być aspiracyjna i estetyczna. {audience} jest tylko subtelnym tłem. "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    )
}

