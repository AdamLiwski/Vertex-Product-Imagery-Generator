# src/config.py

# --- Konfiguracja Połączenia z Google Cloud ---
GCP_LOCATION = "us-central1"
ANALYSIS_MODEL_NAME = "gemini-2.5-flash"
IMAGE_MODEL_NAME = "gemini-2.5-flash-image" # Używamy pełnej, poprawnej nazwy

# --- Konfiguracja Procesu ---
MAX_RETRIES = 3
WAIT_TIME_SECONDS = 20

# --- Konfiguracja Ścieżek ---
CSV_FILE_PATH = "lista zdjec do poprawienia csv.csv"
OUTPUT_DIR = "output"

# --- Słowa Kluczowe do Analizy Nazwy Produktu ---
KIDS_KEYWORDS = ["dziecka", "roczek", "chrzest", "urodziny chłopca", "urodziny dziewczynki", "baby shower", "dla dzieci"]
ADULT_KEYWORDS = ["panieński", "kawalerski", "18-stka", "sylwester", "dla dorosłych", "wódki", "alkohol", "impreza firmowa", "whisky"]


# --- NOWA WERSJA: Prompt Analityczny z Dyrektywą o Realizmie 3D ---
ANALYSIS_PROMPT = (
    "Przeanalizuj poniższe dane produktu. Twoim zadaniem jest zwrócić szczegółowy raport w formacie JSON. "
    "Odpowiedź musi zawierać TYLKO i wyłącznie obiekt JSON z następującymi kluczami: "
    "1. 'product_type': (string) Określ typ produktu (np. 'Balon lateksowy', 'Świeczka urodzinowa'). "
    "2. 'main_subject': (string) Opisz główny motyw/kształt (np. 'Cyfra 7', 'Postacie z Minecraft'). "
    "3. 'style_keywords': (string) Podaj 3-5 słów kluczowych opisujących styl (np. 'elegancki, nowoczesny'). "
    "4. 'detected_size_cm': (integer) Jeśli znajdziesz rozmiar w cm, podaj go. Jeśli nie, MUSISZ OSZACOWAĆ przybliżony rozmiar na podstawie zdjęcia. Zawsze zwróć liczbę. "
    "5. 'detected_quantity': (integer) Przeanalizuj nazwę i opis. Jeśli mowa o jednym produkcie, zwróć 1. Jeśli to zestaw (np. '10 szt.'), zwróć liczbę sztuk. Zawsze zwróć liczbę. "
    "6. 'suggested_theme': (string) Zaproponuj motyw przewodni imprezy (np. 'urodziny dziecka'). "
    "7. 'needs_3d_realism': (boolean) BARDZO WAŻNE: Jeśli 'product_type' to 'Balon lateksowy' i na zdjęciu wejściowym wygląda on jak ZDJĘCIE PRODUKTOWE, RENDER lub GRAFIKA, a nie jak obiekt na prawdziwym, fotorealistycznym zdjęciu, zwróć 'true'. Priorytetem jest dodanie realizmu do nie-fotorealistycznych obrazów. W każdym innym przypadku zwróć 'false'."
)


# --- Prompty Generujące z Placeholderami na Reguły ---
PROMPT_TEMPLATES = {
    "packshot": (
        "Zadanie: Stwórz perfekcyjne zdjęcie produktowe (packshot). {realism_info}"
        "KADROWANIE (KRYTYCZNE): Produkt musi maksymalnie wypełniać kwadratowy kadr, z minimalnymi marginesami. "
        "Tło musi być idealnie białe (#FFFFFF). Oświetlenie studyjne, bez ostrych cieni. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "studio_interaction": (
        "Zadanie: Stwórz profesjonalne zdjęcie studyjne z interakcją. {realism_info}"
        "Scena: {audience} (wygląd słowiański) trzyma produkt lub wchodzi z nim w interakcję. "
        "Tło proste, jednolite, w pastelowym kolorze. Oświetlenie studyjne, miękkie i komercyjne. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): Zachowaj absolutnie realistyczną skalę produktu względem postaci. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "studio_props": (
        "Zadanie: Stwórz profesjonalne zdjęcie studyjne z rekwizytami. {realism_info}"
        "Scena: Produkt umieszczony jest w estetycznej kompozycji z rekwizytami pasującymi do motywu '{suggested_theme}' (np. konfetti, serpentyny, prezenty). "
        "Tło proste, w pastelowym kolorze. Oświetlenie studyjne. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "lifestyle_scene": (
        "Zadanie: Stwórz fotorealistyczne, dynamiczne zdjęcie lifestylowe. {realism_info}"
        "Scena: Pokaż produkt w użyciu podczas '{suggested_theme}'. "
        "Na zdjęciu powinna być {audience} (wygląd słowiański), naturalnie i radośnie bawiąca się, z produktem jako centralnym elementem. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): Zachowaj absolutnie realistyczną skalę produktu względem postaci. "
        "{size_info} {quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    )
}

