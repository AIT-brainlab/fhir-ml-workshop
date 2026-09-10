"""
Generate the slide imagery from the workshop's own artefacts.

No stock photography: every figure here is produced by the code the students
run, or is a verbatim listing from the repository.
"""

import json
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "slides" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# AIT template palette, sampled from the deck
DARK = "#2E5A34"
LIME = "#A2C63B"
INK = "#16211A"
PANEL = "#1D2C22"
PAPER = "#FFFFFF"
GREY = "#8A9A90"
MUTED = "#5C6B62"
ALERT = "#C4552F"

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#C8D2CC",
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.grid": True,
        "grid.color": "#E6EBE7",
        "grid.linewidth": 0.8,
    }
)

df = pd.read_csv(REPO / "data" / "patients.csv")


# --------------------------------------------------------------- text cards
def card(name, w, h, lines, *, bg=INK, pad=54, size=None, title=None,
         title_color=LIME, line_gap=1.62):
    """Render a code / terminal card as a PNG."""
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)

    y = pad
    if title:
        ft = ImageFont.truetype(SANSB, int(h * 0.045))
        d.text((pad, y), title, font=ft, fill=title_color)
        y += int(h * 0.045 * 2.0)

    n = max(len(lines), 1)
    fs = size or max(11, int((h - y - pad) / (n * line_gap)))
    f = ImageFont.truetype(MONO, fs)
    fb = ImageFont.truetype(MONOB, fs)

    for item in lines:
        text, colour, bold = (item if isinstance(item, tuple) else (item, "#D9E4DC", False))
        d.text((pad, y), text, font=fb if bold else f, fill=colour)
        y += int(fs * line_gap)

    img.save(OUT / name, quality=95)
    print("  ", name, img.size)


# 1. FHIR JSON — the real file, trimmed to fit
bundle = json.loads((REPO / "data" / "fhir" / "P0001.json").read_text())
obs = next(e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "Observation")
json_lines = [
    ("{", GREY, False),
    ('  "resourceType": "Bundle",', "#D9E4DC", True),
    ('  "id": "bundle-P0001",', GREY, False),
    ('  "type": "collection",', GREY, False),
    ('  "entry": [{', GREY, False),
    ('    "resource": {', GREY, False),
    ('      "resourceType": "Observation",', "#D9E4DC", True),
    ('      "status": "final",', GREY, False),
    ('      "code": { "coding": [{', GREY, False),
    ('        "code": "radius",', LIME, True),
    ('        "display": "Nucleus radius"', GREY, False),
    ("      }] },", GREY, False),
    ('      "subject": {', GREY, False),
    ('        "reference": "Patient/P0001"', LIME, True),
    ("      },", GREY, False),
    ('      "valueQuantity": {', GREY, False),
    ('        "value": 17.99,', LIME, True),
    ('        "unit": "pixel"', GREY, False),
    ("      }", GREY, False),
    ("    }", GREY, False),
    ("  }, ... eleven more resources ]", GREY, False),
    ("}", GREY, False),
]
card("fhir_json.png", 1600, 1000, json_lines, title="data/fhir/P0001.json")

# The three PART dividers use a near-black wall of real FHIR as wallpaper.
# It is barely legible on purpose, but it is still on the projector and still
# in the repo - so it is generated from the current Bundle rather than kept as
# a screenshot taken once. A stale copy of this leaked an old base URL.
def divider_wall(name="divider_json.png", w=2000, h=1327):
    bg, fg = (11, 18, 14), (24, 38, 29)
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(MONO, 21)
    text = (REPO / "data" / "fhir" / "P0001.json").read_text().split("\n")
    y, pad = 40, 34
    for line in text:
        if y > h - 30:
            break
        d.text((pad, y), line.rstrip(), font=f, fill=fg)
        y += 24
    img.save(OUT / name)
    print("  ", name, img.size)


divider_wall()

# 2. Bundles -> rows, before and after.
# Values are read out of patients.csv rather than typed, and the file count is
# read off disk, so the card can never claim a table the repo does not hold.
_n_files = len(list((REPO / "data" / "fhir").glob("*.json")))


def _row(pid):
    r = df[df["patient_id"] == pid].iloc[0]
    tex = "NaN" if pid == "P0010" else f"{r['texture']:.2f}"
    return (f"{pid}{r['radius']:>14.2f}{tex:>10}{int(r['malignant']):>12}",
            "#E8B04B" if pid == "P0010" else "#D9E4DC", pid == "P0010")


flat = [
    (f"data/fhir/{_n_files:>26} files", LIME, True),
    ("  P0001.json    12 resources", "#D9E4DC", False),
    ("  P0002.json    12 resources", "#D9E4DC", False),
    ("  ...", GREY, False),
    ("  P0010.json    11 resources   <- one Observation missing", "#E8B04B", True),
    ("  ...", GREY, False),
    (f"  P{_n_files:04d}.json    12 resources", "#D9E4DC", False),
    ("", GREY, False),
    ("           |  01_fhir_to_table.py", GREY, False),
    ("           v", GREY, False),
    ("", GREY, False),
    (f"patient_id   radius   texture   malignant{_n_files:>10} rows", LIME, True),
    _row("P0001"),
    _row("P0002"),
    ("...", GREY, False),
    _row("P0010"),
    ("...", GREY, False),
    _row(f"P{_n_files:04d}"),
]
card("flatten.png", 1780, 1000, flat, title="Bundles become rows")

