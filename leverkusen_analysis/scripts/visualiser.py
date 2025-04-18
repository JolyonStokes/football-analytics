# scripts/visualizer.py

import pandas as pd
import matplotlib.pyplot as plt

def plot_cumulative_pts_comparison(xpts_df: pd.DataFrame, actual_pts_df: pd.DataFrame, team_name: str):
    # Merge and sort by match order
    merged = pd.merge(xpts_df, actual_pts_df, on=["match_id", "team"])
    merged = merged[merged["team"] == team_name].sort_values("match_id")

    merged["cum_xPts"] = merged["xPts"].cumsum()
    merged["cum_Pts"] = merged["Pts"].cumsum()

    plt.figure(figsize=(10, 6))
    plt.plot(merged["cum_xPts"], label="Expected Points (xPts)", linewidth=2)
    plt.plot(merged["cum_Pts"], label="Actual Points", linewidth=2, linestyle="--")
    plt.title(f"Cumulative Points vs xPoints – {team_name}")
    plt.xlabel("Match Number")
    plt.ylabel("Cumulative Points")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_xpts_vs_actual_per_match(xpts_df: pd.DataFrame, actual_pts_df: pd.DataFrame, team_name: str):
    merged = pd.merge(xpts_df, actual_pts_df, on=["match_id", "team"])
    merged = merged[merged["team"] == team_name].sort_values("match_id")

    plt.figure(figsize=(10, 6))
    plt.plot(merged["xPts"], label="xPts", marker="o")
    plt.plot(merged["Pts"], label="Actual Pts", marker="x", linestyle="--")
    plt.title(f"Match-by-Match Points vs xPoints – {team_name}")
    plt.xlabel("Match Number")
    plt.ylabel("Points")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
