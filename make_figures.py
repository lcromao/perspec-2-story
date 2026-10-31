#!/usr/bin/env python3
"""
Likert-style figures for the LLM-as-a-judge results.

Reads runs/<run>/analysis/decoded_long.csv (written by "judge_runner.py analyze") and writes,
in runs/<run>/analysis/figures/:

  fig_overall           Both projects: all criteria pooled and each criterion.
  fig_project_M         Project M: one bar per story type (all criteria pooled).
  fig_project_N         Project N: same for project N.
  fig_project_M_by_criterion, fig_project_N_by_criterion
                        One panel per criterion, one bar per story type.
  likert_shares.csv     The shares plotted in every figure.

Each bar shows the share of all judgments (4 judges x 2 orders x 3 repetitions x items)
that preferred the ad hoc version, had no preference, or preferred the mapping version.
Figures are saved as PDF (for LaTeX) and PNG.

Usage: .venv/bin/python make_figures.py [--run main]
"""

import argparse
import csv
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent

STORIES = [
    "Data Collection",
    "Data Pre-processing",
    "Data Management",
    "Model Feature Preprocessing",
    "Model Training & Evaluation",
    "Model Deployment",
    "Model Integration",
]
CRITERIA = ["Completeness", "Clarity", "Correctness", "Consistency"]
PROJECTS = {"M": "Malicious URL Classification", "N": "NYC Taxi Trip Duration Regression"}

CATS = ["ad hoc", "no preference", "mapping"]
LABELS = {"ad hoc": "Ad hoc preferred", "no preference": "No preference", "mapping": "Mapping preferred"}
COLORS = {"ad hoc": "#C8702A", "no preference": "#D9D9D6", "mapping": "#2B6CA3"}
TEXT_ON = {"ad hoc": "white", "no preference": "#3A3A38", "mapping": "white"}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 8.5,
    "axes.edgecolor": "#8A8A86",
    "axes.linewidth": 0.6,
    "xtick.color": "#4A4A47",
    "ytick.color": "#2A2A28",
    "pdf.fonttype": 42,
})


def shares(rows):
    c = Counter(r["preferred_condition"] for r in rows)
    n = sum(c[k] for k in CATS)
    return n, {k: (c[k] / n if n else 0.0) for k in CATS}


def draw(ax, labels, data, title=None, show_xlabel=True, show_ylabels=True, label_min=0.12, label_size=7.5):
    """Diverging stacked bars centred on the middle of 'no preference'."""
    for i, (label, (n, s)) in enumerate(zip(labels, data)):
        y = len(labels) - 1 - i
        left = -s["ad hoc"] - s["no preference"] / 2
        for k in CATS:
            w = s[k]
            if w <= 0:
                continue
            ax.barh(y, w, left=left, height=0.68, color=COLORS[k], edgecolor="white", linewidth=0.6)
            if w >= label_min:
                ax.text(left + w / 2, y, f"{w:.0%}", ha="center", va="center", fontsize=label_size, color=TEXT_ON[k])
            left += w
    ax.axvline(0, color="#6B6B67", linewidth=0.6, zorder=0)
    ax.set_xlim(-1.02, 1.02)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xticklabels(["100%", "50%", "0", "50%", "100%"])
    ax.set_ylim(-0.6, len(labels) - 0.4)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(list(reversed(labels)))
    ax.tick_params(axis="y", length=0, labelleft=show_ylabels)
    ax.tick_params(axis="x", labelsize=7)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    if title:
        ax.set_title(title, fontsize=9, loc="left", pad=4)
    if show_xlabel:
        ax.set_xlabel("Share of judgments  (← ad hoc · mapping →)", fontsize=7.5, color="#4A4A47")


def legend(fig, y=0.0):
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[k]) for k in CATS]
    fig.legend(handles, [LABELS[k] for k in CATS], loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, y), fontsize=8, handlelength=1.2, columnspacing=1.6)


def save(fig, out, name):
    for ext in ("pdf", "png"):
        fig.savefig(out / f"{name}.{ext}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="main")
    args = ap.parse_args()
    adir = HERE / "runs" / args.run / "analysis"
    rows = list(csv.DictReader(open(adir / "decoded_long.csv", encoding="utf-8")))
    out = adir / "figures"
    out.mkdir(parents=True, exist_ok=True)
    table = []

    def record(figure, project, story, criterion, sel):
        n, s = shares(sel)
        table.append({"figure": figure, "project": project, "story_type": story, "characteristic": criterion,
                      "n_judgments": n, **{f"share_{k.replace(' ', '_')}": round(s[k], 4) for k in CATS},
                      "net_mapping_minus_adhoc": round(s["mapping"] - s["ad hoc"], 4)})
        return n, s

    # Overall: one panel per project, rows = all criteria + each criterion
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.3), sharey=True)
    labels = ["All criteria"] + CRITERIA
    for ax, (p, pname) in zip(axes, PROJECTS.items()):
        P = [r for r in rows if r["project"] == p]
        data = [record("overall", p, "All", "All", P)]
        data += [record("overall", p, "All", c, [r for r in P if r["characteristic"] == c]) for c in CRITERIA]
        draw(ax, labels, data, title=f"Project {p} — {pname}", show_ylabels=(ax is axes[0]))
    fig.tight_layout(w_pad=1.5)
    legend(fig, y=0.0)
    save(fig, out, "fig_overall")

    # Per project: one bar per story type
    for p, pname in PROJECTS.items():
        P = [r for r in rows if r["project"] == p]
        labels = ["All stories"] + STORIES
        data = [record(f"project_{p}", p, "All", "All", P)]
        data += [record(f"project_{p}", p, s, "All", [r for r in P if r["story_type"] == s]) for s in STORIES]
        fig, ax = plt.subplots(figsize=(6.2, 3.0))
        draw(ax, labels, data, title=f"Project {p} — {pname}")
        ax.axhline(len(labels) - 1.5, color="#BDBDB8", linewidth=0.6)
        fig.tight_layout()
        legend(fig, y=0.0)
        save(fig, out, f"fig_project_{p}")

        # Per project: story x criterion
        fig, axes = plt.subplots(1, 4, figsize=(9.6, 2.9), sharey=True)
        for ax, c in zip(axes, CRITERIA):
            C = [r for r in P if r["characteristic"] == c]
            data = [record(f"project_{p}_by_criterion", p, s, c, [r for r in C if r["story_type"] == s]) for s in STORIES]
            draw(ax, STORIES, data, title=c, show_xlabel=False, show_ylabels=(ax is axes[0]),
                 label_min=0.22, label_size=6.5)
        fig.suptitle(f"Project {p} — {pname}", x=0.01, ha="left", fontsize=9.5)
        fig.tight_layout(w_pad=0.8)
        legend(fig, y=0.0)
        save(fig, out, f"fig_project_{p}_by_criterion")

    with open(out / "likert_shares.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)
    print(f"Wrote figures and likert_shares.csv to {out}")


if __name__ == "__main__":
    main()