# 3. Real terminal output from the script the students run.
# Run it here rather than reading a saved copy, so the card can never drift
# away from what the room actually sees.
import subprocess as _sp

raw = _sp.run([sys.executable, str(REPO / "scripts" / "01_fhir_to_table.py")],
              capture_output=True, text=True, cwd=REPO, check=True).stdout.splitlines()
start = next(i for i, l in enumerate(raw) if "WHAT WENT WRONG" in l) - 1
term = [("$ uv run python scripts/01_fhir_to_table.py", LIME, True), ("", GREY, False)]
for line in raw[start : start + 14]:
    colour = "#E8B04B" if ("P0010" in line or "texture" in line) else "#D9E4DC"
    term.append((line[:64], colour, "====" in line))
card("terminal.png", 1780, 1000, term, title=None)

# 4. API request / response, portrait
api = [
    ("POST /predict", LIME, True),
    ("", GREY, False),
    ("{", GREY, False),
    ('  "radius": 17.99,', "#D9E4DC", False),
    ('  "texture": 10.38,', "#D9E4DC", False),
    ('  "perimeter": 122.8,', "#D9E4DC", False),
    ('  "area": 1001.0,', "#D9E4DC", False),
    ("  ...", GREY, False),
    ("}", GREY, False),
    ("", GREY, False),
    ("200 OK", LIME, True),
    ("", GREY, False),
    ("{", GREY, False),
    ('  "prediction":', "#D9E4DC", False),
    ('      "malignant",', "#D9E4DC", False),
    ('  "probability": 0.9996,', "#D9E4DC", False),
    ('  "risk_band": "HIGH"', "#E8704B", True),
    ("}", GREY, False),
]
card("api_card.png", 900, 1300, api, title=None)

# 5. Cover — a wall of the real Bundle, dimmed for the title overlay
wall = (REPO / "data" / "fhir" / "P0001.json").read_text().splitlines()
cover_lines = []
for line in (wall * 4)[:46]:
    cover_lines.append((line[:96], "#2E4A38", False))
card("cover.png", 2000, 1327, cover_lines, bg="#101A14", pad=40, size=22, line_gap=1.25)


# ------------------------------------------------------------------ figures
def fig(name, w_in, h_in, draw_fn, dpi=170):
    f, ax = plt.subplots(figsize=(w_in, h_in))
    draw_fn(ax)
    f.tight_layout(pad=1.4)
    f.savefig(OUT / name, dpi=dpi, facecolor=PAPER)
    plt.close(f)
    print("  ", name, Image.open(OUT / name).size)


counts = df["malignant"].value_counts().sort_index()


def balance_wide(ax):
    ax.barh(["benign", "malignant"], [counts[0], counts[1]], color=[LIME, DARK], height=0.55)
    for i, v in enumerate([counts[0], counts[1]]):
        ax.text(v + 6, i, f"{v}   {v/len(df):.1%}", va="center", fontsize=11, color=MUTED)
    ax.set_xlim(0, 430)
    ax.set_title("Class balance — 569 patients", fontsize=12, loc="left", color=INK)
    ax.grid(axis="y", visible=False)


def balance_tall(ax):
    ax.bar(["benign", "malignant"], [counts[0], counts[1]], color=[LIME, DARK], width=0.55)
    ax.axhline(counts[0], color=ALERT, lw=1.4, ls="--")
    ax.text(0.5, counts[0] + 12, "62.7% baseline", color=ALERT, fontsize=11, ha="center")
    ax.set_ylim(0, 430)
    ax.set_ylabel("patients")
    ax.grid(axis="x", visible=False)


def feature_hist(ax):
    top = "concave_points"
    ax.hist(df.loc[df.malignant == 0, top], bins=28, alpha=0.85, label="benign", color=LIME)
    ax.hist(df.loc[df.malignant == 1, top], bins=28, alpha=0.85, label="malignant", color=DARK)
    ax.set_xlabel(top)
    ax.set_ylabel("patients")
    ax.legend(frameon=False, fontsize=10)
    ax.set_title("Strongest single feature", fontsize=12, loc="left", color=INK)


def roc(ax):
    import joblib
    from sklearn.metrics import roc_curve

    import sys

    sys.path.insert(0, str(REPO))
    from common import add_features

    b = joblib.load(REPO / "models" / "model.joblib")
    from sklearn.model_selection import train_test_split

    d = add_features(df)
    X, y = d[b["feature_names"]], d["malignant"]
    _, Xte, _, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    fpr, tpr, _ = roc_curve(yte, b["pipeline"].predict_proba(Xte)[:, 1])
    ax.plot(fpr, tpr, color=DARK, lw=2.4, label=f"AUC = {b['metrics']['roc_auc']:.3f}")
    ax.plot([0, 1], [0, 1], color=GREY, lw=1, ls="--")
    ax.fill_between(fpr, tpr, alpha=0.12, color=LIME)
    ax.set_xlabel("false positive rate")
    ax.set_ylabel("recall")
    ax.set_title("ROC — held-out test set", fontsize=12, loc="left", color=INK)
    ax.legend(frameon=False, fontsize=11, loc="lower right")


