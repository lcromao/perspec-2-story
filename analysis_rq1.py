#!/usr/bin/env python3
"""Rebuild RQ1 as two descriptive ordinal analyses of the processed working CSV.

Run from the project: .venv/bin/python analysis_rq1.py
The historical output filenames are retained; no arithmetic scale means or
mean-based crossover effects are calculated. Source CSV files are read-only.
"""

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
STORIES = [
    "Data Collection", "Data Pre-processing", "Data Management",
    "Model Feature Preprocessing", "Model Training & Evaluation",
    "Model Deployment", "Model Integration",
]
ITEMS = STORIES + ["Sufficient time"]
MAP_FIRST = {"A", "C"}
SCALE = tuple(range(1, 8))
COLORS = {1: "#E8898A", 2: "#F2B3B3", 3: "#F8DADA", 4: "#DCDCDC",
          5: "#D3ECD9", 6: "#A8D5B3", 7: "#7DBE8D"}
GREEN, RED = "#3F8F57", "#C65B5C"
SCENARIOS = {"com_54": False, "sem_54": True}
TITLES = {"com_54": "Com as 54 notas 4 sem justificativa",
          "sem_54": "Sem as 54 notas 4 sem justificativa"}
DATE = "2026-10-27"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8,
                     "pdf.fonttype": 42, "axes.linewidth": 0.6})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    assert rows, path
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)


