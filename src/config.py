# src/config.py

# --- Konfiguracja Połączenia z Google Cloud ---
GCP_LOCATION = "us-central1"
# NOWOŚĆ: Definiujemy dwa osobne modele
ANALYSIS_MODEL_NAME = "gemini-2.5-flash"      # Nasz "Analityk" do tekstu i JSON
IMAGE_GENERATION_MODEL = "gemini-2.5-flash-image" # Nasz "Malarz" do obrazów

# --- Konfiguracja Procesu ---
MAX_RETRIES = 5
WAIT_TIME_SECONDS = 30
INTER_TASK_DELAY = 10

# --- Konfiguracja Ścieżek ---
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# --- Paczka Promptów ---
PROMPT_TEMPLATES = {
    "analysis": (
        "Analyze the product in this image. Respond in JSON format with two keys: "
        "'product_description' (a 3-5 word description, e.g., 'luxury men's Rolex watch') and "
        "'suggested_style' (1-3 keywords for a photoshoot theme, e.g., 'elegant, luxurious, professional')."
    ),
    "enhancement": (
        "Re-imagine this product photo to be of perfect e-commerce quality. "
        "Correct any awkward angles to present a clear, professional front-facing view of the product. "
        "Enhance colors and lighting. Place the final, unchanged product on a pure white background (#FFFFFF). "
        "**Return only the image.**"
    ),
    "studio_with_props": (
        "Create a professional studio photograph of the '{product_description}'. "
        "Place it on a simple, elegant prop suitable for this type of product (e.g., a stand for a watch, a pedestal for a sculpture, a stylish surface for electronics). "
        "The background should be clean and minimalist. Use commercial studio lighting. "
        "The style should be: {suggested_style}. **Return only the image.**"
    ),
    "lifestyle_in_use": (
        "Create a realistic lifestyle photo showing the '{product_description}' in practical use. "
        "A person appropriate for the product should be interacting with it naturally (e.g., a man wearing the watch, a person driving the car, a family watching the TV). "
        "The setting should be authentic and match the style: {suggested_style}. **Return only the image.**"
    ),
    "lifestyle_alternative": (
        "Create a second, different lifestyle photo of the '{product_description}'. "
        "Showcase the product in a beautiful, aspirational setting that reflects the style: {suggested_style}. "
        "The product should be the clear focus of the image. Use creative composition and natural lighting. "
        "**Return only the image.**"
    )
}