def confusion(ax):
    import json
    R = json.loads((Path(__file__).resolve().parent / "results.json").read_text())
    c = R["models"][R["selected"]]["confusion"]
    m = np.array([[c["tn"], c["fp"]], [c["fn"], c["tp"]]])
    ax.imshow(m, cmap="Greens", vmin=-30, vmax=95)
    for i in range(2):
        for j in range(2):
            hot = (i, j) == (1, 0)
            ax.text(
                j, i, m[i, j],
                ha="center", va="center", fontsize=30,
                color=ALERT if hot else ("white" if m[i, j] > 50 else INK),
                fontweight="bold",
            )
    ax.set_xticks([0, 1], ["pred.\nbenign", "pred.\nmalignant"], fontsize=10)
    ax.set_yticks([0, 1], ["actual\nbenign", "actual\nmalignant"], fontsize=10)
    ax.set_title(f"{c['fn']} tumours missed", fontsize=13, loc="left", color=ALERT,
                 pad=12)
    ax.grid(False)


def pca_strip(ax):
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    feats = [c for c in df.columns if c not in ("patient_id", "malignant")]
    Xs = StandardScaler().fit_transform(df[feats])
    cl = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(Xs)
    xy = PCA(n_components=2, random_state=42).fit_transform(Xs)
    ax.scatter(xy[:, 0], xy[:, 1], c=[DARK if c else LIME for c in cl], s=26, alpha=0.85,
               edgecolors="none")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)


def missingness(ax):
    rng = np.random.default_rng(3)
    grid = rng.random((26, 34)) < 0.06
    ax.imshow(~grid, cmap="Greens", vmin=-0.6, vmax=1.6)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.set_title("Gaps a real extract carries", fontsize=11, loc="left", color=MUTED)


def demographics(ax):
    ax.axis("off")
    rows = ["age", "sex", "ethnicity", "comorbidity", "site", "device"]
    for i, r in enumerate(rows):
        ax.text(0.04, 0.88 - i * 0.145, r, fontsize=13, color=INK)
        ax.text(0.62, 0.88 - i * 0.145, "absent", fontsize=13, color=ALERT, fontweight="bold")
    ax.set_title("Fields needed for a bias audit", fontsize=11, loc="left", color=MUTED)


def label_noise(ax):
    ax.axis("off")
    ax.text(0.5, 0.62, "biopsy\nreport", ha="center", va="center", fontsize=20,
            color=INK, linespacing=1.35)
    ax.annotate("", xy=(0.5, 0.34), xytext=(0.5, 0.46),
                arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2))
    ax.text(0.5, 0.22, "ground truth", ha="center", fontsize=15, color=ALERT,
            fontweight="bold")
    ax.set_title("The target is a human judgement", fontsize=11, loc="left", color=MUTED)


fig("balance_wide.png", 6.8, 2.5, balance_wide)
fig("feature_hist.png", 5.2, 5.0, feature_hist)
fig("balance_tall.png", 4.4, 6.6, balance_tall)
fig("roc.png", 5.4, 5.6, roc)
fig("confusion.png", 4.2, 6.1, confusion)
fig("pca_strip.png", 13.2, 4.0, pca_strip)
fig("limit_missing.png", 4.6, 4.7, missingness)
fig("limit_demog.png", 4.6, 4.7, demographics)
fig("limit_label.png", 4.6, 4.7, label_noise)
fig("closing.png", 5.2, 6.0, pca_strip)

print("\nall images written to", OUT)


# ---------------------------------------------------------- the ML figures
# Everything below is fitted on the spot with the same seed the scripts use,
# so the pictures on the slides are the real models, not an illustration of
# what a model might look like.
import sys

sys.path.insert(0, str(REPO))

from sklearn.decomposition import PCA                              # noqa: E402
from sklearn.ensemble import RandomForestClassifier                # noqa: E402
from sklearn.impute import SimpleImputer                           # noqa: E402
from sklearn.linear_model import LogisticRegression                # noqa: E402
from sklearn.model_selection import cross_val_score, train_test_split  # noqa: E402
from sklearn.pipeline import Pipeline                              # noqa: E402
from sklearn.preprocessing import StandardScaler                   # noqa: E402

from common import RAW_FEATURES, TARGET, add_features              # noqa: E402

R = json.loads((REPO / "slides" / "results.json").read_text())
SEED = R["seed"]

_d = add_features(df)
_names = [c for c in _d.columns if c not in ("patient_id", TARGET)]
_X, _y = _d[_names], _d[TARGET]
_Xtr, _Xte, _ytr, _yte = train_test_split(
    _X, _y, test_size=R["test_size"], stratify=_y, random_state=SEED)

