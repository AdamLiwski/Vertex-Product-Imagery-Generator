import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "marine-base-474312-g7"
LOCATION = "us-central1"

print("--- Start OSTATECZNEGO skryptu testowego ---")
try:
    print(f"Łączenie z projektem '{PROJECT_ID}'...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print("-> Inicjalizacja OK.")

    print("Wysyłanie najprostszego możliwego zapytania...")
    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("test")

    print("\n--- !!! SUKCES !!! ---")
    print(f"Odpowiedź modelu: {response.text}")

except Exception as e:
    print("\n--- !!! BŁĄD !!! ---")
    print(f"Szczegóły błędu: {e}")

print("\n--- Koniec testu ---")