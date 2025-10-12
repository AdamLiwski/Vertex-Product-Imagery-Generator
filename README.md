# 🎈 Vertex Product Imagery Generator

Automatyczny pipeline do generowania zdjęć produktowych z wykorzystaniem AI, zoptymalizowany pod kątem e-commerce. Projekt wykorzystuje modele generatywne Google Vertex AI (Gemini 2.5 Flash Image) do tworzenia scen lifestylowych na bazie zdjęć produktów — np. balonów — zgodnie ze standardami sklepów internetowych.

---

## 🚀 Funkcje

- ✅ Obsługa wejścia multimodalnego: obraz + tekst
- 🎨 Generacja scen lifestylowych z dziećmi, aranżacjami urodzinowymi i białym tłem
- 🔁 Retry logic przy błędach quota i API
- 🧠 Obsługa różnych typów odpowiedzi: `inline_data`, `generated_images`
- 📂 Automatyczne przetwarzanie folderów wejściowych i wyjściowych
- 📸 Zgodność z wymaganiami zdjęć produktowych (tło #FFFFFF, zachowanie kształtu)

---

## 🧠 Model GenAI

- **Używany model:** `gemini-2.5-flash-image`  
- **Region:** `us-central1`  
- **Obsługiwane typy odpowiedzi:** `inline_data.data` (nowy format), `generated_images` (fallback)

---

## 📦 Struktura folderów

