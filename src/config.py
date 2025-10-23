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

# --- USUNIĘTO SŁOWA KLUCZOWE ---
# Logika została przeniesiona do modelu AI

# --- ZMODYFIKOWANY Prompt Analityczny (Nowa logika audytorium) ---
ANALYSIS_PROMPT = (
    "Przeanalizuj poniższe dane produktu. Twoim zadaniem jest zwrócić szczegółowy raport w formacie JSON. "
    "Odpowiedź musi zawierać TYLKO i wyłącznie obiekt JSON z następującymi kluczami: "
    "1. 'product_type': (string) Określ typ produktu (np. 'Balon lateksowy', 'Świeczka urodzinowa'). "
    "2. 'main_subject': (string) Opisz główny motyw/kształt (np. 'Cyfra 7', 'Postacie z Minecraft'). "
    "3. 'style_keywords': (string) Podaj 3-5 słów kluczowych opisujących styl (np. 'elegancki, nowoczesny'). "
    "4. 'detected_size_cm': (integer) Jeśli znajdziesz rozmiar w cm, podaj go. Jeśli nie, MUSISZ OSZACOWAĆ przybliżony rozmiar na podstawie zdjęcia. Zawsze zwróć liczbę. (Ważne dla reguł fizyki!)"
    "5. 'detected_quantity': (integer) Przeanalizuj nazwę i opis. Jeśli mowa o jednym produkcie, zwróć 1. Jeśli to zestaw (np. '10 szt.'), zwróć liczbę sztuk. Zawsze zwróć liczbę. "
    "6. 'suggested_theme': (string) Zaproponuj motyw przewodni imprezy (np. 'urodziny dziecka'). "
    "7. 'scale_description': (string) BARDZO WAŻNE: Na podstawie 'detected_size_cm' i 'product_type', napisz krótki, ale obrazowy opis skali produktu w kontekście człowieka lub powszechnego obiektu (np. 'To jest mały przedmiot, wielkości dłoni' lub 'To duży balon foliowy, prawie tak wysoki jak przedszkolak')."
    "8. 'suggested_audience': (string) NOWE ZADANIE: Na podstawie wszystkich danych (obraz, nazwa, motyw, kolory), wybierz NAJBARDZIEJ PASUJĄCĄ grupę docelową z poniższej listy. Zwróć DOKŁADNIE jeden z tych ciągów znaków: "
    "[ 'grupa małych dzieci (1-3 lata)', 'grupa przedszkolaków (4-7 lat)', 'grupa dzieci w wieku szkolnym (8-15 lat)', 'grupa dorosłych osób', 'grupa osób w różnym wieku' ] "
    "Wybierz 'grupa osób w różnym wieku' TYLKO jeśli produkt jest skrajnie uniwersalny (np. zwykłe złote balony)."
)

# --- Prompty Generujące (używają teraz 'suggested_audience') ---
PROMPT_TEMPLATES = {
    "packshot": (
        "Zadanie: Stwórz perfekcyjne zdjęcie produktowe (packshot). "
        "KADROWANIE (KRYTYCZNE): Produkt powinien być dobrze wyeksponowany i zajmować większość kadru. Unikaj przycinania ważnych elementów. "
        "Tło musi być idealnie białe (#FFFFFF). Oświetlenie studyjne, bez ostrych cieni. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): {scale_description} "
        "{quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "studio_interaction": (
        "Zadanie: Stwórz profesjonalne zdjęcie studyjne z interakją. "
        "Scena: {suggested_audience} (wygląd słowiański) trzyma produkt lub wchodzi z nim w interakcję. "
        "Tło proste, jednolite, w pastelowym kolorze. Oświetlenie studyjne, miękkie i komercyjne. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): Zachowaj realistyczną skalę produktu względem postaci. {scale_description} "
        "{quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "studio_props": (
        "Zadanie: Stwórz profesjonalne zdjęcie studyjne z rekwizytami. "
        "Scena: Produkt umieszczony jest w estetycznej kompozycji z rekwizytami pasującymi do motywu '{suggested_theme}' (np. konfetti, serpentyny, prezenty). "
        "Tło proste, w pastelowym kolorze. Oświetlenie studyjne. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): {scale_description} "
        "{quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    ),
    "lifestyle_scene": (
        "Zadanie: Stwórz fotorealistyczne, dynamiczne zdjęcie lifestylowe. "
        "Scena: Pokaż produkt w użyciu podczas '{suggested_theme}'. "
        "Na zdjęciu powinna być {suggested_audience} (wygląd słowiański), naturalnie i radośnie bawiąca się, z produktem jako centralnym elementem. "
        "INTEGRALNOŚĆ (KRYTYCZNE): ZACHOWAJ wszystkie istniejące, oryginalne napisy i logo na produkcie, ale pod żadnym pozorem NIE DODAWJ żadnych nowych. "
        "SKALA (KRYTYCZNE): Zachowaj absolutnie realistyczną skalę produktu względem postaci. {scale_description} "
        "{quantity_info} {physics_info} {interaction_info} "
        "**Zwróć tylko i wyłącznie sam obraz, bez żadnego tekstu.**"
    )
}