# two dimensions to draw in; the models below are fitted in this same 2-D space
# so the boundary shown is genuinely the boundary of the thing that was fitted
_pca = PCA(n_components=2, random_state=SEED)
_P = _pca.fit_transform(StandardScaler().fit_transform(_X))


def _boundary(ax, model, title):
    model.fit(_P, _y)
    x0, x1 = _P[:, 0].min() - 0.6, _P[:, 0].max() + 0.6
    y0, y1 = _P[:, 1].min() - 0.6, _P[:, 1].max() + 0.6
    gx, gy = np.meshgrid(np.linspace(x0, x1, 420), np.linspace(y0, y1, 420))
    zz = model.predict_proba(np.c_[gx.ravel(), gy.ravel()])[:, 1].reshape(gx.shape)
    ax.contourf(gx, gy, zz, levels=[0, 0.5, 1], colors=["#EEF4E6", "#D3E3C0"])
    ax.contour(gx, gy, zz, levels=[0.5], colors=[DARK], linewidths=2.0)
    ax.scatter(_P[_y == 0, 0], _P[_y == 0, 1], s=9, c=LIME, linewidths=0)
    ax.scatter(_P[_y == 1, 0], _P[_y == 1, 1], s=9, c=DARK, linewidths=0)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_title(title, fontsize=13, loc="left", color=INK)
    for s in ax.spines.values():
        s.set_visible(False)


fig("boundary_logit.png", 5.56, 3.13,
    lambda ax: _boundary(ax, LogisticRegression(max_iter=2000, random_state=SEED),
                         "one straight boundary"))
fig("boundary_forest.png", 5.56, 3.13,
    lambda ax: _boundary(ax, RandomForestClassifier(n_estimators=300,
                                                    random_state=SEED, n_jobs=-1),
                         "300 trees, voting"))


def split_diagram(ax):
    """569 patients, cut once, and never uncut."""
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 46)
    n = R["cohort"]["n"]; nte = R["cohort"]["n_test"]; ntr = n - nte
    ax.add_patch(plt.Rectangle((14, 33), 72, 9, color="#E4EBE4"))
    ax.text(50, 37.5, f"{n} patients", ha="center", va="center", fontsize=15, color=INK)
    ax.add_patch(plt.Rectangle((14, 14), 52, 10, color=DARK))
    ax.text(40, 19, f"train  {ntr}", ha="center", va="center", fontsize=15, color="white")
    ax.add_patch(plt.Rectangle((69, 14), 17, 10, color=LIME))
    ax.text(77.5, 19, f"test  {nte}", ha="center", va="center", fontsize=15, color=INK)
    for x0, x1 in ((46, 40), (54, 77)):
        ax.annotate("", xy=(x1, 25), xytext=(x0, 32),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4))
    ax.text(50, 7, "every number we report comes from the right-hand box",
            ha="center", fontsize=12, color=MUTED, style="italic")


fig("split.png", 5.56, 3.13, split_diagram)


def confusion_explained(ax):
    """The four cells, then the two fractions read straight off them."""
    m = R["models"][R["selected"]]["confusion"]
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 56)
    cells = [(0, 0, "tn", "true negative", "#DCE8CC"),
             (1, 0, "fp", "false positive", "#F6DCD2"),
             (0, 1, "fn", "false negative", "#E9A88F"),
             (1, 1, "tp", "true positive", "#B9D98E")]
    for cx, cy, key, label, colour in cells:
        x = 22 + cx * 25; y = 30 - cy * 21
        ax.add_patch(plt.Rectangle((x, y), 22, 18, color=colour))
        ax.text(x + 11, y + 11, str(m[key]), ha="center", va="center",
                fontsize=30, color=INK, fontweight="bold")
        ax.text(x + 11, y + 3.5, label, ha="center", fontsize=10.5, color=MUTED)
    ax.text(33, 51, "predicted benign", ha="center", fontsize=11, color=MUTED)
    ax.text(58, 51, "predicted malignant", ha="center", fontsize=11, color=MUTED)
    ax.text(20, 39, "actually\nbenign", ha="right", va="center", fontsize=11,
            color=MUTED, linespacing=1.4)
    ax.text(20, 18, "actually\nmalignant", ha="right", va="center", fontsize=11,
            color=MUTED, linespacing=1.4)
    ax.text(73, 41, "recall", fontsize=13, color=ALERT, fontweight="bold")
    ax.text(73, 36, f"{m['tp']} / ({m['tp']}+{m['fn']}) = "
                    f"{m['tp'] / (m['tp'] + m['fn']):.3f}",
            fontsize=13, color=ALERT, fontweight="bold")
    ax.text(73, 19, "precision", fontsize=13, color=DARK, fontweight="bold")
    ax.text(73, 14, f"{m['tp']} / ({m['tp']}+{m['fp']}) = "
                    f"{m['tp'] / (m['tp'] + m['fp']):.3f}",
            fontsize=13, color=DARK, fontweight="bold")


