"""
HPPCS[03] Advertisement Creator using Image Generation.

Required pipeline:
1. Qwen3 (LLM #1) converts advertisement text into a creative brief.
2. Llama 3.2 (LLM #2) converts the brief into an image-generation prompt.
3. FLUX.1-schnell generates a realistic commercial product visual.
4. Pillow composes the visual and exact advertisement copy into ONE supplied
   advertisement template to produce three final advertisements.

Modes:
    python main.py --demo
        Uses the included realistic visual samples. No model download is needed.

    python main.py --live
        Uses local Ollama (Qwen3 + Llama 3.2) and Diffusers/FLUX.
"""
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

import torch

if not torch.cuda.is_available():
    raise RuntimeError(
        "FLUX image generation requires a CUDA-capable GPU. "
        "Run this project in Google Colab with GPU enabled."
    )

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "ad_template.png"
ADS = {
    1: ROOT / "ad_text_1.txt",
    2: ROOT / "ad_text_2.txt",
    3: ROOT / "ad_text_3.txt",
}
# The central photo area in the actual advertisement template.
VISUAL_BOX = (59, 148, 715, 638)


def read_advertisement(path: Path) -> dict:
    """Read Brand/Product/Headline/Message/CTA fields from an ad text file."""
    text = path.read_text(encoding="utf-8").strip()
    data = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip().lower()] = value.strip()
    return data


def call_ollama(model: str, prompt: str) -> str:
    """Call a local Ollama model and return its response."""
    import requests

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=1800,
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def create_creative_brief(ad: dict) -> str:
    """Use Qwen3 as LLM #1 to create a concise visual creative brief."""
    prompt = f"""
You are a senior advertising creative strategist.
Analyze this advertisement and create a concise visual creative brief.

Brand: {ad.get('brand', '')}
Product: {ad.get('product', '')}
Headline: {ad.get('headline', '')}
Message: {ad.get('message', '')}
CTA: {ad.get('cta', '')}

Return product, target audience, marketing objective, emotional tone,
setting, visual concept, lighting, composition, color direction and
must-show product details.
"""
    return call_ollama("qwen3:4b", prompt)


def create_image_prompt(brief: str) -> str:
    """Use Llama 3.2 as LLM #2 to create a FLUX-ready visual prompt."""
    prompt = f"""
You are an expert commercial image-prompt engineer.
Turn the following creative brief into a photorealistic FLUX.1-schnell prompt.

CREATIVE BRIEF:
{brief}

Requirements:
- realistic commercial product photography
- product is the clear visual focus
- premium advertising lighting and composition
- realistic materials, reflections and shadows
- setting must match the product
- no invented slogans, typography, logos, watermarks or readable text
- Python will add the exact advertisement copy after image generation
"""
    return call_ollama("llama3.2:3b", prompt)


def generate_flux_image(prompt: str, output_path: Path) -> Path:
    """Generate a realistic product visual with FLUX.1-schnell."""
    import torch
    from diffusers import FluxPipeline

    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-schnell",
        dtype=dtype,
        token=True,
    )
    if torch.cuda.is_available():
        pipe.enable_model_cpu_offload()
    else:
        pipe.to("cpu")

    image = pipe(
        prompt=prompt,
        height=656,
        width=656,
        num_inference_steps=4,
        guidance_scale=0.0,
    ).images[0]
    image.save(output_path)
    return output_path


def load_font(size: int, bold: bool = False):
    """Load a common font with a fallback for environments without fonts."""
    candidates = (
        ["DejaVuSans-Bold.ttf", "arialbd.ttf"]
        if bold
        else ["DejaVuSans.ttf", "arial.ttf"]
    )
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap_text(draw, text: str, font, max_width: int) -> str:
    """Wrap text to fit a fixed pixel width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return "\n".join(lines)


def compose_ad(visual_path: Path, ad: dict, output_path: Path) -> None:
    """Compose one generated visual and exact ad copy into the single template."""
    base = Image.open(TEMPLATE).convert("RGB")
    visual = Image.open(visual_path).convert("RGB")
    target = (VISUAL_BOX[2] - VISUAL_BOX[0], VISUAL_BOX[3] - VISUAL_BOX[1])
    visual = ImageOps.fit(visual, target, method=Image.Resampling.LANCZOS)
    base.paste(visual, (VISUAL_BOX[0], VISUAL_BOX[1]))

    draw = ImageDraw.Draw(base)
    dark = (25, 25, 25)
    white = (245, 245, 245)
    gray = (75, 75, 75)

    # Clear and redraw header/copy areas so the supplied text is exact.
    draw.rectangle((45, 35, 350, 105), fill=dark)
    draw.rectangle((60, 690, 710, 885), fill=(255, 255, 255))

    brand_font = load_font(12)
    headline_font = load_font(14, bold=True)
    message_font = load_font(10)
    cta_font = load_font(10, bold=True)

    draw.text((60, 60), ad.get("brand", ""), fill=white, font=brand_font)
    headline = wrap_text(draw, ad.get("headline", ""), headline_font, 610)
    message = wrap_text(draw, ad.get("message", ""), message_font, 610)
    draw.text((62, 708), headline, fill=dark, font=headline_font, spacing=4)
    draw.text((62, 750), message, fill=gray, font=message_font, spacing=5)

    cta = ad.get("cta", "").upper()
    button = (80, 815, 320, 865)
    draw.rounded_rectangle(button, radius=22, fill=dark)
    draw.text(((button[0] + button[2]) // 2, (button[1] + button[3]) // 2),
               cta, fill=white, font=cta_font, anchor="mm")

    base.save(output_path, quality=95)


def run_demo() -> None:
    """Build three final ads from included realistic visual samples."""
    log = []
    for number, text_path in ADS.items():
        ad = read_advertisement(text_path)
        visual = ROOT / f"ad{number}_generated_visual.png"
        output = ROOT / f"final_ad_{number}.png"
        compose_ad(visual, ad, output)
        log.append({
            "ad": number,
            "text": text_path.name,
            "template": TEMPLATE.name,
            "visual": visual.name,
            "output": output.name,
            "mode": "demo",
            "status": "success",
        })
    (ROOT / "generation_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")


def run_live() -> None:
    """Run Qwen3 -> Llama 3.2 -> FLUX -> Pillow for all three ads."""
    log = []
    for number, text_path in ADS.items():
        ad = read_advertisement(text_path)
        brief = create_creative_brief(ad)
        prompt = create_image_prompt(brief)
        visual = ROOT / f"ad{number}_live_visual.png"
        output = ROOT / f"final_ad_{number}.png"
        generate_flux_image(prompt, visual)
        compose_ad(visual, ad, output)
        log.append({
            "ad": number,
            "models": ["Qwen3 4B", "Llama 3.2 3B", "FLUX.1-schnell"],
            "creative_brief": brief,
            "image_prompt": prompt,
            "template": TEMPLATE.name,
            "output": output.name,
            "mode": "live",
            "status": "success",
        })
    (ROOT / "generation_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")


def main() -> None:
    """Parse arguments and execute demo or live mode."""
    parser = argparse.ArgumentParser(description="HPPCS[03] Advertisement Creator")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--demo", action="store_true", help="Run without AI model downloads.")
    group.add_argument("--live", action="store_true", help="Run the full Qwen3/Llama/FLUX pipeline.")
    args = parser.parse_args()
    if args.live:
        run_live()
    else:
        run_demo()
    print("Advertisement generation completed.")


if __name__ == "__main__":
    main()
