"""
Photograph the running Streamlit app for the deck.

    uv run --with playwright python slides/capture_app.py
    # first time only, to fetch the browser:
    #   uv run --with playwright playwright install chromium

Starts the real app, drives it through the moves slides 20-23 ask the room to
make, and writes three 16:9 images into slides/figures/:

    app_full.png        the whole screen with a real malignant patient loaded
    app_threshold.png   the sidebar cost panel at threshold 0.20 and at 0.80
    app_fhir.png        the FHIR RiskAssessment after pressing "Send to record"

The point of doing it this way rather than pasting a screenshot: if the app
changes, the picture on the slide changes with it. Nothing on a slide should be
a photograph of something that used to be true.

playwright is not a workshop dependency — students never run this.
"""

import re
import socket
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "figures"
PORT = 8791
PAPER = (255, 255, 255)
INK = (22, 33, 26)
MUTED = (92, 107, 98)


def free_port(port: int) -> bool:
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def pad_to(img: Image.Image, ratio: float = 16 / 9) -> Image.Image:
    """Letterbox onto a white canvas rather than crop content away."""
    w, h = img.size
    if w / h > ratio:
        canvas = Image.new("RGB", (w, round(w / ratio)), PAPER)
    else:
        canvas = Image.new("RGB", (round(h * ratio), h), PAPER)
    canvas.paste(img, ((canvas.width - w) // 2, (canvas.height - h) // 2))
    return canvas


def trim(img: Image.Image, keep_left: int = 0) -> Image.Image:
    """Drop the empty white margin Streamlit leaves at the bottom and right."""
    grey = img.convert("L")
    bbox = grey.point(lambda v: 255 if v < 246 else 0).getbbox()
    if bbox is None:
        return img
    l, t, r, b = bbox
    return img.crop((min(l, keep_left), max(t - 12, 0),
                     min(r + 24, img.width), min(b + 24, img.height)))


def slider_value(widget) -> float:
    return float([x for x in widget.inner_text().split("\n") if x.strip()][1])


def set_slider(page, index: int, target: float) -> str:
    w = page.locator('[data-testid="stSlider"]').nth(index)
    box = w.bounding_box()
    page.mouse.click(box["x"] + box["width"] * 0.5, box["y"] + box["height"] * 0.62)
    page.wait_for_timeout(2000)
    for _ in range(40):
        cur = slider_value(page.locator('[data-testid="stSlider"]').nth(index))
        if abs(cur - target) < 1e-9:
            break
        page.keyboard.press("ArrowRight" if cur < target else "ArrowLeft")
        page.wait_for_timeout(1200)
    return f"{slider_value(page.locator('[data-testid=stSlider]').nth(index)):.2f}"


def cost_panel(page, threshold: float, path: Path) -> str:
    """Clip the sidebar from the threshold heading down past the three costs."""
    set_slider(page, 0, threshold)
    page.wait_for_timeout(1500)
    top = page.get_by_text("Decision threshold", exact=True).bounding_box()
    bottom = page.get_by_text("healthy patient", exact=False).last.bounding_box()
    page.screenshot(path=str(path), clip={
        "x": top["x"] - 18, "y": top["y"] - 14,
        "width": 330,
        "height": (bottom["y"] + bottom["height"] + 18) - (top["y"] - 14),
    })
    body = page.inner_text("body")
    return " · ".join(re.findall(r"(?:miss|falsely alarm) \d+ \w+ ?\w*", body)[:2])


def compose_pair(a: Path, b: Path, out: Path) -> None:
    """Two cost panels, side by side, on one 16:9 card."""
    from PIL import ImageDraw, ImageFont

    def font(size, bold=False):
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        try:
            return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
        except OSError:
            return ImageFont.load_default()

    left, right = Image.open(a), Image.open(b)
    h = max(left.height, right.height)
    gap, pad, head = 70, 46, 62
    card = Image.new("RGB", (left.width + right.width + gap + pad * 2,
                             h + head + pad * 2), PAPER)
    d = ImageDraw.Draw(card)
    for img, x, label in ((left, pad, "threshold  0.20"),
                          (right, pad + left.width + gap, "threshold  0.80")):
        d.text((x, pad), label, font=font(30, bold=True), fill=INK)
        card.paste(img, (x, pad + head))
    d.text((pad, card.height - pad + 6), "same model, same weights - only the line moved",
           font=font(24), fill=MUTED)
    pad_to(card).save(out)


def main() -> None:
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    if not (ROOT / "models" / "model.joblib").exists():
        raise SystemExit("Run scripts/03_train_model.py first — the app needs a model.")
    if not free_port(PORT):
        raise SystemExit(f"port {PORT} is busy")

    app = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app/streamlit_app.py",
         "--server.headless", "true", "--server.port", str(PORT)],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            if not free_port(PORT):
                break
            time.sleep(1)
        time.sleep(6)

        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--no-sandbox"])
            # a 16:9 viewport so the screenshot fills the slide's frame exactly,
            # with no white letterboxing eating the space the room has to read
            page = browser.new_page(viewport={"width": 1776, "height": 999},
                                    device_scale_factor=1.9)
            page.goto(f"http://localhost:{PORT}", wait_until="load", timeout=90_000)
            page.wait_for_timeout(9_000)

            page.get_by_text("Patient with a malignant tumour").click()
            page.wait_for_timeout(5_000)

            shot = OUT / "_app_raw.png"
            page.screenshot(path=str(shot))          # viewport only: already 16:9
            pad_to(Image.open(shot)).save(OUT / "app_full.png")
            band = re.search(r"RISK BAND\s*\n\s*(\w+)", page.inner_text("body"))
            print("  app_full.png       real patient loaded, risk band",
                  band.group(1) if band else "?")

            lo, hi = OUT / "_cost_lo.png", OUT / "_cost_hi.png"
            print("  threshold 0.20    ", cost_panel(page, 0.20, lo))
            print("  threshold 0.80    ", cost_panel(page, 0.80, hi))
            compose_pair(lo, hi, OUT / "app_threshold.png")
            print("  app_threshold.png ", Image.open(OUT / "app_threshold.png").size)

            # slide 23: the result written back as FHIR. Scroll the section to
            # the top of the viewport so the fields worth reading are the ones
            # on the slide, rather than whatever happened to be in shot.
            set_slider(page, 0, 0.50)
            page.get_by_role("button", name="Send to record").click()
            page.wait_for_timeout(6_000)
            heading = page.get_by_text(
                "Send this result back to the hospital record").bounding_box()
            page.mouse.wheel(0, heading["y"] - 40)
            page.wait_for_timeout(2_500)
            page.screenshot(path=str(OUT / "app_fhir.png"))
            body = page.inner_text("body")
            print("  app_fhir.png       RiskAssessment shown:",
                  '"RiskAssessment"' in body,
                  "| performer is a Device:", "#breast-mass-risk-model" in body)

            browser.close()
        for tmp in (OUT / "_app_raw.png", OUT / "_cost_lo.png", OUT / "_cost_hi.png"):
            tmp.unlink(missing_ok=True)
    finally:
        app.terminate()
        app.wait(timeout=20)


if __name__ == "__main__":
    main()