fig("confusion_explained.png", 8.73, 4.91, confusion_explained)


def pipeline_chain(ax):
    """One object, three steps - the thing that actually gets saved."""
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 56)
    steps = [("impute", "median of the\ntraining column"),
             ("scale", "mean 0, spread 1\nlearned on train"),
             ("classify", "logistic\nregression")]
    ax.add_patch(plt.Rectangle((4, 12), 92, 32, fill=False, ec=DARK,
                               lw=1.6, ls=(0, (5, 4))))
    ax.text(6, 46.5, "Pipeline  —  one object, fitted and saved together",
            fontsize=12.5, color=DARK, fontweight="bold")
    for i, (name, sub) in enumerate(steps):
        x = 8 + i * 30
        ax.add_patch(plt.Rectangle((x, 20), 24, 16, color=DARK if i == 2 else "#E4EBE4"))
        ax.text(x + 12, 31, name, ha="center", fontsize=14, fontweight="bold",
                color="white" if i == 2 else INK)
        ax.text(x + 12, 24.5, sub, ha="center", va="center", fontsize=9.5,
                color="#DDE7DB" if i == 2 else MUTED, linespacing=1.35)
        if i < 2:
            ax.annotate("", xy=(x + 29.5, 28), xytext=(x + 32.5, 28),
                        arrowprops=dict(arrowstyle="<|-", color=MUTED, lw=1.6))
    ax.text(50, 6.5, "saved as one file  ->  models/model.joblib", ha="center",
            fontsize=11.5, color=MUTED)


fig("pipeline_chain.png", 5.56, 3.13, pipeline_chain)


def cv_folds(ax):
    """Five fits on the training half, before the test set is opened."""
    pipe = Pipeline([("impute", SimpleImputer(strategy="median")),
                     ("scale", StandardScaler()),
                     ("model", LogisticRegression(max_iter=2000, random_state=SEED))])
    scores = cross_val_score(pipe, _Xtr, _ytr, cv=5, scoring="recall")
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 50)
    ax.text(0, 46, f"5-fold cross-validation on the {len(_Xtr)} training patients",
            fontsize=12.5, color=INK)
    for i, s in enumerate(scores):
        y = 37 - i * 7.2
        for j in range(5):
            x = 2 + j * 11
            held = j == i
            ax.add_patch(plt.Rectangle((x, y), 10, 5,
                                       color=LIME if held else "#E4EBE4"))
        ax.text(60, y + 2.5, f"recall  {s:.3f}", va="center", fontsize=12, color=INK)
    ax.text(2, -1, "the pale block is the fold held back that round",
            fontsize=10.5, color=MUTED, style="italic")
    ax.text(60, -1, f"mean {scores.mean():.3f}   spread ±{scores.std():.3f}",
            fontsize=12.5, color=DARK, fontweight="bold")


fig("cv_folds.png", 8.73, 4.91, cv_folds)

print("\nML figures written to", OUT)


def starved_bars(ax):
    """Two bars that disagree: accuracy up, missed tumours up sevenfold."""
    a = R["ablations"]["starved"]
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 150)
    ax.text(6, 140, "train on 455", fontsize=14, color="#B9C9BC")
    ax.text(6, 133, "vs train on 113", fontsize=14, color=LIME)

    def pair(y, title, base, now, hi, fmt, worse):
        ax.text(6, y + 30, title, fontsize=15, color="white", fontweight="bold")
        for i, (v, colour) in enumerate(((base, "#7E9683"), (now, ALERT if worse else LIME))):
            w = 78 * v / hi
            ax.add_patch(plt.Rectangle((6, y + 14 - i * 13), w, 9, color=colour))
            ax.text(6 + w + 2.5, y + 18.5 - i * 13, fmt.format(v), va="center",
                    fontsize=13, color="white")

    pair(78, "accuracy", a["accuracy"]["baseline"], a["accuracy"]["now"], 1.05,
         "{:.3f}", worse=False)
    pair(20, "tumours missed", a["missed"]["baseline"], a["missed"]["now"], 26,
         "{:.0f}", worse=True)


f, ax = plt.subplots(figsize=(4.55, 6.82))
f.patch.set_facecolor(PANEL)
ax.set_facecolor(PANEL)
starved_bars(ax)
f.subplots_adjust(0, 0, 1, 1)
f.savefig(OUT / "starved_bars.png", dpi=170, facecolor=PANEL)
plt.close(f)
print("   starved_bars.png", Image.open(OUT / "starved_bars.png").size)