def central_categories(values):
    """Lower/upper central observed categories: never interpolate ordinal scores."""
    ordered = sorted(values)
    if not ordered:
        return None, None
    return ordered[(len(ordered) - 1) // 2], ordered[len(ordered) // 2]


def med_text(values):
    lo, hi = central_categories(values)
    return "—" if lo is None else str(lo) if lo == hi else f"{lo}–{hi}"


def pct(numerator, denominator):
    return 100 * numerator / denominator if denominator else None


def display(numerator, denominator):
    return f"{numerator}/{denominator} ({pct(numerator, denominator):.1f}%)" if denominator else "— (n=0)"


def load(data_path):
    with data_path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    people, records = [], []
    for row in rows:
        pid = row["participante"].replace("Grupo_", "").replace("-Individuo_", "")
        group = pid[0]
        sequence = "MAP->ADHOC" if group in MAP_FIRST else "ADHOC->MAP"
        audit = {x["campo"]: x for x in json.loads(row["recodificacoes_na"] or "[]")}
        person_records = []
        for project, section, period in (("M", 2, 1), ("N", 3, 2)):
            condition = "mapping" if (group in MAP_FIRST) == (period == 1) else "ad_hoc"
            for item, name in enumerate(ITEMS, 1):
                field = f"{section}.{item}.a"
                raw = row[field].strip()
                justification = row[f"{section}.{item}.b"].strip()
                if raw == "":
                    value, status = None, "missing"
                elif raw == "N.A":
                    value, status = None, "not_applicable"
                else:
                    assert raw in {str(v) for v in SCALE}, (pid, field, raw)
                    value = int(raw)
                    status = "neutral_unknown" if item <= 7 and value == 4 and not justification else (
                        "neutral_accepted" if item <= 7 and value == 4 else "rated")
                record = dict(participant=pid, group=group, sequence=sequence, project=project,
                              period=period, item_index=item, item=name, field=field,
                              condition=condition, input_value=raw, value=value,
                              source_status=status, justification=justification,
                              original_before_na=audit.get(field, {}).get("valor_original", ""),
                              recoding_reason=audit.get(field, {}).get("motivo", ""))
                person_records.append(record)
        eligible = any(r["value"] is not None and r["item_index"] <= 7 for r in person_records)
        for record in person_records:
            record["participant_eligible"] = eligible
        people.append(dict(id=pid, group=group, sequence=sequence, eligible=eligible,
                           records=person_records))
        records.extend(person_records)
    assert len(people) == 20
    assert sum(p["eligible"] for p in people) == 17
    tally = Counter(r["source_status"] for r in records if r["item_index"] <= 7)
    assert tally == Counter(missing=43, not_applicable=23, neutral_unknown=54,
                            neutral_accepted=7, rated=153), tally
    return people, records


def kept(record, remove_unknown):
    return record["participant_eligible"] and record["value"] is not None and not (
        remove_unknown and record["source_status"] == "neutral_unknown")


def values(records, remove_unknown):
    return [r["value"] for r in records if kept(r, remove_unknown)]


def summarize(records, remove_unknown):
    eligible = [r for r in records if r["participant_eligible"]]
    included = [r for r in eligible if kept(r, remove_unknown)]
    counts = Counter(r["value"] for r in included)
    n = len(included)
    lo, hi = central_categories([r["value"] for r in included])
    result = dict(n_expected=len(eligible), n_valid=n,
                  n_not_applicable=sum(r["source_status"] == "not_applicable" for r in eligible),
                  n_missing=sum(r["source_status"] == "missing" for r in eligible),
                  n_unknown_excluded=sum(remove_unknown and r["source_status"] == "neutral_unknown" for r in eligible),
                  n_unknown_retained=sum(not remove_unknown and r["source_status"] == "neutral_unknown" for r in eligible),
                  n_accepted_neutral=sum(r["source_status"] == "neutral_accepted" for r in included),
                  n_below4=sum(counts[v] for v in (1, 2, 3)), n_neutral=counts[4],
                  n_above4=sum(counts[v] for v in (5, 6, 7)),
                  median_lower=lo if lo is not None else "",
                  median_upper=hi if hi is not None else "")
    for v in SCALE:
        result[f"count_{v}"] = counts[v]
        result[f"pct_{v}"] = round(pct(counts[v], n), 6) if n else ""
    result["pct_below4"] = round(pct(result["n_below4"], n), 6) if n else ""
    result["pct_neutral"] = round(pct(result["n_neutral"], n), 6) if n else ""
    result["pct_above4"] = round(pct(result["n_above4"], n), 6) if n else ""
    assert result["n_expected"] == n + result["n_not_applicable"] + result["n_missing"] + result["n_unknown_excluded"]
    assert n == sum(result[f"count_{v}"] for v in SCALE)
    return result


def matched_profile(person, remove_unknown):
    per = {}
    for project in ("M", "N"):
        per[project] = {r["item_index"]: r["value"] for r in person["records"]
                        if r["project"] == project and r["item_index"] <= 7 and kept(r, remove_unknown)}
    common = sorted(per["M"].keys() & per["N"].keys())
    return common, {project: [per[project][i] for i in common] for project in ("M", "N")}


def participant_rows(people, remove_unknown):
    output = []
    for person in people:
        row = dict(participant=person["id"], group=person["group"], sequence=person["sequence"],
                   eligible=person["eligible"])
        for project in ("M", "N"):
            subset = [r for r in person["records"] if r["project"] == project and r["item_index"] <= 7]
            # Per-person coverage retains the seven missing entries of ineligible people.
            stats = summarize([r | {"participant_eligible": True} for r in subset], remove_unknown)
            for key in ("n_valid", "n_not_applicable", "n_missing", "n_unknown_excluded", "n_unknown_retained",
                        "n_below4", "n_neutral", "n_above4", "median_lower", "median_upper"):
                row[f"{project}_{key}"] = stats[key]
            for score in SCALE:
                row[f"{project}_count_{score}"] = stats[f"count_{score}"]
            time = next(r for r in person["records"] if r["project"] == project and r["item_index"] == 8)
            row[f"time_{project}"] = time["value"] if time["value"] is not None else ""
        common, profiles = matched_profile(person, remove_unknown)
        row["matched_story_count"] = len(common)
        row["matched_story_indices"] = ";".join(map(str, common))
        row["trajectory_included"] = bool(common)
        for project in ("M", "N"):
            lo, hi = central_categories(profiles[project])
            row[f"matched_{project}_median_lower"] = lo if lo is not None else ""
            row[f"matched_{project}_median_upper"] = hi if hi is not None else ""
        output.append(row)
    return output


def paired_story_rows(people, remove_unknown):
    output = []
    for item, name in enumerate(ITEMS, 1):
        row = dict(item=name, item_index=item)
        for sequence, prefix in (("MAP->ADHOC", "mapping_first"), ("ADHOC->MAP", "adhoc_first")):
            pairs = []
            for person in people:
                if person["sequence"] != sequence or not person["eligible"]:
                    continue
                selected = [r for r in person["records"] if r["item_index"] == item and kept(r, remove_unknown)]
                per = {r["project"]: r["value"] for r in selected}
                if len(per) == 2:
                    pairs.append((per["M"], per["N"]))
            row[f"{prefix}_pairs"] = len(pairs)
            row[f"{prefix}_round2_higher"] = sum(n > m for m, n in pairs)
            row[f"{prefix}_equal"] = sum(n == m for m, n in pairs)
            row[f"{prefix}_round2_lower"] = sum(n < m for m, n in pairs)
            for project, index in (("M", 0), ("N", 1)):
                lo, hi = central_categories([pair[index] for pair in pairs])
                row[f"{prefix}_{project}_median_lower"] = lo if lo is not None else ""
                row[f"{prefix}_{project}_median_upper"] = hi if hi is not None else ""
            assert len(pairs) == row[f"{prefix}_round2_higher"] + row[f"{prefix}_equal"] + row[f"{prefix}_round2_lower"]
        output.append(row)
    return output


def save_figure(fig, folder, name):
    for ext in ("pdf", "png"):
        fig.savefig(folder / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig_likert(distributions, people, folder, project, remove_unknown):
    fig, axes = plt.subplots(1, 2, figsize=(7.16, 2.75), sharey=True)
    for ax, condition in zip(axes, ("mapping", "ad_hoc")):
        selected = [d for d in distributions if d["project"] == project and d["condition"] == condition]
        for i, row in enumerate(selected):
            y = 7 - i
            n = row["n_valid"]
            shares = {v: row[f"count_{v}"] / n if n else 0 for v in SCALE}
            left = -sum(shares[v] for v in (1, 2, 3)) - shares[4] / 2
            for score in SCALE:
                width = shares[score]
                if width:
                    ax.barh(y, width, left=left, height=0.62, color=COLORS[score], edgecolor="white", linewidth=0.5)
                    if score == 4 and row["n_unknown_retained"]:
                        unknown = row["n_unknown_retained"] / n
                        ax.barh(y, unknown, left=left + width - unknown, height=0.62,
                                facecolor="none", edgecolor="#888884", hatch="////", linewidth=0)
                    if width >= 0.13:
                        ax.text(left + width / 2, y, f"{width:.0%}", ha="center", va="center",
                                fontsize=6.3 if width >= 0.2 else 5.4, color="#2E2E2C")
                left += width
            ax.text(1.015, y, f"n={n}", transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=6.0)
        ax.axvline(0, color="#7A7A76", linestyle=(0, (3, 3)), linewidth=0.7, zorder=0)
        ax.axhline(0.5, color="#B5B5B0", linewidth=0.6)
        ax.set_xlim(-1.02, 1.02)
        ax.set_ylim(-0.6, 7.6)
        ax.set_xticks([])
        ax.set_yticks(range(8))
        ax.set_yticklabels(list(reversed([f"{s} Story" for s in STORIES] + ["Sufficient time"])))
        ax.tick_params(axis="y", length=0, labelleft=ax is axes[0], labelsize=7.0)
        for spine in ax.spines.values():
            spine.set_color("#9A9A96")
        teams = "A and C" if (project == "M") == (condition == "mapping") else "B and D"
        title = "With mapping" if condition == "mapping" else "Ad hoc"
        ax.set_title(f"{title} (teams {teams})", fontsize=8.5, pad=4)
    labels = {1: "1 - It wasn't easy", 4: "4 - Neutral", 7: "7 - It was easy"}
    fig.tight_layout(w_pad=1.8)
    handles = [Patch(facecolor=COLORS[s]) for s in SCALE]
    fig.legend(handles, [labels.get(s, str(s)) for s in SCALE], loc="upper center", ncol=7,
               frameon=True, fancybox=False, edgecolor="#D0D0CC", bbox_to_anchor=(0.5, 0.02),
               fontsize=7, handlelength=1.1, columnspacing=1.1, handletextpad=0.4)
    note = "n = valid ratings per item. Time: 1 = insufficient; 7 = sufficient."
    if not remove_unknown:
        note += " Hatched gray: 4 without justification."
    fig.text(0.5, -0.105, note, ha="center", va="top", fontsize=5.8, color="#444440")
    save_figure(fig, folder, f"rq1_likert_project{project}")


def fig_crossover(profiles, folder):
    fig, ax = plt.subplots(figsize=(3.45, 2.55))
    labels = {0: [], 1: []}
    included = [p for p in profiles if p["trajectory_included"]]
    for sequence, color, dx in (("MAP->ADHOC", "#4C6E91", -0.04), ("ADHOC->MAP", "#9C6B3C", 0.04)):
        people = [p for p in included if p["sequence"] == sequence]
        for person in people:
            ax.plot([dx, 1 + dx], [person["matched_M_median_lower"], person["matched_N_median_lower"]],
                    color=color, alpha=0.18, linewidth=0.8)
        med = {project: central_categories([p[f"matched_{project}_median_lower"] for p in people])[0]
               for project in ("M", "N")}
        first = sequence == "MAP->ADHOC"
        label = "Mapping first (A, C)" if first else "Ad hoc first (B, D)"
        ax.plot([dx, 1 + dx], [med["M"], med["N"]], color=color, linewidth=1.8,
                label=f"{label}, n={len(people)}")
        for side, project in enumerate(("M", "N")):
            is_mapping = first == (side == 0)
            ax.scatter(side + dx, med[project], s=34, zorder=3,
                       color=GREEN if is_mapping else "white", edgecolor=GREEN if is_mapping else RED,
                       linewidth=1.3)
            labels[side].append((med[project], color))
    for side, points in labels.items():
        points.sort()
        gap = max(0, 0.25 - (points[-1][0] - points[0][0]))
        for i, (value, color) in enumerate(points):
            y = value + (gap / 2 if i else -gap / 2)
            ax.text(-0.13 if side == 0 else 1.13, y, str(value), ha="right" if side == 0 else "left",
                    va="center", fontsize=7, color=color)
    ax.set_xticks([0, 1], ["Round 1\n(project M)", "Round 2\n(project N)"])
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(0.8, 8.1)
    ax.set_yticks(SCALE)
    ax.set_ylabel("Median category of matched stories (1-7)", fontsize=7)
    ax.axhline(4, color="#9A9A96", linestyle=(0, (3, 3)), linewidth=0.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.scatter([], [], s=30, color=GREEN, label="With mapping")
    ax.scatter([], [], s=30, color="white", edgecolor=RED, linewidth=1.2, label="Ad hoc")
    ax.legend(fontsize=6.0, frameon=False, loc="upper left")
    counts = [p["matched_story_count"] for p in included]
    ax.text(0.98, 0.025, f"Matched stories/person: {min(counts)}-{max(counts)}\nLower central categories; descriptive",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=5.7, color="#3A3A38")
    fig.tight_layout()
    save_figure(fig, folder, "rq1_crossover")


def before_after_distributions(people, remove_unknown):
    """Round distributions with the same respondents per item and sequence."""
    output = []
    for sequence in ("MAP->ADHOC", "ADHOC->MAP"):
        candidates = [p for p in people if p["eligible"] and p["sequence"] == sequence]
        for item, name in enumerate(ITEMS, 1):
            lookup = {p["id"]: {r["project"]: r for r in p["records"] if r["item_index"] == item}
                      for p in candidates}
            matched = {pid for pid, rounds in lookup.items()
                       if all(kept(rounds[project], remove_unknown) for project in ("M", "N"))}
            for project, period in (("M", 1), ("N", 2)):
                partner = "N" if project == "M" else "M"
                selected = [rounds[project] for pid, rounds in lookup.items() if pid in matched]
                stats = summarize(selected, remove_unknown)
                own_invalid = sum(not kept(rounds[project], remove_unknown) for rounds in lookup.values())
                partner_invalid = sum(kept(rounds[project], remove_unknown) and
                                      not kept(rounds[partner], remove_unknown) for rounds in lookup.values())
                assert len(candidates) == len(matched) + own_invalid + partner_invalid
                condition = "mapping" if (sequence == "MAP->ADHOC") == (project == "M") else "ad_hoc"
                row = dict(sequence=sequence, project=project, period=period, condition=condition,
                           item_index=item, item=name, n_candidates=len(candidates), n_pairs=len(matched),
                           n_unpaired_excluded=len(candidates) - len(matched),
                           n_own_invalid=own_invalid, n_partner_invalid_when_own_valid=partner_invalid,
                           n_unknown_retained=stats["n_unknown_retained"],
                           n_accepted_neutral=stats["n_accepted_neutral"])
                for score in SCALE:
                    row[f"count_{score}"] = stats[f"count_{score}"]
                    row[f"pct_{score}"] = stats[f"pct_{score}"]
                assert sum(row[f"count_{score}"] for score in SCALE) == row["n_pairs"]
                output.append(row)
    return output


def fig_likert_before_after(distributions, folder, remove_unknown):
    """Reference-style side-by-side 100% stacks, separated by treatment sequence."""
    fig, axes = plt.subplots(2, 2, figsize=(7.16, 5.8), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.29, right=0.93, top=0.88, bottom=0.20, wspace=0.30, hspace=0.75)
    item_labels = STORIES + ["Sufficient time"]
    for seq_index, sequence in enumerate(("MAP->ADHOC", "ADHOC->MAP")):
        heading = "Mapping first (teams A and C)" if sequence == "MAP->ADHOC" else "Ad hoc first (teams B and D)"
        axes[seq_index, 0].text(0, 1.30, heading, transform=axes[seq_index, 0].transAxes,
                                ha="left", va="bottom", fontsize=9, fontweight="bold")
        for column, project in enumerate(("M", "N")):
            ax = axes[seq_index, column]
            selected = [d for d in distributions if d["sequence"] == sequence and d["project"] == project]
            for index, row in enumerate(selected):
                y, n, left = 7 - index, row["n_pairs"], 0.0
                for score in SCALE:
                    width = row[f"count_{score}"] / n if n else 0
                    if width:
                        ax.barh(y, width, left=left, height=0.62, color=COLORS[score],
                                edgecolor="white", linewidth=0.5)
                        if score == 4 and row["n_unknown_retained"]:
                            unknown = row["n_unknown_retained"] / n
                            ax.barh(y, unknown, left=left + width - unknown, height=0.62,
                                    facecolor="none", edgecolor="#888884", hatch="////", linewidth=0)
                        if width >= 0.13:
                            ax.text(left + width / 2, y, f"{width:.0%}", ha="center", va="center",
                                    fontsize=6.1 if width >= 0.2 else 5.3, color="#2E2E2C")
                    left += width
                ax.text(1.035, y, f"n={n}", transform=ax.get_yaxis_transform(),
                        ha="left", va="center", fontsize=6.0)
                if not n:
                    ax.text(0.5, y, "No matched responses", ha="center", va="center", fontsize=6)
            treatment = "With mapping" if selected[0]["condition"] == "mapping" else "Ad hoc"
            ax.set_title(f"Round {column + 1} (project {project})\n{treatment}", fontsize=8, pad=6)
            ax.set_xlim(0, 1)
            ax.set_ylim(-0.6, 7.6)
            ax.set_xticks([0, 0.5, 1], ["0%", "50%", "100%"])
            ax.set_yticks(range(8), list(reversed(item_labels)))
            ax.tick_params(axis="x", labelbottom=True, labelsize=6.5, length=2)
            ax.tick_params(axis="y", labelleft=column == 0, labelsize=7.2, length=0)
            ax.axhline(0.5, color="#B5B5B0", linewidth=0.6)
            for spine in ax.spines.values():
                spine.set_color("#9A9A96")
    labels = {1: "1 - It wasn't easy", 4: "4 - Neutral", 7: "7 - It was easy"}
    fig.legend([Patch(facecolor=COLORS[score]) for score in SCALE],
               [labels.get(score, str(score)) for score in SCALE], loc="upper center", ncol=7,
               frameon=True, fancybox=False, edgecolor="#D0D0CC", bbox_to_anchor=(0.5, 0.12),
               fontsize=7, handlelength=1.1, columnspacing=1.1, handletextpad=0.4)
    note = ("Same respondents in both rounds per item; n = matched valid pairs.\n"
            "Project and treatment change between rounds; comparison is descriptive.\n"
            "Time: 1 = insufficient; 7 = sufficient.")
    if not remove_unknown:
        note += " Hatched gray: 4 without justification."
    fig.text(0.5, 0.065, note, ha="center", va="top", fontsize=6, color="#444440", linespacing=1.4)
    save_figure(fig, folder, "rq1_likert_before_after")


def markdown_table(headers, rows):
    return ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)] + [
        "| " + " | ".join(str(v) for v in row) + " |" for row in rows]


def summarize_scope(records, remove_unknown, project=None, condition=None, time=False):
    subset = [r for r in records if (r["item_index"] == 8 if time else r["item_index"] <= 7)
              and (project is None or r["project"] == project)
              and (condition is None or r["condition"] == condition)]
    return summarize(subset, remove_unknown)


def render_latex(folder, name, distributions):
    lookup = {(d["item_index"], d["project"], d["condition"]): d for d in distributions}
    lines = [r"\begin{table}[t]", r"\centering",
             r"\caption{Ratings 5--7 as a percentage of valid responses per item; valid $n$ in parentheses. N.A and missing responses are excluded.}",
             rf"\label{{tab:rq1-crossover-{name.replace('_', '-')}}}", r"\scriptsize",
             r"\setlength{\tabcolsep}{3pt}", r"\begin{tabular}{p{0.34\columnwidth}rrrr}", r"\hline",
             r"\textbf{Item} & \multicolumn{2}{c}{\textbf{M / Round 1}} & \multicolumn{2}{c}{\textbf{N / Round 2}} \\",
             r" & Map. & Ad hoc & Map. & Ad hoc \\", r"\hline"]
    for item, label in enumerate(ITEMS, 1):
        cells = []
        for project, condition in (("M", "mapping"), ("M", "ad_hoc"), ("N", "mapping"), ("N", "ad_hoc")):
            stats = lookup[item, project, condition]
            cells.append(f"{stats['pct_above4']:.0f}\\% ({stats['n_valid']})" if stats["n_valid"] else "-- (0)")
        lines.append(label.replace("&", r"\&") + " & " + " & ".join(cells) + r" \\")
    lines += [r"\hline", r"\end{tabular}", r"\end{table}"]
    (folder / "table_rq1_crossover.tex").write_text("\n".join(lines) + "\n")


def results_text(name, records, profiles, distributions, pairs, remove_unknown):
    overall = summarize_scope(records, remove_unknown)
    lines = [f"# RQ1 — {TITLES[name]}", "",
             "**Pergunta:** como os participantes percebem a facilidade de especificar Data e Model Stories com mapeamento e ad hoc?", "",
             "Análise descritiva ordinal. As unidades são as respostas por história; 17 participantes têm avaliações, distribuídos em quatro times. As respostas repetidas não são participantes independentes.", "",
             "## Base analisada", "",
             f"Foram incluídas **{overall['n_valid']} avaliações de histórias**, com {overall['n_below4']} notas 1–3, {overall['n_neutral']} notas 4 e {overall['n_above4']} notas 5–7. Os **23 N.A** foram excluídos dos percentuais em ambos os cenários.", "",
             f"Notas 4 sem justificativa mantidas: **{overall['n_unknown_retained']}**; excluídas: **{overall['n_unknown_excluded']}**. Os sete neutros aceitos pelo critério acordado, incluindo B1/3.6 (`No comments`), foram preservados.", "",
             "Os registros originais em branco permanecem ausentes. A3, A4 e D3 não têm avaliações de histórias; entre os outros 17 participantes, D4/2.6 tem marcação ambígua e permanece ausente.", "",
             "## Distribuição por projeto e abordagem", "",
             "A tabela abaixo reúne respostas às sete histórias apenas para descrever o volume observado. Os resultados por item, apresentados em seguida, são a análise central.", ""]
    aggregate = []
    for project in ("M", "N"):
        for condition in ("mapping", "ad_hoc"):
            stats = summarize_scope(records, remove_unknown, project, condition)
            aggregate.append([project, "Mapeamento" if condition == "mapping" else "Ad hoc", stats["n_valid"],
                              display(stats["n_below4"], stats["n_valid"]), display(stats["n_neutral"], stats["n_valid"]),
                              display(stats["n_above4"], stats["n_valid"]), stats["n_not_applicable"], stats["n_unknown_excluded"]])
    lines += markdown_table(["Projeto", "Abordagem", "n válido", "Notas 1–3", "Nota 4", "Notas 5–7", "N.A", "4 excluídos"], aggregate)
    for project in ("M", "N"):
        lines += ["", f"## Projeto {project} — rodada {1 if project == 'M' else 2}", "",
                  "Cada célula apresenta contagem/denominador e percentual de notas **5–7**. Consulte `likert_distributions.csv` para a distribuição completa de 1 a 7 e as exclusões de cada item.", ""]
        rows = []
        for index, item in enumerate(ITEMS, 1):
            selected = {d["condition"]: d for d in distributions if d["project"] == project and d["item_index"] == index}
            m, a = selected["mapping"], selected["ad_hoc"]
            rows.append([item, display(m["n_above4"], m["n_valid"]), display(a["n_above4"], a["n_valid"]),
                         f"{m['n_not_applicable']} / {a['n_not_applicable']}",
                         f"{m['n_unknown_excluded']} / {a['n_unknown_excluded']}"])
        lines += markdown_table(["Item", "Mapeamento: 5–7", "Ad hoc: 5–7", "N.A: map./ad hoc", "4 excluídos: map./ad hoc"], rows)
    collection = {d["condition"]: d for d in distributions if d["project"] == "M" and d["item_index"] == 1}
    lines += ["", "## Leitura dos padrões", "",
              f"Em Data Collection na rodada 1, o mapeamento teve **{display(collection['mapping']['n_above4'], collection['mapping']['n_valid'])}** notas 5–7 e o ad hoc **{display(collection['ad_hoc']['n_above4'], collection['ad_hoc']['n_valid'])}**. Essa diferença é descritiva; os times são diferentes e não se apresenta um teste de efeito da abordagem.", ""]
    for project in ("M", "N"):
        m = summarize_scope(records, remove_unknown, project, "mapping")
        a = summarize_scope(records, remove_unknown, project, "ad_hoc")
        lines.append(f"No conjunto de respostas da rodada {1 if project == 'M' else 2}, as notas 5–7 representam {display(m['n_above4'], m['n_valid'])} com mapeamento e {display(a['n_above4'], a['n_valid'])} no ad hoc. O agrupamento das histórias serve como panorama, não como escore ou teste independente.")
        lines.append("")
    time_m = summarize_scope(records, remove_unknown, "M", time=True)
    time_n = summarize_scope(records, remove_unknown, "N", time=True)
    lines += [f"Para tempo suficiente, as notas 5–7 passaram de **{display(time_m['n_above4'], time_m['n_valid'])}** na rodada 1 para **{display(time_n['n_above4'], time_n['n_valid'])}** na rodada 2. B1/3.8=2, recuperado na imagem complementar, está incluído. Este item não participa da exclusão das 54 notas de facilidade.", "",
              "## Distribuições lado a lado entre rodadas", "",
              "O [Likert antes/depois](rq1_likert_before_after.png), também em [PDF](rq1_likert_before_after.pdf), coloca as rodadas em colunas e as duas sequências de tratamento em linhas. As barras são empilhadas de 0% a 100%, seguindo o formato de comparação temporal da figura de referência.", "",
              "Para cada história e sequência, as duas barras usam exatamente as mesmas pessoas, com resposta válida nas duas rodadas. O denominador pode mudar entre histórias e cenários, mas é igual entre M e N dentro de cada comparação. `before_after_distributions.csv` registra as frequências e a cobertura desse recorte pareado.", "",
              "A abordagem está indicada em cada painel: A/C passam de mapeamento para ad hoc, e B/D fazem o inverso. A figura compara rodadas e projetos diferentes, portanto não é uma comparação pré/pós de uma mesma intervenção para todos. O item de tempo é mostrado separadamente das sete histórias.", "",
              "## Trajetórias entre rodadas", "",
              "O gráfico `rq1_crossover` foi adaptado para categorias medianas observadas. Cada linha fina usa apenas os mesmos tipos de história com resposta válida nas duas rodadas de uma pessoa. As linhas grossas representam a categoria mediana inferior desses resumos por sequência.", ""]
    seq_rows = []
    included = [p for p in profiles if p["trajectory_included"]]
    for sequence in ("MAP->ADHOC", "ADHOC->MAP"):
        selected = [p for p in included if p["sequence"] == sequence]
        seq_rows.append([sequence, len(selected), med_text([p["matched_M_median_lower"] for p in selected]),
                         med_text([p["matched_N_median_lower"] for p in selected]),
                         f"{min(p['matched_story_count'] for p in selected)}–{max(p['matched_story_count'] for p in selected)}"])
    lines += markdown_table(["Sequência", "Participantes com histórias comuns", "Categoria central M", "Categoria central N", "Histórias comuns/pessoa"], seq_rows)
    lines += ["", f"**{len(included)} participantes** têm ao menos um tipo de história válido em ambas as rodadas. D6 tem respostas válidas em cada projeto, mas em tipos de história diferentes, e por isso não entra apenas nessa figura. Pessoas com uma história comum continuam identificadas no CSV; suas trajetórias têm cobertura limitada.", "",
              "O gráfico é complementar: sintetiza conjuntos de histórias, não mede um construto validado de facilidade. Não estima efeito do mapeamento, período ou carryover.", "",
              "## Mudanças ordinais por história", "",
              "A comparação pareada abaixo informa quantas pessoas deram nota maior, igual ou menor na rodada 2 para o mesmo item. O denominador exige ambas as respostas válidas. A abordagem muda entre rodadas e o projeto também.", ""]
    pair_rows = []
    for row in pairs:
        for prefix, sequence in (("mapping_first", "MAP->ADHOC"), ("adhoc_first", "ADHOC->MAP")):
            pair_rows.append([row["item"], sequence, row[f"{prefix}_pairs"], row[f"{prefix}_round2_higher"],
                              row[f"{prefix}_equal"], row[f"{prefix}_round2_lower"]])
    lines += markdown_table(["Item", "Sequência", "Pares", "Rodada 2 maior", "Igual", "Rodada 2 menor"], pair_rows)
    lines += ["", "## Alcance da conclusão", "",
              "Os percentuais descrevem as respostas disponíveis por item e abordagem. Projeto e período estão confundidos: M foi sempre primeiro e N sempre segundo. Os participantes também trabalharam em times, de modo que respostas da mesma pessoa ou do mesmo time não são independentes.", "",
              "Esta análise **não calcula médias, efeitos crossover em pontos ou p-valores**. H₀1 não é testada aqui; não se transfere a decisão inferencial do caso antigo. A comparação dos dois cenários está no `README.md` da pasta superior.", "",
              "Processo, critérios, denominadores, arquivos e verificações: [report.md](report.md).", "",
              "Figuras: [Projeto M](rq1_likert_projectM.png), [Projeto N](rq1_likert_projectN.png), [trajetórias](rq1_crossover.png) e [Likert entre rodadas](rq1_likert_before_after.png), também em PDF."]
    return "\n".join(lines) + "\n"


def report_text(name, input_path, input_hash, script_hash, records, profiles, remove_unknown):
    totals = summarize_scope(records, remove_unknown)
    unknown = Counter(r["participant"] for r in records if r["source_status"] == "neutral_unknown")
    trajectory = [p for p in profiles if p["trajectory_included"]]
    lines = [f"# Processo de análise — {TITLES[name]}", "", f"Data da revisão: {DATE}.", "",
             "## Fonte e rastreabilidade", "",
             "Entrada exclusiva: [RESPOSTAS_ANALISE_1_7_NA.csv](../../from_drive/Data/RESPOSTAS_ANALISE_1_7_NA.csv). O arquivo contém 20 questionários, a página recuperada de B1 e a coluna `recodificacoes_na`, com valores anteriores e razões de tratamento.", "",
             f"SHA-256 da entrada: `{input_hash}`.", "", f"SHA-256 do script: `{script_hash}`.", "",
             "A entrada é lida sem alterações. O CSV OCR original, sua transcrição Markdown e o dashboard não são usados para corrigir ou sobrescrever valores durante a execução.", "",
             "## Delineamento e unidade de análise", "",
             "Cada pessoa respondeu sobre sete tipos de história no projeto M/rodada 1 e no projeto N/rodada 2. A e C usaram mapeamento em M e ad hoc em N; B e D fizeram a sequência contrária. O item de tempo é separado da facilidade.", "",
             "A unidade descritiva central é a resposta de uma pessoa a um tipo de história em um projeto. Há 17 participantes com avaliações e quatro times. As contagens de respostas não são tamanhos amostrais de pessoas independentes.", "",
             "## Tratamento aplicado", "",
             "1. Validar os códigos: somente 1–7, `N.A` ou célula vazia nas respostas fechadas.",
             "2. Excluir `N.A` dos denominadores. São 23 respostas: dez com N/A explícito e treze com declaração de não realização, conforme a recodificação já registrada na cópia de trabalho; vinte eram 4, uma era 3 e duas eram 5.",
             "3. Preservar os sete neutros aceitos pelo critério acordado: seis com comentário sobre a tarefa e B1/3.6, com `No comments`. Esta é uma regra operacional, não uma validação independente da intenção subjetiva.",
             "4. Identificar os 54 indeterminados exclusivamente por: item de facilidade (1–7), resposta fechada igual a 4 e campo aberto correspondente vazio. Comentários gerais não são usados para adivinhar a intenção de um item.",
             ("5. Neste cenário, manter os 54 como categoria 4, com sinalização de interpretação incerta. O hachurado cinza nos gráficos identifica a parcela sem justificativa."
              if not remove_unknown else "5. Neste cenário, excluir somente essas 54 respostas dos cálculos. Os valores de entrada permanecem 4; `responses_used.csv` registra a exclusão de sensibilidade. Não convertê-los em N.A e não excluir as demais respostas de uma pessoa."),
             "6. Manter ausentes as células vazias. A3, A4 e D3 não têm a seção de avaliações e ficam fora dos denominadores. Das 43 células de facilidade vazias na matriz de 20 pessoas, 42 pertencem a esses três questionários e uma é D4/2.6, ambígua na transcrição.",
             "7. Não aplicar a remoção dos 54 ao item 2.8/3.8 (tempo), nem alterar comentários abertos ou os N.A existentes.", "",
             "## Fluxo de contabilização", ""]
    lines += markdown_table(["Conjunto", "Respostas de facilidade"], [
        ["Células possíveis: 20 pessoas × 2 projetos × 7 histórias", 280],
        ["Ausentes dos três participantes sem avaliações", 42],
        ["Célula ambígua entre os 17 participantes com avaliações", 1],
        ["N.A excluídos", 23], ["Notas 4 sem justificativa excluídas", totals["n_unknown_excluded"]],
        ["Incluídas no cenário", totals["n_valid"]], ["Notas 4 incluídas", totals["n_neutral"]]])
    lines += ["", "## Frequências e percentuais", "",
              "Para cada história × projeto × abordagem, contar cada categoria de 1 a 7. O percentual é 100 × contagem da categoria / número de respostas válidas daquele recorte. O denominador nunca inclui N.A, ausentes ou exclusões de sensibilidade; todos são contabilizados separadamente.", "",
              "Notas 1–3 e 5–7 também são somadas como resumos abaixo/acima do ponto 4. A escala completa permanece disponível no CSV e nas barras. Percentuais agregados entre histórias são apenas panoramas das respostas, sem inferência ou suposta independência.", "",
              "Os percentuais têm seis casas decimais nos CSVs, uma casa no texto e arredondamento inteiro nas figuras e na tabela LaTeX. Por arredondamento, os rótulos de uma barra podem somar 99% ou 101%, embora as frequências subjacentes fechem exatamente no denominador.", "",
              "## Como interpretar o cinza e a hachura", "",
              "Nas perguntas de facilidade, os traços diagonais (hachura) identificam a parcela de notas 4 sem justificativa. São os casos de significado indeterminado: o texto disponível não permite distinguir neutralidade de uma possível resposta não se aplica. A hachura sinaliza essa incerteza; os registros mantidos continuam como categoria 4, sem uma nova recodificação para N.A.", "",
              "O cinza liso, nas perguntas de facilidade, identifica os neutros aceitos pelo critério acordado: seis com comentário sobre a tarefa e B1/3.6 com No comments. Essa aceitação é uma regra operacional e não uma verificação independente da intenção subjetiva.", "",
              ("Neste cenário, os 54 casos indeterminados permanecem nos cálculos e podem aparecer hachurados. Quando uma barra combina cinza liso e hachurado, o percentual escrito na categoria 4 representa todos os neutros daquele recorte; somente a parcela sem justificativa recebe os traços."
               if not remove_unknown else "Neste cenário, os 54 casos indeterminados foram excluídos dos cálculos, por isso não aparecem segmentos hachurados. Os neutros aceitos continuam na categoria 4, em cinza liso."), "",
              "A identificação dos 54 foi aplicada somente às sete perguntas de facilidade. No item Sufficient time, as notas 4 são apresentadas em cinza liso, sem aplicar essa classificação pela justificativa. Portanto, o cinza liso desse item não significa que sua intenção tenha sido validada pelo mesmo critério das histórias.", "",
              "## Gráfico Likert entre rodadas", "",
              "O arquivo `rq1_likert_before_after.{pdf,png}` adapta a disposição antes/depois da Figura 7 de `reference_papers/2407.15982v1.pdf`: duas colunas com distribuições de categorias empilhadas de 0% a 100%. A figura organiza as sequências em duas linhas: A/C (mapeamento → ad hoc) e B/D (ad hoc → mapeamento).", "",
              "Para cada item e sequência, selecionar apenas as pessoas com resposta incluída em ambos os projetos, aplicando primeiro as exclusões do cenário. Contar as categorias em cada rodada usando exatamente esse mesmo conjunto de pessoas. Logo, cada par de barras tem o mesmo n e a mesma composição de respondentes. Isso pode produzir denominadores menores que os dos gráficos por projeto, que usam todas as respostas válidas de cada item.", "",
              "`before_after_distributions.csv` registra 32 recortes: duas sequências × oito itens × duas rodadas. As colunas de cobertura distinguem respostas próprias inválidas da exclusão de uma resposta própria válida porque a resposta da outra rodada não é válida. As frequências somam o número de pares válidos. No cenário com os 54, a parte hachurada da categoria 4 identifica justificativas vazias.", "",
              "O item de tempo não é filtrado pelo critério dos 54. Os rótulos identificam rodada, projeto e abordagem; o desenho não é um pré/pós com a mesma intervenção para todos, e a figura não isola causalmente aprendizagem ou efeito das dicas.", "",
              "## Resumos ordinais e trajetórias", "",
              "Ordenar as categorias válidas. Com quantidade ímpar, a categoria central é única. Com quantidade par, registrar as duas categorias centrais (inferior e superior), sem tirar a média entre elas. O gráfico usa a categoria central inferior, sempre uma categoria observada.", "",
              "Para a trajetória de cada pessoa, primeiro intersectar os tipos de história com resposta válida nos dois projetos. Calcular as categorias centrais de M e N apenas nessa mesma interseção. Assim, a trajetória não compara cestas diferentes dentro de uma pessoa. Não se exige artificialmente um mínimo de quatro respostas; o número efetivo de histórias é informado.", "",
              f"Nesta execução, {len(trajectory)} pessoas têm histórias comuns. D6 não possui tipos válidos em comum entre M e N. Isso o exclui apenas da figura de trajetórias, preservando suas avaliações nos gráficos e tabelas por item.", "",
              "As linhas grossas usam a categoria central inferior das categorias inferiores por pessoa, dando o mesmo peso a cada pessoa da sequência. Esta síntese é complementar; não constitui escore psicométrico nem efeito causal. O arquivo também guarda os limites centrais superiores para tornar a escolha explícita.", "",
              "A tabela pareada por história conta somente direções (maior/igual/menor), sem subtrair categorias ou assumir distâncias iguais. Não são reaplicados testes por permutação sobre médias, estimativas em pontos, testes de carryover nem decisões sobre H₀1.", "",
              "## Sensibilidade e limites", "",
              "Os 54 indeterminados se dividem em 31 respostas com mapeamento e 23 ad hoc. A exclusão reduz os denominadores de forma desigual e seleciona somente a categoria 4. Por construção, os números de notas 1–3 e 5–7 permanecem iguais, mas seus percentuais aumentam. Essa mudança não representa nova melhora observada.", "",
              "Projeto e rodada coincidem; não é possível separar aprendizado de dificuldade do projeto por esta descrição. A troca de abordagem, a dependência entre respostas de uma pessoa, a colaboração em quatro times, a cobertura desigual dos itens e a recodificação posterior de N.A limitam conclusões causais.", "",
              "## Auditoria dos 54 registros", ""]
    lines += markdown_table(["Participante", "Notas 4 sem justificativa"], sorted(unknown.items()))
    lines += ["", "## Arquivos e nomes preservados", "",
              "- `results.md`: resultados descritivos e limites de interpretação.",
              "- `report.md`: processo de análise e rastreabilidade.",
              "- `participant_means.csv`: nome histórico preservado; contém contagens e categorias centrais, **não médias**. Inclui os 20 IDs e indicadores de elegibilidade e participação na trajetória.",
              "- `crossover_by_story.csv`: nome histórico preservado; contém pares válidos, direções de mudança e categorias centrais por sequência, **não efeitos crossover**.",
              "- `table_rq1_crossover.tex`: nome histórico preservado; tabela de percentuais de notas 5–7 e denominadores por item/projeto/abordagem.",
              "- `rq1_likert_projectM.{pdf,png}` e `rq1_likert_projectN.{pdf,png}`: mesmas famílias, ordem de itens, paleta e formato lado a lado dos gráficos anteriores; denominador por linha e exclusões atualizadas.",
              "- `rq1_crossover.{pdf,png}`: mesmo formato de linhas por pessoa e sequência, adaptado para categorias centrais de histórias pareadas. Os rótulos e a anotação deixam de usar médias e p-valores.",
              "- `rq1_likert_before_after.{pdf,png}`: barras 100% empilhadas lado a lado por rodada, em dois blocos de sequência de tratamento, com as mesmas pessoas por item.",
              "- `before_after_distributions.csv`: frequências completas e cobertura dos pares usados no novo Likert entre rodadas.",
              "- `likert_distributions.csv`: contagens completas, percentuais, N.A, ausentes e cobertura dos 32 recortes (8 itens × 2 projetos × 2 abordagens).",
              "- `responses_used.csv`: 320 registros (20 pessoas × 2 projetos × 8 itens), com valor de entrada, uso/exclusão, justificativa e rastreabilidade dos N.A. Não contém nomes ou e-mails.", "",
              "## Reprodução e verificações", "", "```sh", ".venv/bin/python analysis_rq1.py", "```", "",
              "O comando recria ambos os cenários e a comparação na pasta `rq1/`. Use `--output-root` para gerar em outra pasta e `--data` para explicitar uma cópia de trabalho compatível.", "",
              "Verificações automáticas: soma das categorias igual ao denominador; fechamento entre respostas esperadas e todas as exclusões; 214 respostas com os 54 versus 160 sem eles; diferença exata de 54; 23 N.A em ambos; sete neutros aceitos preservados; contagens não neutras idênticas; item de tempo idêntico; categorias medianas pertencentes a 1–7; mesmos respondentes e n nas duas barras de cada comparação do novo Likert; ausência de e-mails nos arquivos gerados; SHA-256 da entrada inalterado.", "",
              "As figuras em PDF e PNG são geradas a partir das mesmas contagens. O Markdown e a tabela LaTeX usam as mesmas distribuições estruturadas. A inspeção visual de entrega complementa as verificações numéricas.", "",
              "Os arquivos legados diretos de `rq1/` foram substituídos pelos dois cenários. O manuscrito e suas cópias antigas em `tex/images/` permanecem fora do escopo desta execução; não devem ser confundidos com estas novas análises."]
    return "\n".join(lines) + "\n"


def run_scenario(folder, name, people, records, remove_unknown, data_path, input_hash, script_hash):
    folder.mkdir(parents=True, exist_ok=True)
    distributions = []
    for project, period in (("M", 1), ("N", 2)):
        for condition in ("mapping", "ad_hoc"):
            for index, item in enumerate(ITEMS, 1):
                subset = [r for r in records if r["project"] == project and r["condition"] == condition and r["item_index"] == index]
                distributions.append(dict(project=project, period=period, condition=condition,
                                          item_index=index, item=item, **summarize(subset, remove_unknown)))
    profiles = participant_rows(people, remove_unknown)
    pairs = paired_story_rows(people, remove_unknown)
    before_after = before_after_distributions(people, remove_unknown)
    for row in before_after:
        prefix = "mapping_first" if row["sequence"] == "MAP->ADHOC" else "adhoc_first"
        assert row["n_pairs"] == pairs[row["item_index"] - 1][f"{prefix}_pairs"]
    audit_rows = []
    for r in records:
        use = kept(r, remove_unknown)
        status = "participant_without_ratings" if not r["participant_eligible"] else (
            "excluded_unknown_neutral" if remove_unknown and r["source_status"] == "neutral_unknown" else r["source_status"])
        audit_rows.append({k: r[k] for k in ("participant", "group", "sequence", "project", "period", "item_index", "item", "field", "condition", "input_value", "source_status", "participant_eligible", "justification", "original_before_na", "recoding_reason")} |
                          dict(included=use, analysis_status=status, analysis_value=r["value"] if use else ""))
    write_csv(folder / "likert_distributions.csv", distributions)
    write_csv(folder / "participant_means.csv", profiles)
    write_csv(folder / "crossover_by_story.csv", pairs)
    write_csv(folder / "responses_used.csv", audit_rows)
    write_csv(folder / "before_after_distributions.csv", before_after)
    render_latex(folder, name, distributions)
    fig_likert(distributions, people, folder, "M", remove_unknown)
    fig_likert(distributions, people, folder, "N", remove_unknown)
    fig_crossover(profiles, folder)
    fig_likert_before_after(before_after, folder, remove_unknown)
    (folder / "results.md").write_text(results_text(name, records, profiles, distributions, pairs, remove_unknown))
    (folder / "report.md").write_text(report_text(name, data_path, input_hash, script_hash, records, profiles, remove_unknown))
    return dict(distributions=distributions, profiles=profiles, audit=audit_rows,
                summary=summarize_scope(records, remove_unknown))


def compare(output_root, analyses, records):
    keep, drop = analyses["com_54"], analyses["sem_54"]
    assert keep["summary"]["n_valid"] == 214 and drop["summary"]["n_valid"] == 160
    assert keep["summary"]["n_neutral"] == 61 and drop["summary"]["n_neutral"] == 7
    assert keep["summary"]["n_not_applicable"] == drop["summary"]["n_not_applicable"] == 23
    assert keep["summary"]["n_below4"] == drop["summary"]["n_below4"] == 38
    assert keep["summary"]["n_above4"] == drop["summary"]["n_above4"] == 115
    changed = [(a, b) for a, b in zip(keep["audit"], drop["audit"]) if a["included"] != b["included"]]
    assert len(changed) == 54 and all(a["source_status"] == "neutral_unknown" and a["included"] and not b["included"] for a, b in changed)
    comparisons = []
    for a, b in zip(keep["distributions"], drop["distributions"]):
        assert all(a[k] == b[k] for k in ("project", "condition", "item_index", "n_expected", "n_not_applicable", "n_missing", "n_below4", "n_above4"))
        assert a["n_valid"] - b["n_valid"] == b["n_unknown_excluded"]
        if a["item_index"] == 8:
            assert a == b
        comparisons.append(dict(project=a["project"], condition=a["condition"], item=a["item"],
                                n_com_54=a["n_valid"], n_sem_54=b["n_valid"],
                                unknown_removed=b["n_unknown_excluded"], n_above4_both=a["n_above4"],
                                pct_above4_com_54=a["pct_above4"], pct_above4_sem_54=b["pct_above4"],
                                percentage_point_change=round(b["pct_above4"] - a["pct_above4"], 6)))
    write_csv(output_root / "scenario_comparison.csv", comparisons)
    lines = ["# RQ1 — dois cenários de tratamento dos neutros", "",
             "Análise descritiva ordinal, usando exclusivamente `from_drive/Data/RESPOSTAS_ANALISE_1_7_NA.csv`. Os resultados antigos diretos desta pasta foram substituídos. Os arquivos de origem não foram alterados.", "",
             "| Cenário | Avaliações de histórias | Notas 4 incluídas | N.A excluídos | Resultados | Processo |",
             "|---|---:|---:|---:|---|---|",
             "| Mantendo os 54 sem justificativa | 214 | 61 (7 aceitos + 54 indeterminados) | 23 | [results.md](com_54/results.md) | [report.md](com_54/report.md) |",
             "| Excluindo os 54 sem justificativa | 160 | 7 aceitos | 23 | [results.md](sem_54/results.md) | [report.md](sem_54/report.md) |", "",
             "## Comparação dos cenários", "",
             "Os números de respostas 1–3 (38) e 5–7 (115) são iguais nos dois cenários. A exclusão muda os denominadores e a composição dos pares, não acrescenta avaliações positivas ou negativas. Os 54 excluídos se dividem em 31 com mapeamento e 23 ad hoc.", "",
             "A tabela abaixo reúne respostas às sete histórias como panorama descritivo; não representa 214 ou 160 participantes independentes.", ""]
    table = []
    for project in ("M", "N"):
        for condition in ("mapping", "ad_hoc"):
            a = summarize_scope(records, False, project, condition)
            b = summarize_scope(records, True, project, condition)
            table.append([project, "Mapeamento" if condition == "mapping" else "Ad hoc",
                          display(a["n_above4"], a["n_valid"]), display(b["n_above4"], b["n_valid"]), b["n_unknown_excluded"]])
    lines += markdown_table(["Projeto", "Abordagem", "Notas 5–7: mantendo 54", "Notas 5–7: excluindo 54", "4 removidos"], table)
    lines += ["", "No projeto N, a ordenação dos percentuais agregados entre abordagens muda entre cenários. Isso mostra sensibilidade à escolha dos denominadores; não demonstra uma mudança causal na facilidade. Avalie os resultados por história e reporte os dois cenários.", "",
              "`scenario_comparison.csv` permite comparar as distribuições por item. O item de tempo permanece idêntico em ambos os cenários.", "",
              "## Arquivos preservados em cada cenário", "",
              "Cada pasta contém os dez nomes de arquivo da análise anterior, adaptados para resumos ordinais, mais `report.md`, `likert_distributions.csv`, `responses_used.csv`, `before_after_distributions.csv` e o novo Likert entre rodadas. Os nomes históricos `participant_means`, `crossover_by_story` e `table_rq1_crossover` foram mantidos para organização; os conteúdos não apresentam médias ou efeitos crossover.", "",
              "Há quatro conjuntos de figuras em PDF e PNG: distribuição por projeto M, distribuição por projeto N, trajetórias entre rodadas e barras Likert antes/depois. O gráfico de trajetórias usa categorias medianas inferiores de histórias pareadas; não reaproveita p-valores antigos.", "",
              "O novo Likert coloca as rodadas lado a lado e separa as duas sequências de tratamento, usando as mesmas pessoas por história: [com os 54](com_54/rq1_likert_before_after.png) e [sem os 54](sem_54/rq1_likert_before_after.png). Os painéis indicam as abordagens invertidas entre rodadas; a comparação é descritiva.", "",
              "## Reprodução", "", "```sh", ".venv/bin/python analysis_rq1.py", "```", "",
              "O manuscrito em `tex/sections/04-experimental_results.tex` e as imagens antigas em `tex/images/` não foram reescritos nesta tarefa. Eles ainda descrevem a análise anterior e precisam de atualização própria antes de uso no artigo."]
    (output_root / "README.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=HERE / "from_drive/Data/RESPOSTAS_ANALISE_1_7_NA.csv")
    parser.add_argument("--output-root", type=Path, default=HERE / "rq1")
    args = parser.parse_args()
    input_hash = digest(args.data)
    script_hash = digest(Path(__file__))
    people, records = load(args.data)
    args.output_root.mkdir(parents=True, exist_ok=True)
    analyses = {name: run_scenario(args.output_root / name, name, people, records, remove,
                                   args.data, input_hash, script_hash)
                for name, remove in SCENARIOS.items()}
    compare(args.output_root, analyses, records)
    assert digest(args.data) == input_hash, "The working CSV changed during analysis"
    for folder in args.output_root.iterdir():
        if folder.is_dir() and folder.name in SCENARIOS:
            for file in folder.iterdir():
                if file.suffix in {".csv", ".md", ".tex"}:
                    assert "@" not in file.read_text(encoding="utf-8-sig"), file
    print(json.dumps({"output_root": str(args.output_root), "source_sha256": input_hash,
                      "scenarios": {name: {"story_ratings": analysis["summary"]["n_valid"],
                                           "neutral_ratings": analysis["summary"]["n_neutral"],
                                           "na_excluded": analysis["summary"]["n_not_applicable"],
                                           "unknown_excluded": analysis["summary"]["n_unknown_excluded"]}
                                    for name, analysis in analyses.items()}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
