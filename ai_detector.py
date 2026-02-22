from __future__ import annotations

import io
from pathlib import Path
from typing import Union

import cairosvg
from PIL import Image
from huggingface_hub import InferenceClient


MODEL_ID = "Ateeqq/ai-vs-human-image-detector"


def _load_as_png_bytes(path: Union[str, Path]) -> bytes:
    """
    Load a PNG/JPG/JPEG/WebP or SVG from disk and return PNG bytes (RGB).
    SVGs are rasterized to 512x512 with a white background.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    ext = p.suffix.lower()

    # SVG -> rasterize to 512x512, white background
    if ext == ".svg":
        svg_bytes = p.read_bytes()
        png_bytes = cairosvg.svg2png(
            bytestring=svg_bytes,
            output_width=512,
            output_height=512,
            background_color="white",
        )
        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    else:
        # Raster image -> open normally
        img = Image.open(p).convert("RGB")

    # Encode as PNG bytes for HF
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def check_if_ai(image_path: Union[str, Path]) -> int:
    """
    Returns an integer score 0-100 representing confidence the image is AI-generated.
    Score = round(prob_ai * 100).
    """
    png_bytes = _load_as_png_bytes(image_path)

    # No token: uses public serverless inference (may rate-limit sometimes).
    client = InferenceClient(model=MODEL_ID)

    # Returns list of {label, score} entries. :contentReference[oaicite:1]{index=1}
    results = client.image_classification(image=png_bytes)

    # Prefer explicit 'ai' label (model card shows 'ai' vs 'hum'). :contentReference[oaicite:2]{index=2}
    prob_ai = None
    for r in results:
        label = str(getattr(r, "label", "")).lower()
        if label == "ai":
            prob_ai = float(getattr(r, "score"))
            break

    # Fallback: if labels differ, treat "not human" as AI
    if prob_ai is None:
        best = max(results, key=lambda x: float(getattr(x, "score")))
        best_label = str(getattr(best, "label", "")).lower()
        best_score = float(getattr(best, "score"))
        if best_label in ("hum", "human"):
            prob_ai = 1.0 - best_score
        else:
            prob_ai = best_score

    score_0_100 = int(round(prob_ai * 100))
    # clamp just in case of tiny float weirdness
    return max(0, min(100, score_0_100))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python ai_detector.py <path_to_png_or_svg>")
        raise SystemExit(1)

    print(check_if_ai(sys.argv[1]))