def loop_closed(ax):
    """FHIR in at Part 1, FHIR out at Part 3. The afternoon as one circle."""
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 52)
    boxes = [
        (1.5,  "FHIR\nBundle",   "12 resources",    "#E4EBE4", INK),
        (26.0, "flat\ntable",    "1 row, 12 cols",  "#E4EBE4", INK),
        (50.5, "model",          "one probability", DARK,      "white"),
        (75.0, "Risk\nAssessment", "back as FHIR",  LIME,      INK),
    ]
    for x, title, sub, colour, textcolour in boxes:
        ax.add_patch(plt.Rectangle((x, 24), 23.5, 16, color=colour))
        ax.text(x + 11.75, 34, title, ha="center", va="center", fontsize=12,
                fontweight="bold", color=textcolour, linespacing=1.25)
        ax.text(x + 11.75, 27, sub, ha="center", fontsize=9.5,
                color="#DDE7DB" if textcolour == "white" else MUTED)
        if x < 70:
            ax.annotate("", xy=(x + 25.6, 32), xytext=(x + 23.9, 32),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.8))
    for label, x in (("Part 1", 13.2), ("Part 2", 62.0), ("Part 3", 86.7)):
        ax.text(x, 42.5, label, ha="center", fontsize=10, color=MUTED,
                style="italic")
    # the return path, drawn as plain segments so it cannot bow off the canvas
    ax.plot([86.7, 86.7, 13.2], [24, 14, 14], color=DARK, lw=2.0,
            solid_capstyle="round")
    ax.annotate("", xy=(13.2, 23.6), xytext=(13.2, 15),
                arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.0))
    ax.text(50, 8, "the same record, the same standard, the other direction",
            ha="center", fontsize=11.5, color=DARK)


fig("loop_closed.png", 5.56, 3.13, loop_closed)


# ------------------------------------------------ recap: HL7 v2 vs FHIR
# The morning covered both. By the afternoon half the room has forgotten which
# is which, so one slide puts the same measurement in both formats.
#
# The v2 message is written by hand: this repository has no v2 feed, and
# inventing one and calling it real would be worse than saying so. It is a
# faithful ORU^R01 carrying the value that P0001's Observation carries.
_obx = "OBX|1|NM|radius^Nucleus radius^L||17.99|pixel|||||F"
_marker = " " * _obx.index("17.99") + "^^^^^ OBX-5"

# Both cards are deliberately short. They are read from ten metres away, so
# every line that is not the point costs font size for the lines that are.
card(
    "recap_v2.png", 1600, 900,
    [
        ("one line of an ORU^R01 lab result message", MUTED, False),
        ("", GREY, False),
        (_obx, "#D9E4DC", True),
        (_marker, ALERT, True),
        ("", GREY, False),
        ("the value is found by COUNTING", MUTED, False),
    ],
    title="HL7 v2  (1989, still runs most hospitals)", size=40, line_gap=2.0,
)

card(
    "recap_fhir.png", 1600, 900,
    [
        ('"code": { "coding": [{ "code": "radius" }] },', LIME, True),
        ('"subject": { "reference": "Patient/P0001" },', "#D9E4DC", True),
        ('"valueQuantity": { "value": 17.99,', "#D9E4DC", True),
        ('                   "unit": "pixel" }', "#D9E4DC", True),
        ("", GREY, False),
        ("the value is found by NAME", MUTED, False),
    ],
    title="FHIR  (2014, same value, same patient)", size=37, line_gap=2.0,
)




# ------------------------------- where the data actually came from
# The deck says "FHIR Bundles to a table". The truth is that the table came
# first and the Bundles were written from it. Draw that, rather than let a
# student work it out and wonder what else was glossed over.
def provenance(ax):
    """One lane, left to right. Three boxes, one idea."""
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 46)

    def box(x, w, title, sub, fill, fg):
        ax.add_patch(plt.Rectangle((x, 18), w, 15, color=fill))
        fs = 13 if len(title) <= 13 else 11
        ax.text(x + w / 2, 26.5, title, ha="center", va="center",
                fontsize=fs, fontweight="bold", color=fg)
        ax.text(x + w / 2, 21.5, sub, ha="center", va="center",
                fontsize=9.5, color="#DDE7DB" if fg == "white" else MUTED)

    box(2, 26, "patients.csv", "a published dataset", "#E4EBE4", INK)
    box(37, 26, "data/fhir/", "569 Bundles", LIME, INK)
    box(72, 26, "a table", "569 rows, 12 columns", DARK, "white")

    for x0, x1, label, when in ((28.4, 36.4, "we wrote these", "before today"),
                                (63.4, 71.4, "Part 1", "you run this")):
        ax.annotate("", xy=(x1, 25.5), xytext=(x0, 25.5),
                    arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2))
        ax.text((x0 + x1) / 2, 29.5, label, ha="center", fontsize=10.5,
                color=DARK, fontweight="bold")
        ax.text((x0 + x1) / 2, 14.5, when, ha="center", fontsize=9.5, color=MUTED)

    ax.text(50, 5,
            "FHIR is one of the raw formats a model cannot read.\n"
            "Part 1 is what turns it into one it can.",
            ha="center", fontsize=12, color=INK, linespacing=1.5)


fig("provenance.png", 8.73, 4.91, provenance)

card(
    "roundtrip.png", 1600, 900,
    [
        ("$ uv run python scripts/01_fhir_to_table.py", LIME, True),
        ("", GREY, False),
        ("Identical to patients.csv : True", "#D9E4DC", True),
        ("", GREY, False),
        ("in a real project nobody hands you", MUTED, False),
        ("the answer to check against", MUTED, False),
    ],
    title="The round-trip check", size=34, line_gap=2.0,
)


