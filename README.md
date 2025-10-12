# 🚀 Vertex Product Imagery Generator

## ✨ Opis Projektu
**Vertex Product Imagery Generator** to zaawansowany skrypt w Pythonie, który wykorzystuje możliwości generatywnej sztucznej inteligencji **Google Vertex AI (Model Gemini 2.5 Flash)** do automatyzacji procesu tworzenia profesjonalnych i lifestylowych zdjęć produktowych.

Projekt demonstruje wykorzystanie zaawansowanego **Image-to-Image Generation** i obsługi błędów (w tym logiki ponawiania dla błędów Quota), co jest kluczowe w produkcyjnym środowisku pracy z AI.

### Kluczowe Funkcje
* **Optymalizacja Zdjęć**: Automatyczne poprawianie jakości, kolorów i cieni oryginalnego zdjęcia.
* **Usuwanie Tła**: Generowanie produktu na idealnie białym tle (#FFFFFF) spełniającym standardy e-commerce.
* **Tworzenie Scen Lifestylowych**: Generowanie dwóch unikalnych, lifestylowych scen z udziałem dzieci, wykorzystując ulepszony obraz bazowy jako źródło (`Image-to-Image`).
* **Solidna Architektura**: Implementacja obsługi błędów Quota i logiki ponawiania (retry mechanism).

---

## 🛠️ Technologie
* **Język**: Python 3.x
* **Platforma AI**: Google Cloud Vertex AI
* **Model GenAI**: `gemini-2.5-flash`
* **Biblioteki**: `google-cloud-aiplatform`, `Pillow`, `python-dotenv`

---

## ⚙️ Uruchomienie Projektu

### 1. Wymagania Wstępne
* Konto Google Cloud z aktywnym projektem.
* Włączone **Vertex AI API** w projekcie.
* Zainstalowany Google Cloud CLI (`gcloud`).
* **Ważne**: Upewnienie się, że Twoje konto ma odpowiednie limity (Quotas) dla modeli Gemini.

### 2. Konfiguracja Środowiska (Visual Studio Code)

1.  **Klonowanie Repozytorium**
    ```bash
    git clone [url_twojego_repo]
    cd Vertex-Product-Imagery-Generator
    ```

2.  **Uwierzytelnienie Google Cloud**
    Używamy Application Default Credentials (ADC) - jest to najbezpieczniejsza metoda.
    ```bash
    gcloud auth application-default login
    ```

3.  **Środowisko Wirtualne (VENV)**
    ```bash
    python -m venv venv
    # Aktywacja (macOS/Linux):
    source venv/bin/activate
    # Aktywacja (Windows PowerShell):
    # .\venv\Scripts\Activate
    
    pip install -r requirements.txt
    ```

4.  **Plik Konfiguracyjny `.env`**
    Utwórz plik `.env` w głównym folderze:
    ```dotenv
    GCLOUD_PROJECT_ID="twoj-project-id-z-google-cloud"
    ```

### 3. Przygotowanie Danych i Uruchomienie

1.  **Dane Wejściowe**: Utwórz folder `zdjecia_do_przerobienia` i umieść w nim zdjęcie, np. `BAF485800_0.jpg` (zgodnie z nazwą w pliku `image_modifier.py`).
2.  **Uruchomienie Skryptu**
    ```bash
    python image_modifier.py
    ```
3.  **Wyniki**: Gotowe zdjęcia znajdą się w nowo utworzonym folderze `gotowe/`.

---

## 🖼️ Rezultaty (Przykładowe Wyjście)

| Wejście (Oryginał) | Wynik 1 (Poprawa + Białe Tło) | Wynik 2 (Dziecko Zza Balonu) | Wynik 3 (Scena Urodzinowa) |
| :---: | :---: | :---: | :---: |
| [Obraz oryginalny] | [Obraz wynikowy SKU_0] | [Obraz wynikowy SKU_1] | [Obraz wynikowy SKU_2] |