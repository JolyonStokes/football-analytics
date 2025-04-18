from statsbombpy import sb
import pandas as pd

def get_leverkusen_bundesliga_matches():
    matches = sb.matches(competition_id=9, season_id=281)
    leverkusen_matches = matches[
        (matches['home_team'].str.contains("Leverkusen")) | 
        (matches['away_team'].str.contains("Leverkusen"))
    ].copy()
    return leverkusen_matches

def get_shots_for_matches(match_ids: list):
    all_shots = []

    for match_id in match_ids:
        events = sb.events(match_id=match_id)
        if 'shot_statsbomb_xg' not in events.columns:
            continue

        shots = events[events['type'] == 'Shot'].copy()
        shots['match_id'] = match_id

        shots = shots[shots['shot_statsbomb_xg'].notna()]

        all_shots.append(shots)

    if all_shots:
        return pd.concat(all_shots, ignore_index=True)
    else:
        return pd.DataFrame()

def get_leverkusen_shots():
    matches = get_leverkusen_bundesliga_matches()
    match_ids = matches['match_id'].tolist()
    shots = get_shots_for_matches(match_ids)

    if shots.empty:
        print("No valid shots found for Leverkusen with xG data.")
        return shots

    desired_cols = ['match_id', 'team', 'player', 'minute', 'second', 'shot_statsbomb_xg', 'outcome.name']
    available_cols = [col for col in desired_cols if col in shots.columns]
    shots = shots[available_cols]

    if 'outcome.name' in shots.columns:
        shots = shots.rename(columns={'outcome.name': 'outcome'})

    return shots


def get_actual_points_for_leverkusen():
    matches = get_leverkusen_bundesliga_matches()
    records = []

    for _, row in matches.iterrows():
        match_id = row['match_id']
        home_team = row['home_team']
        away_team = row['away_team']
        home_score = row['home_score']
        away_score = row['away_score']

        # Determine result and assign points
        if home_score > away_score:
            winner = home_team
        elif away_score > home_score:
            winner = away_team
        else:
            winner = "Draw"

        for team in [home_team, away_team]:
            if winner == "Draw":
                pts = 1
            elif team == winner:
                pts = 3
            else:
                pts = 0

            if "Leverkusen" in team:
                records.append({
                    'match_id': match_id,
                    'team': team,
                    'Pts': pts
                })

    return pd.DataFrame(records)
