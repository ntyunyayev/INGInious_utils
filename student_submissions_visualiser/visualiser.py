#!/usr/bin/env python3
"""Visualise student submissions from an INGInious export CSV."""

import sys
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

DEFAULT_CSV = "../export.csv"
DEFAULT_COURSE = "../course.yaml"
OUTPUT_PDF = "submissions_overview.pdf"

# Colour palette (muted, colour-blind friendly)
C_ATTEMPTS = "#5a7db5"
C_SUCCESSES = "#6ab87a"


INCLUDED_SECTIONS = {
    "S1 - Introduction Assembleur",
    "S2 - Assembleur: Conditions & Boucles",
    "S3 - Assembleur: Tableaux & Chaînes de charactères",
    "S4 - Assembleur: Fonctions & Procédures",
    "S5 - Assembleur: Fonctions avancées",
}


def load_toc(course_path):
    """Parse course.yaml and return (ordered_tasks, section_for_task).

    ordered_tasks: list of task ids in course order
    section_for_task: dict mapping task id -> section title
    """
    with open(course_path) as f:
        course = yaml.safe_load(f)

    toc = course["dispenser_data"]["toc"]
    ordered_tasks = []
    section_for_task = {}
    for section in toc:
        title = section["title"]
        if title not in INCLUDED_SECTIONS:
            continue
        tasks = section.get("tasks_list", [])
        for t in tasks:
            section_for_task[t] = title
        ordered_tasks.extend(tasks)
    return ordered_tasks, section_for_task


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    # username column contains stringified lists like "['Alice']" – extract the name
    df["username"] = df["username"].str.strip("[]'\" ")
    return df


def build_stats(df):
    """Return a DataFrame with per-exercise stats."""
    stats = df.groupby("taskid").agg(
        attempts=("result", "size"),
        successes=("result", lambda x: (x == "success").sum()),
    )
    return stats


def plot(stats, ordered_tasks, section_for_task, output_pdf):
    # Keep only tasks that appear in both the toc and the CSV
    tasks_in_order = [t for t in ordered_tasks if t in stats.index]
    stats = stats.loc[tasks_in_order]

    # Compute section boundaries after filtering
    section_boundaries = []
    prev_section = None
    for i, t in enumerate(tasks_in_order):
        sec = section_for_task[t]
        if sec != prev_section:
            section_boundaries.append((sec, i))
            prev_section = sec

    # Reverse so the first exercise in the course is at the top of the chart
    stats = stats.iloc[::-1]
    tasks_in_order = tasks_in_order[::-1]

    exercises = stats.index
    n = len(exercises)
    y = np.arange(n)
    bar_height = 0.3
    max_val = stats["attempts"].max()

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 12,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })

    fig, ax = plt.subplots(figsize=(14, max(7, n * 0.5)))
    fig.patch.set_facecolor("#fafafa")
    ax.set_facecolor("#fafafa")

    # Subtle horizontal grid behind bars
    ax.xaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.4)
    ax.set_axisbelow(True)

    bars_attempts = ax.barh(y + bar_height / 2, stats["attempts"], bar_height,
                            label="Attempts", color=C_ATTEMPTS, edgecolor="white",
                            linewidth=0.5, zorder=2)
    bars_successes = ax.barh(y - bar_height / 2, stats["successes"], bar_height,
                             label="Successes", color=C_SUCCESSES, edgecolor="white",
                             linewidth=0.5, zorder=2)

    ax.set_yticks(y)
    ax.set_yticklabels(exercises, fontsize=11)
    ax.set_xlabel("Count", fontsize=13, labelpad=8)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_title("Submissions overview per exercise", fontsize=16,
                 fontweight="bold", pad=14)

    # Draw horizontal separators and section labels between weeks
    # section_boundaries indices are in the original (top-to-bottom) order;
    # after reversal the y position needs to be flipped.
    for title, orig_start in section_boundaries:
        # In the reversed array the section starts at (n - 1 - orig_start)
        # and the separator line goes just above it (higher y = further up).
        sep_y = (n - 1 - orig_start) + 0.45
        if sep_y < n - 0.5:
            ax.axhline(sep_y, color="#888888", linewidth=0.6, linestyle="--", zorder=1)
        # Place the section title to the right
        ax.text(max_val * 1.05, sep_y - 0.1, title,
                fontsize=10, fontstyle="italic", color="#555555",
                va="top", clip_on=False)

    # Value labels
    for bars in (bars_attempts, bars_successes):
        for bar in bars:
            width = bar.get_width()
            ax.text(width + max_val * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(width)}", va="center", fontsize=10, color="#333333")

    ax.legend(loc="lower right", frameon=True, fancybox=True, shadow=False,
              framealpha=0.9, fontsize=11)

    plt.tight_layout()
    fig.savefig(output_pdf, format="pdf", bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved to {output_pdf}")


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    course_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_COURSE
    output_pdf = sys.argv[3] if len(sys.argv) > 3 else OUTPUT_PDF

    ordered_tasks, section_for_task = load_toc(course_path)
    df = load_data(csv_path)
    stats = build_stats(df)
    plot(stats, ordered_tasks, section_for_task, output_pdf)


if __name__ == "__main__":
    main()
