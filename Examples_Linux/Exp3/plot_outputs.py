from __future__ import annotations

import math
import re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def _norm_col(name: str) -> str:
    # Normalize headers like "z", "z(cm)", " Z ", "Depth (cm)" into comparable keys.
    return re.sub(r"[^a-z0-9]+", "", name.strip().lower())


def _find_depth_col(columns, path: Path) -> str:
    # Prefer exact matches first, then fall back to common variants.
    for c in columns:
        n = _norm_col(c)
        if n in {"z", "zcm", "depth", "depthcm"}:
            return c
    for c in columns:
        n = _norm_col(c)
        if n.startswith("z"):
            return c
    raise ValueError(f"Cannot find depth column (z/depth) in {path.name}. Columns={list(columns)}")


def _extract_time_value(df) -> float | None:
    # Support headers like "time", "time(d)", "Time (d)".
    for c in df.columns:
        if _norm_col(c).startswith("time"):
            try:
                return float(df[c].iloc[0])
            except Exception:
                return None
    return None


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_")

def _pretty_label(name: str) -> str:
    base = name.strip()
    if "(" in base:
        base = base.split("(", 1)[0].strip()
    key = base.lower()
    if key == "aaw":
        return r"$\it{A_{aw}}$ (cm$^2$/cm$^3$)"
    if key == "caw1":
        return r"$\it{C_{aw,1}}$ (mg/cm$^3$)"
    if key == "caw2":
        return r"$\it{C_{aw,2}}$ (mg/cm$^3$)"
    if key == "cs1":
        return r"$\it{C_{s,1}}$ (mg/g)"
    if key == "cs2":
        return r"$\it{C_{s,2}}$ (mg/g)"
    if key == "ctot":
        return r"$\it{C_{tot}}$ (mg/cm$^3$)"
    if key == "sw":
        return r"$\it{S_w}$ (-)"
    if key == "h":
        return r"$\it{h}$ (cm)"
    if key == "th":
        return r"$\it{\theta}$ (cm$^3$/cm$^3$)"
    if key == "c":
        return r"$\it{C}$ (mg/L)"
    return name

def _pretty_time_series_label(name: str) -> str:
    key = re.sub(r"\s+", "", name.lower())
    mapping = {
        "htop(cm)": r"$\it{h_{top}}$ (cm)",
        "hbot(cm)": r"$\it{h_{bottom}}$ (cm)",
        "ctop(mg/l)": r"Porewater $\it{C}$ (top) (mg/L)",
        "cbot(mg/l)": r"Porewater $\it{C}$ (bottom) (mg/L)",
        "water_input(cm)": "Water input (cm)",
        "et(cm)": "ET (cm)",
        "drainage(cm)": "Drainage (cm)",
        "water_drainage(cm)": "Drainage (cm)",
        "water_tot(cm)": "Total amount of water in the domain (cm)",
        "pfas_in(mg)": "PFAS input (mg)",
        "pfas_decay(mg)": "PFAS Decay (mg)",
        "pfas_discharge(mg)": "PFAS discharged from the outlet (mg)",
        "pfas_tot(mg)": "Total amount of PFAS in the domain (mg)",
        "water_error(%)": r"MB Err$_{water}$ (%)",
        "water_mb_error(%)": r"MB Err$_{water}$ (%)",
        "pfas_error(%)": r"MB Err$_{PFAS}$ (%)",
        "pfas_mb_error(%)": r"MB Err$_{PFAS}$ (%)",
    }
    return mapping.get(key, name)


def _facet_size(n_panels: int, ncols: int, base_w: float, base_h: float) -> tuple[int, int, float, float]:
    ncols = max(1, min(ncols, n_panels))
    nrows = math.ceil(n_panels / ncols)
    width = base_w * ncols
    height = base_h * nrows
    return nrows, ncols, width, height


