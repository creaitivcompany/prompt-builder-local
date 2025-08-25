"""
AI Generator Configurations
Contains all AI image generator settings, syntax rules, and metadata.
"""

# AI Generator configurations with metadata
AI_GENERATORS = {
    "None": {
        "prefix": "",
        "suffix": "",
        "style_keywords": [],
        "supports_negative_prompt": False,
        "has_flags": False,
        "category": "basic"
    },
    
    "Stable Diffusion": {
        "prefix": "",
        "suffix": ", highly detailed, 8k resolution, professional photography",
        "style_keywords": ["photorealistic", "cinematic lighting", "sharp focus"],
        "supports_negative_prompt": True,
        "has_flags": False,
        "category": "stable_diffusion",
        "default_negative": "lowres, blurry, bad anatomy, watermark, text, signature"
    },
    
    "SDXL": {
        "prefix": "",
        "suffix": ", high detail, sharp focus, 4k, photography",
        "style_keywords": ["photorealistic", "soft light", "detailed textures"],
        "supports_negative_prompt": True,
        "has_flags": False,
        "category": "stable_diffusion",
        "default_negative": "lowres, blurry, bad anatomy, watermark, text, signature, worst quality"
    },
    
    "ComfyUI/Auto1111": {
        "prefix": "",
        "suffix": ", best quality, high detail",
        "style_keywords": ["photorealistic", "cinematic lighting", "sharp focus"],
        "supports_negative_prompt": True,
        "has_flags": False,
        "category": "stable_diffusion",
        "default_negative": "lowres, blurry, bad anatomy, watermark, text, signature, worst quality, low quality",
        "supports_lora": True
    },
    
    "Flux": {
        "prefix": "",
        "suffix": ", photoreal, crisp lighting, 50mm lens, natural skin tones",
        "style_keywords": ["realistic skin", "subtle bokeh", "dynamic range"],
        "supports_negative_prompt": True,
        "has_flags": False,
        "category": "flux",
        "default_negative": "blurry, low quality, distorted, artificial"
    },
    
    "Midjourney": {
        "prefix": "",
        "suffix": " --ar 16:9 --v 6 --style raw",
        "style_keywords": ["hyperrealistic", "award-winning", "trending on artstation"],
        "supports_negative_prompt": False,
        "has_flags": True,
        "category": "midjourney",
        "flag_options": {
            "aspect_ratios": ["1:1", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2"],
            "versions": ["6", "5.2", "5.1", "5"],
            "styles": ["raw", "default"],
            "stylize_range": [0, 1000]
        }
    },
    
    "DALL-E 3": {
        "prefix": "Create an image of ",
        "suffix": ". High quality, detailed, professional.",
        "style_keywords": ["vibrant colors", "clear details", "artistic composition"],
        "supports_negative_prompt": False,
        "has_flags": False,
        "category": "dalle"
    },
    
    "Leonardo AI": {
        "prefix": "",
        "suffix": ", masterpiece, best quality, ultra-detailed",
        "style_keywords": ["photorealistic", "dramatic lighting", "high contrast"],
        "supports_negative_prompt": False,
        "has_flags": False,
        "category": "leonardo"
    },
    
    "Ideogram": {
        "prefix": "",
        "suffix": ", clean vector style, legible typography, centered composition",
        "style_keywords": ["minimal design", "flat colors", "high contrast"],
        "supports_negative_prompt": False,
        "has_flags": False,
        "category": "ideogram"
    },
    
    "Code playground v2.5": {
        "prefix": "",
        "suffix": ", soft cinematic lighting, high detail, film grain",
        "style_keywords": ["moody", "cinematic", "depth of field"],
        "supports_negative_prompt": False,
        "has_flags": False,
        "category": "playground"
    },
    
    "Firefly": {
        "prefix": "",
        "suffix": ", studio lighting, editorial style, color-graded",
        "style_keywords": ["commercial photography", "balanced contrast", "professional finish"],
        "supports_negative_prompt": False,
        "has_flags": False,
        "category": "firefly"
    },
    
    "Kandinsky 3": {
        "prefix": "",
        "suffix": ", minimal, modern, matte finish",
        "style_keywords": ["clean composition", "subtle shading", "elegant"],
        "supports_negative_prompt": False,
        "has_flags": False,
        "category": "kandinsky"
    }
}

def get_generator_names():
    """Return list of all generator names for dropdown."""
    return list(AI_GENERATORS.keys())

def get_generator_config(name):
    """Get configuration for a specific generator."""
    return AI_GENERATORS.get(name, AI_GENERATORS["None"])

def supports_negative_prompt(generator_name):
    """Check if generator supports negative prompts."""
    config = get_generator_config(generator_name)
    return config.get("supports_negative_prompt", False)

def has_flags(generator_name):
    """Check if generator uses command-line style flags."""
    config = get_generator_config(generator_name)
    return config.get("has_flags", False)

def get_default_negative_prompt(generator_name):
    """Get default negative prompt for generators that support it."""
    config = get_generator_config(generator_name)
    return config.get("default_negative", "")

def build_midjourney_flags(aspect_ratio="16:9", version="6", style="raw", stylize=None):
    """Build Midjourney-style flags."""
    flags = []
    if aspect_ratio:
        flags.append(f"--ar {aspect_ratio}")
    if version:
        flags.append(f"--v {version}")
    if style and style != "default":
        flags.append(f"--style {style}")
    if stylize is not None and stylize != 100:  # 100 is default
        flags.append(f"--stylize {stylize}")
    
    return " " + " ".join(flags) if flags else ""

def format_prompt(generator_name, base_prompt, **kwargs):
    """
    Format prompt according to generator-specific rules.
    
    Args:
        generator_name: Name of the AI generator
        base_prompt: The base prompt text
        **kwargs: Additional parameters like negative_prompt, aspect_ratio, etc.
    
    Returns:
        dict with 'positive' and optionally 'negative' prompts
    """
    config = get_generator_config(generator_name)
    
    if generator_name == "None":
        return {"positive": base_prompt, "negative": ""}
    
    # Build positive prompt
    positive_prompt = config["prefix"] + base_prompt
    
    # Add style keywords based on generator type
    if generator_name == "Midjourney":
        if config["style_keywords"]:
            positive_prompt = base_prompt + " " + ", ".join(config["style_keywords"])
        # Add Midjourney flags
        flags = build_midjourney_flags(
            aspect_ratio=kwargs.get("aspect_ratio", "16:9"),
            version=kwargs.get("version", "6"),
            style=kwargs.get("style", "raw"),
            stylize=kwargs.get("stylize")
        )
        positive_prompt += flags
        
    elif generator_name in ["Stable Diffusion", "SDXL", "ComfyUI/Auto1111", "Flux"]:
        if config["style_keywords"]:
            positive_prompt = base_prompt + ", " + ", ".join(config["style_keywords"])
        positive_prompt += config["suffix"]
        
    elif generator_name == "DALL-E 3":
        positive_prompt = config["prefix"] + base_prompt + config["suffix"]
        
    else:
        # Default formatting for other generators
        if config["style_keywords"]:
            positive_prompt = base_prompt + ", " + ", ".join(config["style_keywords"])
        positive_prompt += config["suffix"]
    
    result = {"positive": positive_prompt}
    
    # Add negative prompt if supported
    if supports_negative_prompt(generator_name):
        negative = kwargs.get("negative_prompt", get_default_negative_prompt(generator_name))
        result["negative"] = negative
    else:
        result["negative"] = ""
    
    return result

def get_generator_categories():
    """Get generators grouped by category."""
    categories = {}
    for name, config in AI_GENERATORS.items():
        category = config.get("category", "other")
        if category not in categories:
            categories[category] = []
        categories[category].append(name)
    return categories

def get_midjourney_options():
    """Get Midjourney-specific UI options."""
    config = get_generator_config("Midjourney")
    return config.get("flag_options", {})