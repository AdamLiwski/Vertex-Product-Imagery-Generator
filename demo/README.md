# 🧪 Demo: Vertex Product Imagery Generator

This folder demonstrates the functionality of the AI-powered pipeline for automated product photo enhancement and lifestyle scene generation.

## 📥 Input Image

- `demo_input.png` — original product photo (e.g. balloon)

## 📤 AI-Generated Outputs

- `demo_output_0.jpg` — enhanced product photo with improved lighting and pure white background
- `demo_output_1.jpg` — lifestyle scene with a smiling child holding the balloon
- `demo_output_2.jpg` — birthday-themed arrangement with the balloon in a decorated room

## 🧠 Prompt Example

```text
Based on this improved photo of the balloon, create a new scene. 
Add a smiling child (age 4–6) holding the balloon with both hands and peeking out from behind it. 
Make sure the child is fully visible — including legs, feet, and a natural posture. 
Preserve the original shape of the balloon. 
Place the entire scene on a pure white background (#FFFFFF), following product photo standards. 
Return the result as an image. Do not reply with text.

✅ Status
The pipeline runs successfully using the gemini-2.5-flash-image model on Vertex AI. It supports multimodal input (image + text) and returns high-quality visual results suitable for e-commerce.

📁 How to Use This Demo
You can replicate this process by placing your own product image in the zdjecia_do_przerobienia/ folder and running image_modifier.py. The generated outputs will appear in the gotowe/ folder.

This demo is part of the Vertex Product Imagery Generator project by Adam Liwski.


---

Let me know if you’d like to add this to your GitHub Pages or turn it into a portfolio PDF. I can also help you write a short pitch for Upwork based on this demo. Ready to move forward?