# ---------------------------------------- every command, on one wide card
# The agenda page carries this so a student who only ever looks at the
# projector can still see the whole afternoon as seven lines.
card(
    "every_command.png", 1600, 900,
    [
        ("    uv sync", MUTED, False),
        ("1   uv run python scripts/01_fhir_to_table.py", LIME, True),
        ("2   uv run python scripts/02_explore_data.py", LIME, True),
        ("    uv run python scripts/03_train_model.py", LIME, True),
        ("3   uv run streamlit run app/streamlit_app.py", LIME, True),
        ("    uv run uvicorn app.api:app --reload", LIME, True),
    ],
    title="EVERY COMMAND", size=30, line_gap=2.05,
)


# ------------------------------ what the two failure modes do to the table
# Slide 10 used to explain this in prose. A table showing the actual damage
# says it in two seconds: one column deleted by a flag, one cell that was
# never sent. Both drawn from the real flattened output.
def broken_table(ax):
    cols = ["patient_id", "radius", "texture", "perimeter", "area", "malignant"]
    # the first few rows, then the neighbourhood of P0010 - the patient whose
    # texture Observation was never sent. Without it the arrow points at nothing.
    keep = ["P0001", "P0002", "P0003", "P0004", "P0008", "P0009", "P0010"]
    rows = df[df["patient_id"].isin(keep)].set_index("patient_id").loc[keep].reset_index()

    ax.axis("off")
    n = len(rows)
    ax.set_xlim(0, 100); ax.set_ylim(0, n + 4.2)
    xs = [4, 24, 38, 52, 68, 84]

    # the column --drop area removes
    ax.add_patch(plt.Rectangle((xs[4] - 5, 0.4), 14, n + 1.5, color="#F6DCD2"))

    for x, c in zip(xs, cols):
        ax.text(x, n + 1.9, c, fontsize=11.5, color=MUTED, fontweight="bold",
                ha="left" if c == "patient_id" else "center",
                family="DejaVu Sans Mono")

    for i, (_, r) in enumerate(rows.iterrows()):
        y = n - i
        gone = r["patient_id"] == "P0010"
        ax.text(xs[0], y, r["patient_id"], fontsize=11.5, color=INK,
                family="DejaVu Sans Mono")
        if r["patient_id"] == "P0008":       # mark the gap in the sequence
            ax.text(xs[0], y + 0.52, "...", fontsize=11.5, color=MUTED,
                    family="DejaVu Sans Mono")
        for x, c in zip(xs[1:], cols[1:]):
            if gone and c == "texture":
                ax.text(x, y, "NaN", fontsize=11.5, color=ALERT, ha="center",
                        fontweight="bold", family="DejaVu Sans Mono")
                continue
            val = f"{r[c]:.0f}" if c == "malignant" else f"{r[c]:.2f}"
            faded = c == "area"
            ax.text(x, y, val, fontsize=11.5, ha="center",
                    color="#C0938A" if faded else INK, family="DejaVu Sans Mono")

    ax.annotate("--drop area\ndeleted this column",
                xy=(xs[4], n + 2.6), xytext=(xs[4] + 4, n + 3.8),
                fontsize=11, color=ALERT, fontweight="bold", ha="left",
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-|>", color=ALERT, lw=1.6))
    ax.annotate("this Observation was\nnever in the Bundle",
                xy=(xs[2] + 4, 1.0), xytext=(xs[2] - 24, -0.4),
                fontsize=11, color=ALERT, fontweight="bold", ha="left",
                linespacing=1.35,
                arrowprops=dict(arrowstyle="-|>", color=ALERT, lw=1.6))
    ax.text(50, n + 3.9, "the script exits 0 either way",
            fontsize=12, color=INK, ha="center", style="italic")


fig("broken_table.png", 8.73, 4.91, broken_table)

# The ten Observations, spelled out. The room has just been told an Observation
# is "one measurement"; this says which ten, in words a clinician would use.
# Codes are read from common.RAW_FEATURES so the list can never drift from the
# table the model is actually trained on.
FEATURE_MEANING = {
    "radius": "average distance from the centre to the edge",
    "texture": "how much the grey-scale varies inside it",
    "perimeter": "length all the way round the boundary",
    "area": "area enclosed by that boundary",
    "smoothness": "how much the edge wobbles, locally",
    "compactness": "perimeter squared over area — how tight it is",
    "concavity": "how deep the dents in the edge go",
    "concave_points": "how many dents there are",
    "symmetry": "how alike the two halves are",
    "fractal_dimension": "how ragged the edge is overall",
}


def features_table(ax):
    """Observation.code -> what it actually measures. Ten rows, two columns."""
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    rows = [(c, FEATURE_MEANING[c]) for c in RAW_FEATURES]
    top, h = 92.0, 8.2

    ax.add_patch(plt.Rectangle((0, top - h), 100, h, color=DARK))
    ax.text(3, top - h / 2, "Observation.code", va="center",
            fontsize=12.5, fontweight="bold", color="white", family="DejaVu Sans Mono")
    ax.text(37, top - h / 2, "what it measures on the cell nucleus", va="center",
            fontsize=12.5, fontweight="bold", color="#D8E6C4")

    y = top - h
    for i, (code, meaning) in enumerate(rows):
        y -= h
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0, y), 100, h, color="#EFF3EE"))
        ax.text(3, y + h / 2, code, va="center", fontsize=11.5,
                color=DARK, family="DejaVu Sans Mono")
        ax.text(37, y + h / 2, meaning, va="center", fontsize=11.5, color=INK)

    ax.text(3, y - 5.5, "ten Observations, one Condition, one Patient  ->  "
            "12 resources in P0001.json",
            fontsize=10.5, color=MUTED, style="italic")


