# src/file_handler.py
import os
from PIL import UnidentifiedImageError
from vertexai.generative_models import Image as VertexImage

def find_input_images(input_dir: str) -> list[str]:
    """Skanuje folder wejściowy i zwraca listę ścieżek do obsługiwanych plików graficznych."""
    supported_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    image_paths = []
    if not os.path.isdir(input_dir):
        print(f"❌ BŁĄD: Folder wejściowy '{input_dir}' nie istnieje. Tworzenie folderu...")
        os.makedirs(input_dir)
        return []

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_extensions):
            image_paths.append(os.path.join(input_dir, filename))
    
    return image_paths

def load_image_from_file(file_path: str) -> VertexImage | None:
    """Wczytuje obraz z pliku i zwraca go jako obiekt VertexImage."""
    print(f"\n[ŁADOWANIE] Wczytywanie obrazu z: {file_path}...")
    try:
        return VertexImage.load_from_file(file_path)
    except (FileNotFoundError, UnidentifiedImageError, Exception) as e:
        print(f"❌ Błąd wczytywania obrazu: {e}")
        return None