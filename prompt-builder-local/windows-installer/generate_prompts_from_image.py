from blip1_m1_optimized import AppleSiliconBLIP
import os
import re

blip = None  # Lazy init

def normalize_text(text: str) -> str:
    # Basic cleanup
    text = text.strip()
    # Fix spaced apostrophes like "dog ' s" -> "dog's"
    text = re.sub(r"\s+'\s+", "'", text)
    # Collapse multiple spaces
    text = re.sub(r"\s{2,}", " ", text)
    # Remove stray leading/trailing braces or quotes
    text = text.strip(" {}[]\"'")
    return text

def generate_prompts_from_image(image_path, model_size="base"):
    global blip

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Lazy-initialize BLIP-1 once
    if blip is None:
        blip = AppleSiliconBLIP(model_size)

    # 1) Get a strong descriptive base caption
    base = blip.generate_caption(image_path, prompt_type="detailed", max_length=60) or ""
    base = normalize_text(base)

    if not base:
        # True fallback: only use this if BLIP returns empty
        return [
            "Describe the image in detail: subject, composition, colors, style, lighting.",
            "Summarize key elements of the image as an AI art prompt.",
            "Extract objects, scene, mood, and style cues from the image."
        ]

    # 2) Create 3 useful variations from the base caption
    prompts = [
        normalize_text(f"{base}, photorealistic, high detail, natural lighting, crisp focus"),
        normalize_text(f"{base}, minimalist composition, soft lighting, muted palette, modern design"),
        normalize_text(f"{base}, artistic interpretation, cinematic lighting, volumetric light, dramatic contrast")
    ]
    return prompts