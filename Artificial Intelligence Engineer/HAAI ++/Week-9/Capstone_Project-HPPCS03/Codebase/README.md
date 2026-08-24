# HPPCS[03] Advertisement Creator using Image Generation

## Overview

This project converts three advertisement text inputs into three final
advertisements using two LLMs, an image-generation model and deterministic
Python composition.

### AI pipeline

1. **Qwen3 8B** – converts advertisement text into a structured creative brief.
2. **Llama 3.2 3B** – converts the brief into a photorealistic image prompt.
3. **FLUX.1-schnell** – generates the realistic product/lifestyle visual.
4. **Pillow** – inserts the visual into the single advertisement template and
   renders the exact headline, message and CTA.

## Inputs

- `ad_text_1.txt`
- `ad_text_2.txt`
- `ad_text_3.txt`
- `ad_template.png` – one actual advertisement template reused for all three ads.

## Outputs

- `final_ad_1.png`
- `final_ad_2.png`
- `final_ad_3.png`

## Demo mode

Demo mode does not download or run the large image-generation model. It uses
the included realistic generated visual samples and demonstrates the complete
composition workflow.

```bash
python main.py --demo
```

## Live mode

For the complete AI pipeline:

```bash
python main.py --live
```

The recommended environment is Google Colab with a GPU. The final submitted
source remains `main.py`.

## Design decision

FLUX is used only to generate the visual. It is explicitly instructed not to
create advertising text, logos, headlines or CTAs. Pillow renders the exact
copy supplied in the input files. This prevents common image-generation text
errors and keeps the final advertisement deterministic.
