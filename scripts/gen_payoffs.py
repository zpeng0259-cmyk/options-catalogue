#!/usr/bin/env python3
"""Generate static SVG payoff diagrams for CSP / BPS / CC.

Run once after editing the PARAMS dict, then commit the resulting SVGs.
Requires: matplotlib  (pip install matplotlib)
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "payoffs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROFIT = "#34d399"
LOSS = "#f87171"
NEUTRAL = "#a1a1aa"
GRID = "#3f3f46"
BG = "#18181b"
TEXT = "#e4e4e7"


def style(ax, title, xlabel="Stock Price at Expiry", ylabel="P&L ($)"):
    ax.set_facecolor(BG)
    ax.figure.patch.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)
    ax.set_title(title, color=TEXT, fontsize=12, pad=10)
    ax.set_xlabel(xlabel, color=TEXT, fontsize=10)
    ax.set_ylabel(ylabel, color=TEXT, fontsize=10)
    ax.axhline(0, color=NEUTRAL, linewidth=0.8)


def fill_pnl(ax, x, y):
    ax.plot(x, y, color=TEXT, linewidth=2)
    ax.fill_between(x, y, 0, where=y > 0, color=PROFIT, alpha=0.25)
    ax.fill_between(x, y, 0, where=y < 0, color=LOSS, alpha=0.25)


def annotate(ax, x, y, text, dy=8):
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(0, dy),
        textcoords="offset points",
        color=TEXT,
        fontsize=9,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=GRID, alpha=0.9),
    )


def save(fig, name):
    out = OUT_DIR / f"{name}.svg"
    fig.savefig(out, format="svg", bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"wrote {out}")


# ----------------------------- CSP -----------------------------
# Cash-Secured Put: sold put @ K, premium P
def gen_csp():
    K = 100.0
    P = 2.5
    x = np.linspace(K * 0.7, K * 1.3, 400)
    # P&L per share at expiry: premium - max(K - S, 0)
    y = P - np.maximum(K - x, 0)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fill_pnl(ax, x, y)
    ax.axvline(K, color=NEUTRAL, linestyle="--", linewidth=0.8)
    ax.axvline(K - P, color=NEUTRAL, linestyle=":", linewidth=0.8)
    annotate(ax, K, P, f"Strike K=${K:.0f}\nMax profit +${P:.2f}")
    annotate(ax, K - P, 0, f"Breakeven\n${K - P:.2f}", dy=-22)
    annotate(ax, K * 0.75, P - (K - K * 0.75), f"Loss accelerates\nbelow K", dy=-22)
    style(ax, "CSP — Cash-Secured Put 损益图（到期）")
    save(fig, "csp")


# ----------------------------- BPS -----------------------------
# Bull Put Spread: sold put @ K_short (high), bought put @ K_long (low)
def gen_bps():
    K_short = 100.0
    K_long = 95.0
    credit = 1.5  # net premium received per share
    width = K_short - K_long
    max_loss = -(width - credit)
    x = np.linspace(K_long * 0.85, K_short * 1.20, 400)
    # P&L per share = credit - max(K_short - S, 0) + max(K_long - S, 0)
    y = credit - np.maximum(K_short - x, 0) + np.maximum(K_long - x, 0)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fill_pnl(ax, x, y)
    ax.axvline(K_short, color=NEUTRAL, linestyle="--", linewidth=0.8)
    ax.axvline(K_long, color=NEUTRAL, linestyle="--", linewidth=0.8)
    ax.axvline(K_short - credit, color=NEUTRAL, linestyle=":", linewidth=0.8)
    annotate(ax, K_short, credit, f"K_short=${K_short:.0f}\nMax profit +${credit:.2f}")
    annotate(ax, K_long, max_loss, f"K_long=${K_long:.0f}\nMax loss ${max_loss:.2f}", dy=-22)
    annotate(ax, K_short - credit, 0, f"Breakeven\n${K_short - credit:.2f}", dy=10)
    style(ax, "BPS — Bull Put Spread Payoff (at expiry)")
    save(fig, "bps")


# ----------------------------- CC -----------------------------
# Covered Call: long 100 shares @ cost C, sold call @ K, premium P
def gen_cc():
    C = 100.0  # cost basis per share
    K = 105.0
    P = 1.8
    x = np.linspace(C * 0.6, C * 1.4, 400)
    # P&L = (S - C) + P - max(S - K, 0)
    y = (x - C) + P - np.maximum(x - K, 0)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fill_pnl(ax, x, y)
    ax.axvline(K, color=NEUTRAL, linestyle="--", linewidth=0.8)
    ax.axvline(C - P, color=NEUTRAL, linestyle=":", linewidth=0.8)
    annotate(ax, K, (K - C) + P, f"Strike K=${K:.0f}\nMax profit +${(K - C) + P:.2f}")
    annotate(ax, C - P, 0, f"Breakeven\n${C - P:.2f}", dy=-22)
    annotate(ax, C * 0.7, (C * 0.7 - C) + P, f"Stock falls →\nlimited downside protection\n(only premium P)", dy=10)
    style(ax, "CC — Covered Call Payoff (at expiry)")
    save(fig, "cc")


if __name__ == "__main__":
    gen_csp()
    gen_bps()
    gen_cc()
    print("done")
