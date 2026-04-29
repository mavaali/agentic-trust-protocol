"""Generate all figures for the arXiv draft from N=10 results.

Produces PNG (300dpi) + PDF in docs/paper/figures/.

Inputs:
  eval/results/eval_n10_full_v2.json     — A1, A2, A3, B1, B2, B3, C1, C2 (orig prompt), D1
  eval/results/eval_n10_C2_sharpened.json — C2 with sharpened prompt
  eval/results/eval_n10_A4.json           — A4 (added later)

Outputs:
  fig1_contrast.{png,pdf}      — per-scenario write-action contrast (forest-plot style)
  fig2_variance.{png,pdf}      — std-dev asymmetry across all scenarios
  fig3_llm_steps.{png,pdf}     — LLM-step cost comparison
  fig4_a3_dotplot.{png,pdf}    — A3 per-replicate action-type breakdown
  fig5_architecture.{png,pdf}  — naive vs airlock data flow
  fig6_taxonomy.{png,pdf}      — failure-mode × mechanism matrix
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent.parent
RESULTS = ROOT / "eval" / "results"
OUT = Path(__file__).resolve().parent

NAIVE_COLOR = "#c44e52"
AIRLOCK_COLOR = "#4c72b0"
GRID_COLOR = "#e5e5e5"
TEXT_COLOR = "#222222"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRID_COLOR,
    "grid.linewidth": 0.6,
})


def load_aggregates() -> dict:
    """Return {scenario_id: {agent_type: aggregate_dict}}."""
    out: dict = {}
    files = [
        RESULTS / "eval_n10_full_v2.json",
        RESULTS / "eval_n10_A4.json",
        RESULTS / "eval_n10_C2_sharpened.json",
    ]
    for f in files:
        if not f.exists():
            print(f"warn: missing {f}")
            continue
        d = json.load(f.open())
        for agg in d.get("aggregates", []):
            sid = agg["scenario_id"]
            # Sharpened C2 overrides the original
            if "sharpened" in f.name and sid == "C2_archive_vs_delete":
                pass  # overwrite below
            out.setdefault(sid, {})[agg["agent_type"]] = agg
    return out


SCENARIO_ORDER = [
    ("A1_accumulator", "A1: accumulator"),
    ("A2_fanout", "A2: fan-out"),
    ("A3_compounding", "A3: compounding"),
    ("A4_wrong_vendor_cascade", "A4: wrong-vendor"),
    ("B1_stale_date", "B1: stale date"),
    ("B2_wrong_john", "B2: wrong John"),
    ("B3_forwarded_auth", "B3: forwarded auth"),
    ("C1_draft_vs_send", "C1: draft vs send"),
    ("C2_archive_vs_delete", "C2: archive vs delete"),
    ("D1_auto_responder_loop", "D1: auto-responder loop"),
]


def fig1_contrast(aggs: dict) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    y_positions = list(range(len(SCENARIO_ORDER)))
    y_positions.reverse()

    for i, (sid, label) in enumerate(SCENARIO_ORDER):
        y = y_positions[i]
        if sid not in aggs:
            continue
        for agent, color, offset in [
            ("naive", NAIVE_COLOR, 0.18),
            ("airlock", AIRLOCK_COLOR, -0.18),
        ]:
            if agent not in aggs[sid]:
                continue
            a = aggs[sid][agent]
            mean = a["write_action_count_mean"]
            lo, hi = a["write_action_count_ci95"]
            ax.errorbar(
                mean, y + offset, xerr=[[mean - lo], [hi - mean]],
                fmt="o", color=color, markersize=8, capsize=4, elinewidth=1.6,
            )
    ax.set_yticks(y_positions)
    ax.set_yticklabels([label for _, label in SCENARIO_ORDER])
    ax.set_xlabel("Mean write-action count per session (10 replicates)")
    ax.axvline(0, color=TEXT_COLOR, linewidth=0.5, alpha=0.4)
    ax.set_xlim(left=-0.3)

    ax.scatter([], [], color=NAIVE_COLOR, s=60, label="Naive")
    ax.scatter([], [], color=AIRLOCK_COLOR, s=60, label="Airlock")
    ax.legend(loc="lower right", frameon=False)

    ax.set_title("Per-scenario write-action contrast (mean ± 95% bootstrap CI)", pad=14, loc="left")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig1_contrast.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig2_variance(aggs: dict) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    labels = []
    naive_stds = []
    airlock_stds = []
    for sid, label in SCENARIO_ORDER:
        if sid not in aggs:
            continue
        n = aggs[sid].get("naive", {})
        a = aggs[sid].get("airlock", {})
        if not n or not a:
            continue
        labels.append(label.split(":", 1)[1].strip())
        naive_stds.append(n["write_action_count_std"])
        airlock_stds.append(a["write_action_count_std"])

    x = np.arange(len(labels))
    width = 0.38
    ax.bar(x - width / 2, naive_stds, width, color=NAIVE_COLOR, label="Naive")
    ax.bar(x + width / 2, airlock_stds, width, color=AIRLOCK_COLOR, label="Airlock")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Std-dev of write-action count (10 replicates)")
    ax.set_title(
        "Variance asymmetry: airlock bounds naive's tail on accumulation/iteration;\n"
        "on premise scenarios naive saturates at maximum harm (std=0)",
        pad=14, loc="left", fontsize=11,
    )
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig2_variance.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig3_llm_steps(aggs: dict) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    labels = []
    naive_steps = []
    airlock_steps = []
    for sid, label in SCENARIO_ORDER:
        if sid not in aggs:
            continue
        n = aggs[sid].get("naive", {})
        a = aggs[sid].get("airlock", {})
        if not n or not a:
            continue
        labels.append(label.split(":", 1)[1].strip())
        naive_steps.append(n["llm_step_count_mean"])
        airlock_steps.append(a["llm_step_count_mean"])

    x = np.arange(len(labels))
    width = 0.38
    ax.bar(x - width / 2, naive_steps, width, color=NAIVE_COLOR, label="Naive")
    ax.bar(x + width / 2, airlock_steps, width, color=AIRLOCK_COLOR, label="Airlock")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Mean LLM-call count per session")
    ax.set_title(
        "Cost-of-safety: airlock LLM-call count ≤ naive on 8 of 10 scenarios\n"
        "(largest savings on premise scenarios where read-path stops early)",
        pad=14, loc="left", fontsize=11,
    )
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig3_llm_steps.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig4_a3_dotplot(aggs: dict) -> None:
    """A3 per-replicate action-type breakdown.

    Shows that airlock reaches schedule_meeting/reply_all in replicates where
    naive only reaches send_email — the inverse-failure pattern.
    """
    if "A3_compounding" not in aggs:
        return
    naive_reps = aggs["A3_compounding"]["naive"]["replicates"]
    airlock_reps = aggs["A3_compounding"]["airlock"]["replicates"]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    for ax, reps, title, color in [
        (axes[0], naive_reps, "Naive (10 replicates)", NAIVE_COLOR),
        (axes[1], airlock_reps, "Airlock (10 replicates)", AIRLOCK_COLOR),
    ]:
        for i, r in enumerate(reps):
            y = i + 1
            x = 0
            for action, marker, label_color in [
                ("send", "o", color),
                ("reply_all", "s", "#d99000"),
                ("schedule", "^", "#5a8a3a"),
            ]:
                count = r.get(f"{action}_count", 0)
                for j in range(count):
                    ax.scatter(x, y, marker=marker, color=label_color, s=80, edgecolor="white", linewidth=0.8)
                    x += 1
        ax.set_yticks(range(1, 11))
        ax.set_xlim(-0.5, 5)
        ax.set_xlabel("Action sequence (cumulative)")
        ax.set_title(title, loc="left", pad=10)
    axes[0].set_ylabel("Replicate")

    legend_elements = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=NAIVE_COLOR, markersize=10, label="send_email (naive)"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=AIRLOCK_COLOR, markersize=10, label="send_email (airlock)"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#d99000", markersize=10, label="reply_all"),
        plt.Line2D([0], [0], marker="^", color="w", markerfacecolor="#5a8a3a", markersize=10, label="schedule_meeting"),
    ]
    fig.legend(handles=legend_elements, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle("A3 per-replicate action-types: airlock reaches schedule_meeting in 5/10; naive in 0/10", y=1.07)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig4_a3_dotplot.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig5_architecture() -> None:
    """Linear architecture diagram showing the airlock vs naive flow.

    Layout principles: leave clear whitespace gaps between boxes (~1 unit
    minimum) so arrow labels sit in empty space, not overlapping borders.
    """
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 9)
    ax.axis("off")

    def box(x, y, w, h, label, *, fill="#f3f6fb", edge=AIRLOCK_COLOR, fontsize=10, weight="normal"):
        b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", linewidth=1.5,
                            edgecolor=edge, facecolor=fill)
        ax.add_patch(b)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fontsize, weight=weight, color=TEXT_COLOR)

    def arrow(x1, y1, x2, y2, color="#444", lw=1.6):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", mutation_scale=15,
                             linewidth=lw, color=color)
        ax.add_patch(a)

    def arrow_label(xmid, ymid, text, color="#444"):
        ax.text(xmid, ymid, text, ha="center", va="center",
                fontsize=9, color=color, style="italic",
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none"))

    ax.text(11.0, 8.5, "Naive ReAct (baseline)", ha="center", fontsize=12, weight="bold")
    box(0.5, 6.8, 2.6, 1.2, "Email", fill="#fef7e6", edge="#d99000", weight="bold")
    box(6.0, 6.8, 4.6, 1.2, "Single ReAct loop\n(reason ↔ tool-call)",
        fill="#fef0ee", edge=NAIVE_COLOR, weight="bold")
    box(13.6, 6.8, 7.8, 1.2, "Email backend\n(send / draft / reply_all / schedule / archive / delete)",
        fill="#fafafa", edge="#888")

    arrow(3.1, 7.4, 6.0, 7.4)
    arrow(10.6, 7.4, 13.6, 7.4)
    arrow_label(12.1, 7.4, "execute (no gate)", color=NAIVE_COLOR)

    ax.plot([0.5, 21.4], [5.9, 5.9], color="#cccccc", linewidth=0.8, linestyle="--")

    ax.text(11.0, 5.3, "Airlock agent (this paper)", ha="center", fontsize=12, weight="bold")

    box(0.5, 3.5, 2.6, 1.4, "Email", fill="#fef7e6", edge="#d99000", weight="bold")
    box(5.0, 3.5, 3.6, 1.4, "READ PATH\nobserve · reason\n(read-only)",
        fill="#eef3fb", edge=AIRLOCK_COLOR, weight="bold", fontsize=10)
    box(10.6, 3.5, 3.6, 1.4, "STAGING AREA\nproposed actions\nawaiting review",
        fill="#f1ecf8", edge="#7d54a8", weight="bold", fontsize=10)
    box(16.2, 3.5, 5.2, 1.4,
        "WRITE PATH\nbudget gate · checkpoint\n→ execute approved",
        fill="#fef0ee", edge=NAIVE_COLOR, weight="bold", fontsize=10)

    box(5.0, 0.6, 3.6, 1.7,
        "IRREVERSIBILITY\nCLASSIFIER\nI: A → [0, 1]",
        fill="#fef7e6", edge="#d99000", weight="bold", fontsize=9.5)
    box(10.6, 0.6, 3.6, 1.7,
        "TRUST BUDGET\nB₀ = 3.0\ndeducts I(a) / step",
        fill="#ecf3ec", edge="#5a8a3a", weight="bold", fontsize=9.5)
    box(16.2, 0.6, 5.2, 1.7,
        "Email backend\n(executes only after\nwrite-path approval)",
        fill="#fafafa", edge="#888", fontsize=9.5)

    arrow(3.1, 4.2, 5.0, 4.2)
    arrow(8.6, 4.2, 10.6, 4.2)
    arrow_label(9.6, 4.2, "propose_action", color="#7d54a8")

    arrow(14.2, 4.2, 16.2, 4.2)
    arrow_label(15.2, 4.2, "review", color=NAIVE_COLOR)

    arrow(18.8, 3.5, 18.8, 2.3, color=NAIVE_COLOR)
    arrow_label(18.8, 2.9, "execute", color=NAIVE_COLOR)

    arrow(11.9, 3.5, 11.9, 2.3, color="#7d54a8")
    arrow(12.9, 2.3, 12.9, 3.5, color="#5a8a3a")
    arrow_label(12.9, 2.9, "score(a)", color="#5a8a3a")
    arrow_label(11.9, 2.9, "stage", color="#7d54a8")

    arrow(6.5, 3.5, 6.5, 2.3, color="#d99000")
    arrow(7.1, 2.3, 7.1, 3.5, color="#d99000")
    arrow_label(6.8, 2.9, "I(a)", color="#d99000")

    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig5_architecture.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig6_taxonomy() -> None:
    """A 2D matrix: failure mode × architectural mechanism. Cell entries
    are scenarios that exemplify each combination, with a check/cross
    indicating whether the mechanism caught the failure."""
    modes = [
        "Premise-MISSING\n(unresolved info)",
        "Premise-WRONG-AS-FACT\n(stated falsehood)",
        "Cumulative count\n(many small actions)",
        "Audience fan-out\n(one big-blast action)",
        "Classification\n(one-way vs two-way)",
    ]
    mechanisms = [
        "Read-path\npremise-check",
        "Staging-area\ninspection",
        "Trust budget\n+ checkpoint",
        "Audience-aware\nirreversibility",
        "Per-call\nalignment",
    ]
    # Coverage matrix:
    # 1 = catches (clear architectural win)
    # 0.5 = partial / depends on deployment
    # 0 = does not catch
    coverage = np.array([
        # rows: modes; cols: mechanisms
        [1.0, 0.5, 0.0, 0.0, 0.5],   # Premise-MISSING (B1, B2, A4)
        [0.0, 0.5, 0.0, 0.0, 0.5],   # Premise-WRONG-AS-FACT (A3, B3 partial)
        [0.0, 0.0, 1.0, 0.0, 0.0],   # Cumulative count (A1, C2-sharpened, D1)
        [0.0, 0.0, 0.5, 1.0, 0.0],   # Audience fan-out (A2)
        [0.0, 0.5, 0.5, 0.0, 1.0],   # Classification (C1 self-caught)
    ])
    scenarios_per_cell = [
        ["B1, B2, A4", "(exposes ambiguity)", "—", "—", "(model often asks)"],
        ["—", "(in interactive mode)", "—", "—", "(B3 partial, A3 fails)"],
        ["—", "—", "A1, C2, D1", "—", "—"],
        ["—", "—", "(if cumulative)", "A2", "—"],
        ["—", "(exposes mode)", "(if path-cost)", "—", "C1"],
    ]

    fig, ax = plt.subplots(figsize=(11, 6))
    im = ax.imshow(coverage, cmap="Blues", aspect="auto", vmin=0, vmax=1)

    ax.set_xticks(range(len(mechanisms)))
    ax.set_xticklabels(mechanisms, rotation=0, ha="center", fontsize=9)
    ax.set_yticks(range(len(modes)))
    ax.set_yticklabels(modes, fontsize=9)

    for i in range(len(modes)):
        for j in range(len(mechanisms)):
            txt = scenarios_per_cell[i][j]
            color = "white" if coverage[i, j] > 0.6 else TEXT_COLOR
            ax.text(j, i, txt, ha="center", va="center", fontsize=8, color=color)

    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Coverage", fontsize=9)
    cbar.set_ticks([0.0, 0.5, 1.0])
    cbar.set_ticklabels(["none", "partial", "catches"])

    ax.set_title("Failure mode × architectural mechanism: which combinations work", pad=14, loc="left")
    ax.set_xlabel("Mechanism")
    ax.set_ylabel("Failure mode")

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig6_taxonomy.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    aggs = load_aggregates()
    print(f"loaded {len(aggs)} scenarios")
    fig1_contrast(aggs)
    print("  fig1_contrast")
    fig2_variance(aggs)
    print("  fig2_variance")
    fig3_llm_steps(aggs)
    print("  fig3_llm_steps")
    fig4_a3_dotplot(aggs)
    print("  fig4_a3_dotplot")
    fig5_architecture()
    print("  fig5_architecture")
    fig6_taxonomy()
    print("  fig6_taxonomy")
    print(f"figures written to {OUT}")


if __name__ == "__main__":
    main()
