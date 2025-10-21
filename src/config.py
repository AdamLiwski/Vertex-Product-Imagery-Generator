# src/config.py

# --- Konfiguracja Połączenia z Google Cloud ---
GCP_LOCATION = "us-central1"
ANALYSIS_MODEL_NAME = "gemini-2.5-flash"
IMAGE_MODEL_NAME = "gemini-2.5-flash-image"

# --- Konfiguracja Procesu ---
MAX_RETRIES = 3
WAIT_TIME_SECONDS = 20

# --- Konfiguracja Ścieżek ---
CSV_FILE_PATH = "lista zdjec do poprawienia csv.csv"
OUTPUT_DIR = "output"

# --- NOWOŚĆ: Bardziej szczegółowe Słowa Kluczowe do Analizy ---
ADULT_KEYWORDS = ["panieński", "kawalerski", "18-stka", "sylwester", "dla dorosłych", "wódki", "alkohol", "impreza firmowa", "whisky"]
# Podział na grupy wiekowe dla dzieci
SCHOOL_AGE_KEYWORDS = ["minecraft", "fortnite", "harry potter", "gaming", "dla gracza", "starszych dzieci"] # Wiek 7-15
PRESCHOOLER_KEYWORDS = ["psi patrol", "świnka peppa", "masza i niedźwiedź", "dla przedszkolaka", "urodziny dziewczynki", "urodziny chłopca"] # Wiek 4-6
TODDLER_KEYWORDS = ["roczek", "chrzest", "baby shower", "pierwsze urodziny", "maluszka"] # Wiek 1-3


# --- Uproszczony Prompt Analityczny ---
ANALYSIS_PROMPT = (
    "Przeanalizuj poniższe dane produktu. Twoim zadaniem jest zwrócić szczegółowy raport w formacie JSON. "
    "Odpowiedź musi zawierać TYLKO i wyłącznie obiekt JSON z następującymi kluczami: "
    "1. 'product_type': (string) Określ typ produktu (np. 'Balon lateksowy', 'Świeczka urodzinowa'). "
    "2. 'main_subject': (string) Opisz główny motyw/kształt (np. 'Cyfra 7', 'Postacie z Minecraft'). "
    "3. 'style_keywords': (string) Podaj 3-5 słów kluczowych opisujących styl (np. 'elegancki, nowoczesny'). "
    "4. 'detected_size_cm': (integer) Jeśli znajdziesz rozmiar w cm, podaj go. Jeśli nie, MUSISZ OSZACOWAĆ przybliżony rozmiar na podstawie zdjęcia. Zawsze zwróć liczbę. "
    "5. 'detected_quantity': (integer) Przeanalizuj nazwę i opis. Jeśli mowa o jednym produkcie, zwróć 1. Jeśli to zestaw (np. '10 szt.'), zwróć liczbę sztuk. Zawsze zwróć liczbę. "
    "6. 'suggested_theme': (string) Zaproponuj motyw przewodni imprezy (np. 'urodziny dziecka'). "
)

# --- Zmodyfikowane Prompty Generujące ---
PROMPT_TEMPLATES = {
    "packshot": (
        "Zadanie: Stwórz perfekcyjne zdjęcie produktowe (packshot). "
        # ZMIANA: Złagodzono polecenie, aby uniknąć błędów
        "KADROWANIE (KRYTYCZNE): Produkt powinien być dobrze wyeksponowany i zajmować większość kadru. Unikaj przycinania ważnych elementów. "
        "Tło musi być idealnie białe (#FFFFFF). Oświetlenie studyjne, bez ostrych cieni. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "studio_interaction": (
        "Zadanie: Stwórz profesjonalne zdjęcie studyjne z interakją. "
        "Scena: {audience} (wygląd słowiański) trzyma produkt lub wchodzi z nim w interakcję. "
        "Tło proste, jednolite, w pastelowym kolorze. Oświetlenie studyjne, miękkie i komercyjne. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): Zachowaj absolutnie realistyczną skalę produktu względem postaci. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "studio_props": (
        "Zadanie: Stwórz profesjonalne zdjęcie studyjne z rekwizytami. "
        "Scena: Produkt umieszczony jest w estetycznej kompozycji z rekwizytami pasującymi do motywu '{suggested_theme}' (np. konfetti, serpentyny, prezenty). "
        "Tło proste, w pastelowym kolorze. Oświetlenie studyjne. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "lifestyle_scene": (
        "Zadanie: Stwórz fotorealistyczne, dynamiczne zdjęcie lifestylowe. "
        "Scena: Pokaż produkt w użyciu podczas '{suggested_theme}'. "
        "Na zdjęciu powinna być {audience} (wygląd słowiański), naturalnie i radośnie bawiąca się, z produktem jako centralnym elementem. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): Zachowaj absolutnie realistyczną skalę produktu względem postaci. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    )
}

