import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import platform
import time
import argparse
import os

class AppleSiliconBLIP:
    def __init__(self, model_size="base"):
        print("🍎 Initializing BLIP-1 for Apple Silicon...")
        self.device = self._get_device()

        model_names = {
            "base": "Salesforce/blip-image-captioning-base",
            "large": "Salesforce/blip-image-captioning-large"
        }
        model_name = model_names.get(model_size, model_names["base"])
        print(f"Loading model: {model_name}")

        print("Loading processor...")
        self.processor = BlipProcessor.from_pretrained(model_name)

        print("Loading model...")
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        print(f"✅ BLIP-1 loaded successfully on {self.device}")
        if self.device == "mps":
            print("🔧 Applying Apple Silicon optimizations...")
            try:
                torch.backends.mps.empty_cache()
                print("✅ MPS cache cleared")
            except:
                pass

    def _get_device(self):
        if torch.backends.mps.is_available():
            print("✅ Using Apple Silicon GPU (MPS)")
            return "mps"
        elif torch.cuda.is_available():
            print("✅ Using NVIDIA GPU (CUDA)")
            return "cuda"
        else:
            print("⚠️  Using CPU")
            return "cpu"

    def generate_caption(self, image_path, prompt_type="detailed", max_length=50):
        print(f"📸 Processing: {image_path}")
        try:
            image = Image.open(image_path).convert('RGB')
            print(f"Image loaded: {image.size}")
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return None

        prompts = {
            "simple": "",
            "detailed": "a detailed description of",
            "creative": "an artistic description of",
            "custom": "describe this image for AI art generation:"
        }
        prompt = prompts.get(prompt_type, "")

        print(f"🔄 Generating {prompt_type} caption...")
        start_time = time.time()

        if prompt:
            inputs = self.processor(image, prompt, return_tensors="pt").to(self.device)
        else:
            inputs = self.processor(image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            with torch.inference_mode():
                generated_ids = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=4,
                    early_stopping=True,
                    do_sample=False  # deterministic, avoids pad_token_id conflicts
                )

        caption = self.processor.decode(generated_ids[0], skip_special_tokens=True)
        if prompt and caption.startswith(prompt):
            caption = caption[len(prompt):].strip()

        end_time = time.time()
        print(f"✅ Generated in {(end_time - start_time):.2f}s: {caption}")

        if self.device == "mps":
            try:
                torch.backends.mps.empty_cache()
            except:
                pass
        return caption

    def generate_multiple_captions(self, image_path, styles=None):
        if styles is None:
            styles = ["simple", "detailed", "creative"]
        results = {}
        print(f"\n🎯 Generating {len(styles)} caption styles...")
        for style in styles:
            caption = self.generate_caption(image_path, style)
            if caption:
                results[style] = caption
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Generate image captions using BLIP-1 on Apple Silicon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 blip1_m1_optimized.py
  python3 blip1_m1_optimized.py my_photo.jpg
  python3 blip1_m1_optimized.py image.png --style detailed
        """
    )
    parser.add_argument('image_path', nargs='?', default='test_image.jpg', help='Path to the image file')
    parser.add_argument('--style', choices=['simple', 'detailed', 'creative', 'all'], default='all')
    parser.add_argument('--model-size', choices=['base', 'large'], default='base')
    args = parser.parse_args()

    print("🍎 BLIP-1 Apple Silicon Demo")
    print("=" * 50)
    print(f"Image: {args.image_path}")
    print(f"Style: {args.style}")
    print(f"Model: {args.model_size}\n")

    if platform.machine() == "arm64":
        print("✅ Running on Apple Silicon")
    else:
        print("ℹ️  Not on Apple Silicon, but will work on any system")

    if not os.path.exists(args.image_path):
        print(f"❌ Image file '{args.image_path}' not found!")
        if args.image_path == "test_image.jpg":
            print("💡 Run 'python3 download_test_image.py' to get a test image")
        return

    try:
        blip = AppleSiliconBLIP(args.model_size)
    except Exception as e:
        print(f"❌ Failed to initialize BLIP-1: {e}")
        return

    try:
        if args.style == 'all':
            results = blip.generate_multiple_captions(args.image_path)
            print("\n🎉 Results:\n" + "=" * 30)
            for style, caption in results.items():
                print(f"\n{style.upper()}:\n  {caption}")
        else:
            caption = blip.generate_caption(args.image_path, args.style)
            print(f"\n🎉 {args.style.upper()} Caption:\n" + "=" * 30)
            print(f"  {caption}")
    except Exception as e:
        print(f"❌ Caption generation failed: {e}")
        print("💡 Try using a different image or check if the file is corrupted")

if __name__ == "__main__":
    main()