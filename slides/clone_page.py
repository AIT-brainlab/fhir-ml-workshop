"""
Duplicate a page that is already in the deck, and slot the copy in elsewhere.

    python3 slides/clone_page.py --page 13 --after 13

Used for the slides written after the Canva export was thrown away: rather than
inventing a layout, take one the designer already made, put it where it is
needed, and rewrite its text with apply_results.py.

Unlike add_page.py this stays inside one file, so image parts are shared rather
than copied — nothing is duplicated in the zip and the deck does not grow.

Needs python-pptx, which is not a workshop dependency: pip install python-pptx
"""

import argparse
import copy
from pathlib import Path

from pptx import Presentation

R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL_ATTRS = (f"{R_NS}embed", f"{R_NS}link", f"{R_NS}id")
P_NS = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

HERE = Path(__file__).resolve().parent
DECK = HERE / "from-fhir-to-a-table.pptx"


def clone_page(prs, index: int):
    """Append a copy of slide `index` (0-based) and return the new slide."""
    src = prs.slides[index]
    dst = prs.slides.add_slide(src.slide_layout)

    for shape in list(dst.shapes):          # the layout's placeholders
        shape._element.getparent().remove(shape._element)

    remap = {}
    for rid, rel in src.part.rels.items():
        if rel.reltype.endswith("/slideLayout"):
            continue
        if rel.is_external:
            remap[rid] = dst.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
        else:
            # same package, so the copy can point at the very same part
            remap[rid] = dst.part.relate_to(rel.target_part, rel.reltype)

    tree = dst.shapes._spTree
    for shape in src.shapes:
        el = copy.deepcopy(shape._element)
        for node in el.iter():
            for attr in REL_ATTRS:
                old = node.get(attr)
                if old in remap:
                    node.set(attr, remap[old])
        tree.append(el)

    bg = src._element.find(f"{P_NS}cSld/{P_NS}bg")
    if bg is not None:
        dst._element.find(f"{P_NS}cSld").insert(0, copy.deepcopy(bg))

    return dst


def move_to(prs, from_index: int, to_index: int) -> None:
    lst = prs.slides._sldIdLst
    ids = list(lst)
    sid = ids[from_index]
    lst.remove(sid)
    lst.insert(to_index, sid)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--page", type=int, required=True,
                    help="1-based page to copy")
    ap.add_argument("--after", type=int, required=True,
                    help="1-based page the copy should follow")
    ap.add_argument("--deck", default=str(DECK))
    args = ap.parse_args()

    prs = Presentation(args.deck)
    before = len(prs.slides._sldIdLst)
    clone_page(prs, args.page - 1)
    move_to(prs, before, args.after)
    prs.save(args.deck)
    print(f"page {args.page} copied to position {args.after + 1}; deck now has "
          f"{len(Presentation(args.deck).slides._sldIdLst)} pages")


if __name__ == "__main__":
    main()
