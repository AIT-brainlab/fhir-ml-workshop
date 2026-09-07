"""
Swap the AIT template's campus photography for the workshop's own artefacts.

The template's logo and icon PNGs are left alone; only the large photographs
are repointed at figures produced by the code the students run.

Each replacement gets its own new image part, so photographs the template
reused across two slides can be given two different figures.
"""

from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
DECK = HERE / "from-fhir-to-a-table.pptx"
IMG = Path("/tmp/imgs")                    # written by make_figures.py

NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R_EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"

# (slide number in the finished deck, media file currently used) -> new figure
SWAP = {
    (1, "image1.jpeg"): "cover.png",
    (2, "image3.jpeg"): "steps_tall.png",
    (3, "image51.jpeg"): "pca_strip.png",
    (4, "image1.jpeg"): "cover.png",
    (5, "image3.jpeg"): "uv_tall.png",
    (6, "image54.png"): "fhir_json.png",
    (7, "image6.jpeg"): "flatten.png",
    (8, "image14.jpeg"): "terminal.png",
    (9, "image13.jpeg"): "balance_wide.png",
    (9, "image42.jpeg"): "feature_hist.png",
    (10, "image21.jpeg"): "balance_tall.png",
    (11, "image11.jpeg"): "roc.png",
    (12, "image5.jpeg"): "confusion.png",
    (13, "image5.jpeg"): "api_card.png",
    (14, "image45.jpeg"): "limit_missing.png",
    (14, "image46.jpeg"): "limit_demog.png",
    (14, "image14.jpeg"): "limit_label.png",
    (15, "image12.jpeg"): "closing.png",
}


def blips(element):
    return element.findall(f".//{NS_A}blip")


def clear_crop(blip):
    """Remove srcRect so the new figure is not cropped to the old photo's frame."""
    fill = blip.getparent()
    for sr in fill.findall(f"{NS_A}srcRect"):
        fill.remove(sr)
    # stretch/fillRect is the default and is what we want
    for st in fill.findall(f"{NS_A}stretch"):
        for fr in st.findall(f"{NS_A}fillRect"):
            st.remove(fr)


def main() -> None:
    prs = Presentation(DECK)
    done, missed = [], []

    for idx, slide in enumerate(prs.slides, 1):
        seen = {}
        for b in blips(slide._element):
            rid = b.get(R_EMBED)
            if rid is None:
                continue
            try:
                part = slide.part.related_part(rid)
            except KeyError:
                continue
            media = str(part.partname).split("/")[-1]
            key = (idx, media)
            if key not in SWAP:
                continue

            new_file = IMG / SWAP[key]
            if not new_file.exists():
                missed.append(f"slide {idx}: {new_file.name} not generated")
                continue

            if key in seen:              # same photo twice on one slide
                new_rid = seen[key]
            else:
                _, new_rid = slide.part.get_or_add_image_part(str(new_file))
                seen[key] = new_rid
                done.append(f"slide {idx:2}  {media:14} -> {new_file.name}")

            b.set(R_EMBED, new_rid)
            clear_crop(b)

    prs.save(DECK)
    print("\n".join(done))
    if missed:
        print("\nMISSED:")
        print("\n".join(missed))
    print(f"\n{len(done)} images replaced")


if __name__ == "__main__":
    main()