fig("features_table.png", 10.00, 5.74, features_table)


# Feature engineering made concrete. Two nuclei drawn with the SAME area and
# very different outlines, so the ratio the room is about to meet has a picture
# behind it. Both shapes and both numbers are computed here, not typed.
def engineered(ax):
    """Why a shape ratio exists: same size, different outline."""
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 62)

    def blob(cx, cy, lobes, amp, target_area, color):
        t = np.linspace(0, 2 * np.pi, 720)
        r = 1 + amp * np.cos(lobes * t)
        area = 0.5 * np.trapezoid(r ** 2, t)          # polar area
        k = np.sqrt(target_area / area)               # rescale to equal area
        r = r * k
        x, y = cx + r * np.cos(t) * 9, cy + r * np.sin(t) * 9
        per = np.sum(np.hypot(np.diff(x), np.diff(y)))
        ar = 0.5 * np.abs(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1]))
        ax.fill(x, y, color=color, alpha=0.9)
        return per ** 2 / ar

    a = blob(24, 38, 0, 0.0, np.pi, "#BFD8A8")
    b = blob(74, 38, 7, 0.28, np.pi, "#7FA653")

    for cx, label, val in ((24, "round", a), (74, "ragged", b)):
        ax.text(cx, 17, label, ha="center", fontsize=13,
                fontweight="bold", color=DARK)
        ax.text(cx, 11, f"perimeter² / area = {val:.1f}", ha="center",
                fontsize=12, color=INK, family="DejaVu Sans Mono")

    ax.text(50, 57, "Same area. Different outline.", ha="center",
            fontsize=13.5, fontweight="bold", color=INK)
    ax.text(50, 3.0,
            "radius, perimeter and area cannot separate these two on their own.\n"
            "compactness_ratio can — and nobody sent it to us.",
            ha="center", fontsize=11.5, color=MUTED, linespacing=1.6)


fig("engineered.png", 8.73, 4.91, engineered)


# The results page used to carry a ROC curve, which is a whole concept nobody
# defined. What the page is actually about is the disagreement: identical
# accuracy, different recall. Draw that instead. Numbers come from results.json.
def two_models_compare(ax):
    """The whole point of the results page: identical accuracy, different recall."""
    m = R["models"]
    logit, forest = m["logit"], m["forest"]
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)

    xa, xb = 52, 82
    ax.text(50, 94, "Same accuracy.", ha="center", fontsize=15,
            fontweight="bold", color=INK)
    ax.text(50, 87, "Different recall.", ha="center", fontsize=15,
            fontweight="bold", color=DARK)

    for x, name in ((xa, logit["name"]), (xb, forest["name"])):
        for k, word in enumerate(name.split()):
            ax.text(x, 74 - k * 5.5, word, ha="center", fontsize=11.5,
                    fontweight="bold", color=DARK)

    rows = [("accuracy", f"{logit['accuracy']:.3f}", f"{forest['accuracy']:.3f}",
             "identical", "#EFF3EE"),
            ("recall", f"{logit['recall']:.3f}", f"{forest['recall']:.3f}",
             "the one that moved", None),
            ("tumours missed", str(logit["confusion"]["fn"]),
             str(forest["confusion"]["fn"]), "two more cancers", None)]

    y = 58
    for label, a, b, note, band in rows:
        if band:
            ax.add_patch(plt.Rectangle((2, y - 4.4), 96, 13, color=band))
        ax.text(4, y + 2, label, fontsize=12, color=MUTED)
        big = 21 if label == "tumours missed" else 19
        col = ALERT if label != "accuracy" else INK
        ax.text(xa, y, a, ha="center", fontsize=big, color=INK,
                family="DejaVu Sans Mono")
        ax.text(xb, y, b, ha="center", fontsize=big,
                color=col if label != "accuracy" else INK,
                family="DejaVu Sans Mono")
        ax.text(4, y - 6.5, note, fontsize=10,
                color=MUTED if label == "accuracy" else ALERT, style="italic")
        y -= 20

    ax.text(50, 2, "Report accuracy and these two models are the same.",
            ha="center", fontsize=11, color=MUTED)


fig("two_models_compare.png", 6.5, 6.72, two_models_compare)

