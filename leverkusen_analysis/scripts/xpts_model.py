import numpy as np
import pandas as pd
from tqdm import tqdm

def simulate_match(match_df, n_simulations=10000):
    teams = match_df['team'].unique()
    if len(teams) != 2:
        raise ValueError(f"Expected 2 teams in match, got {teams}")

    team_1, team_2 = teams
    team_1_xg = match_df[match_df['team'] == team_1]['shot_statsbomb_xg'].values
    team_2_xg = match_df[match_df['team'] == team_2]['shot_statsbomb_xg'].values

    team_1_goals = np.random.rand(n_simulations, len(team_1_xg)) < team_1_xg
    team_2_goals = np.random.rand(n_simulations, len(team_2_xg)) < team_2_xg

    team_1_score = team_1_goals.sum(axis=1)
    team_2_score = team_2_goals.sum(axis=1)

    team_1_wins = (team_1_score > team_2_score).mean()
    draws = (team_1_score == team_2_score).mean()
    team_2_wins = (team_1_score < team_2_score).mean()

    return {
        team_1: 3 * team_1_wins + 1 * draws,
        team_2: 3 * team_2_wins + 1 * draws
    }

def simulate_season(shots_df, n_simulations=10000):
    xpts_records = []

    for match_id, match_shots in tqdm(shots_df.groupby('match_id'), desc="Simulating season"):
        try:
            match_xpts = simulate_match(match_shots, n_simulations=n_simulations)
            for team, xpts in match_xpts.items():
                xpts_records.append({
                    'match_id': match_id,
                    'team': team,
                    'xPts': xpts
                })
        except Exception as e:
            print(f"Error in match {match_id}: {e}")

    if xpts_records:
        return pd.DataFrame(xpts_records)
    else:
        return None