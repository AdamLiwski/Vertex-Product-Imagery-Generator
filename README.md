# Vertex AI Product Imagery Generator

Automated e-commerce product image generation and editing using Google Vertex AI's Imagen 3.0 model. This Python solution transforms basic product photos into professional studio shots and engaging lifestyle scenes (Image-to-Image), featuring robust quota and error handling for production readiness.

---

### Key Features

- **Automated Workflow:** Processes all images from an `input` folder and saves the results to an `output` folder.
- **Multi-Step Processing:** Implements a configurable, multi-step pipeline for image generation (e.g., studio shot, lifestyle scenes).
- **Intelligent Theming:** Includes a step to analyze the product's theme and dynamically generate a context-aware lifestyle image.
- **Robust Error Handling:** Features a retry mechanism and handles common API errors like `ResourceExhausted` (quota limits).
- **Flexible Configuration:** All paths, model names, and prompts are centralized in a `config.py` file for easy customization.

### Technology Stack

- **Python 3**
- **Google Cloud Vertex AI:** (`gemini-1.5-flash-image` model)
- **Pillow (PIL):** For local image manipulation.
- **python-dotenv:** For secure management of environment variables.

---

### How to Use

**1. Clone the repository:**
```bash
git clone [https://github.com/AdamLiwski/Vertex-Product-Imagery-Generator.git](https://github.com/AdamLiwski/Vertex-Product-Imagery-Generator.git)
cd Vertex-Product-Imagery-Generator