def plot_time_series(output_dir: Path, figure_dir: Path) -> None:
    path = output_dir / "2.Time series.csv"
    # sep=None makes pandas sniff delimiters (robust to comma vs whitespace vs tabs).
    df = pd.read_csv(path, sep=None, engine="python", skipinitialspace=True)

    time_col = df.columns[0]
    cols = list(df.columns[1:])
    if not cols:
        return

    def _norm(name: str) -> str:
        return re.sub(r"\s+", "", name.lower())

    colmap = {_norm(c): c for c in cols}

    groups = [
        ("Monitored pressure head at the top and bottom", ["htop(cm)", "hbot(cm)"]),
        ("Aqueous concentrations at the top and bottom", ["ctop(mg/l)", "cbot(mg/l)"]),
        ("Water Balance", ["water_input(cm)", "et(cm)", "drainage(cm)", "water_drainage(cm)", "water_tot(cm)"]),
        ("PFAS Balance", ["pfas_in(mg)", "pfas_decay(mg)", "pfas_discharge(mg)", "pfas_tot(mg)"]),
        ("Mass balance errors (%)", ["water_error(%)", "water_mb_error(%)", "pfas_error(%)", "pfas_mb_error(%)"]),
    ]

    series_groups: list[tuple[str, list[str]]] = []
    for title, keys in groups:
        cols_found = [colmap[k] for k in keys if k in colmap]
        if cols_found:
            series_groups.append((title, cols_found))

    if not series_groups:
        return

    nrows, ncols, width, height = _facet_size(len(series_groups), ncols=2, base_w=5.5, base_h=3.4)
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height + 1.0), sharex=True)
    axes = axes.flatten()

    for ax, (title, group_cols) in zip(axes, series_groups):
        for col in group_cols:
            ax.plot(df[time_col], df[col], linewidth=1.2, label=_pretty_time_series_label(col))
        ax.set_title(title, fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8, frameon=False)
        if title == "Mass balance errors (%)":
            max_err = 0.0
            for col in group_cols:
                max_err = max(max_err, float(df[col].abs().max()))
            x = 10.0 * max_err if max_err > 0.0 else 1.0
            ax.set_ylim(-x, x)

    for ax in axes[len(series_groups):]:
        ax.axis("off")

    for ax in axes[-ncols:]:
        ax.set_xlabel("Time (d)")

    fig.tight_layout()
    fig.savefig(figure_dir / "Time series.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_observations(output_dir: Path, figure_dir: Path) -> None:
    path = output_dir / "3.Observations.csv"
    df = pd.read_csv(path, sep=None, engine="python", skipinitialspace=True)

    time_col = df.columns[0]
    groups: dict[str, list[tuple[int, str]]] = {}
    for col in df.columns[1:]:
        if "-" not in col:
            continue
        base, cell = col.rsplit("-", 1)
        try:
            cell_id = int(cell)
        except ValueError:
            continue
        groups.setdefault(base, []).append((cell_id, col))

    bases = sorted(groups.keys())
    if not bases:
        return

    nrows, ncols, width, height = _facet_size(len(bases), ncols=3, base_w=4.0, base_h=3.0)
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height), sharex=True)
    axes = axes.flatten()

    for ax, base in zip(axes, bases):
        series = sorted(groups[base], key=lambda x: x[0])
        for cell_id, col in series:
            ax.plot(df[time_col], df[col], linewidth=1.1, label=f"{cell_id}")
        ax.set_title(_pretty_label(base), fontsize=9)
        ax.grid(True, alpha=0.3)

    for ax in axes[len(bases):]:
        ax.axis("off")

    for ax in axes[-ncols:]:
        ax.set_xlabel("Time (d)")

    handles, labels = axes[0].get_legend_handles_labels()
    if handles:
        fig.legend(handles, labels, title="Cell", ncol=6, fontsize=8, frameon=False, loc="lower center")
        fig.subplots_adjust(bottom=0.12)
    else:
        fig.tight_layout()

    fig.savefig(figure_dir / "Monitored cells.pdf", bbox_inches="tight")
    plt.close(fig)


def _profile_sort_key(path: Path) -> int:
    match = re.search(r"Profile-Time-(\d+)", path.name)
    if match:
        return int(match.group(1))
    return 0


def plot_profiles(output_dir: Path, figure_dir: Path) -> None:
    profile_files = sorted(output_dir.glob("1.Profile-Time-*.csv"), key=_profile_sort_key)
    if not profile_files:
        return

    profiles = []
    for path in profile_files:
        df = pd.read_csv(path, sep=None, engine="python", skipinitialspace=True)
        z_col = _find_depth_col(df.columns, path)
        time_val = _extract_time_value(df)
        profiles.append((path, df, z_col, time_val))

    z_norm = _norm_col(profiles[0][2])
    vars_to_plot = [
        c for c in profiles[0][1].columns
        if _norm_col(c) != "iprint" and not _norm_col(c).startswith("time") and _norm_col(c) != z_norm
    ]
    if not vars_to_plot:
        return

    nrows, ncols, width, height = _facet_size(len(vars_to_plot), ncols=3, base_w=4.0, base_h=3.2)
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height + 1.0), sharey=True)
    axes = axes.flatten()

    for ax, var in zip(axes, vars_to_plot):
        for _, df, z_col, time_val in profiles:
            label = f"t={time_val:g} d" if time_val is not None else None
            ax.plot(df[var], df[z_col], linewidth=1.1, label=label)
        ax.set_title(_pretty_label(var), fontsize=9)
        ax.grid(True, alpha=0.3)
        max_depth = max(p[1][p[2]].max() for p in profiles)
        ax.set_ylim(max_depth, 0.0)

    for ax in axes[len(vars_to_plot):]:
        ax.axis("off")

    for ax in axes[::ncols]:
        ax.set_ylabel("Depth (cm)")

    handles, labels = axes[0].get_legend_handles_labels()
    if handles:
        fig.legend(handles, labels, ncol=4, fontsize=8, frameon=False, loc="lower center")
        fig.subplots_adjust(bottom=0.12)
    else:
        fig.tight_layout()

    fig.savefig(figure_dir / "Profiles.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "OUTPUT"
    figure_dir = base_dir / "FIGURES"
    figure_dir.mkdir(parents=True, exist_ok=True)

    plot_time_series(output_dir, figure_dir)
    plot_observations(output_dir, figure_dir)
    plot_profiles(output_dir, figure_dir)


if __name__ == "__main__":
    main()
