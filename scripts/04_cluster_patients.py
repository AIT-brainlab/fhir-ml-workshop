"""
STEP 4 - UNSUPERVISED LEARNING
Find patient subgroups WITHOUT using the diagnosis label.

    uv run python scripts/04_cluster_patients.py

Saves a PCA scatter plot to reports/.

Ask for a different number of groups and see what happens:

    --clusters 3          three groups
    --clusters 5          five groups
    --seed 7              a different starting point
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "patients.csv"
REPORTS = ROOT / "reports"

TARGET = "malignant"
RANDOM_STATE = 42


def rule(title: str) -> None:
    print(f"\n{'=' * 62}\n{title}\n{'=' * 62}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Cluster patients without labels.")
    p.add_argument("--clusters", type=int, default=2, help="how many groups to ask for")
    p.add_argument("--seed", type=int, default=RANDOM_STATE, help="random seed")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    REPORTS.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    features = [c for c in df.columns if c not in ("patient_id", TARGET)]
    X, y = df[features], df[TARGET]

    rule("1. CLUSTER THE PATIENTS (the label is hidden from the model)")
    kmeans = Pipeline(
        [("scale", StandardScaler()),
         ("cluster", KMeans(n_clusters=args.clusters, n_init=10, random_state=args.seed))]
    )
    clusters = kmeans.fit_predict(X)
    print(f"Silhouette score: {silhouette_score(StandardScaler().fit_transform(X), clusters):.3f}")
    print("(0 = overlapping blobs, 1 = tight well-separated groups)")

    rule("2. DID THE CLUSTERS REDISCOVER THE DIAGNOSIS?")
    table = pd.crosstab(clusters, y, rownames=["cluster"], colnames=["actual"])
    table.columns = ["benign", "malignant"]
    print(f"You asked for {args.clusters} group(s).")
    print(table.to_string())
    ari = adjusted_rand_score(y, clusters)
    print(f"\nAdjusted Rand Index vs. true diagnosis: {ari:.3f}")
    print("The algorithm never saw the diagnosis, yet the groups line up with it.")
    print("That is the point: structure already exists in the measurements.")

    rule("3. PROFILE OF EACH SUBGROUP (average measurements)")
    profile = X.assign(cluster=clusters).groupby("cluster").mean().round(2)
    print(profile.T.to_string())

    # ------------------------------------------------------------ pca plot
    coords = PCA(n_components=2, random_state=args.seed).fit_transform(
        StandardScaler().fit_transform(X)
    )
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharex=True, sharey=True)
    axes[0].scatter(coords[:, 0], coords[:, 1], c=clusters, cmap="coolwarm", s=14, alpha=0.8)
    axes[0].set_title("K-Means clusters (label never used)")
    axes[1].scatter(coords[:, 0], coords[:, 1], c=y, cmap="coolwarm", s=14, alpha=0.8)
    axes[1].set_title("Actual diagnosis")
    for ax in axes:
        ax.set_xlabel("PC 1")
    axes[0].set_ylabel("PC 2")
    fig.suptitle("Patients projected onto two principal components")
    fig.tight_layout()
    fig.savefig(REPORTS / "03_clusters_pca.png", dpi=150)
    plt.close(fig)

    rule("DONE")
    print("Figure saved -> reports/03_clusters_pca.png")
    print("\nDiscuss: clustering found groups, but it cannot tell you which group")
    print("is dangerous. Only labelled data can do that.")
    print("\nAsk for a different number of groups:")
    print("  uv run python scripts/04_cluster_patients.py --clusters 3")
    print("  uv run python scripts/04_cluster_patients.py --clusters 5")
    print("\nThree groups will always appear if you ask for three. That is the trap.")
    print("\nNext:  uv run streamlit run app/streamlit_app.py")


if __name__ == "__main__":
    main()
