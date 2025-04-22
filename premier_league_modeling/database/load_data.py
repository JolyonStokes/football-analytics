from sqlalchemy import text

def insert_new_matches(matches, existing_ids, engine, season):
    with engine.begin() as conn:  # ✅ begin() auto-commits if no errors
        for match in matches:
            match_id = int(match['id'])
            if match_id in existing_ids:
                continue  # Skip existing matches
            if match['goals']['h'] is None or match['goals']['a'] is None:
                print(f"Skipping match {match_id} — not played yet.")
                continue

            home_team = match['h']['title']
            away_team = match['a']['title']
            home_goals = int(match['goals']['h']) if match['goals']['h'] is not None else None
            away_goals = int(match['goals']['a']) if match['goals']['a'] is not None else None
            home_xg = float(match['xG']['h']) if match['xG']['h'] is not None else None
            away_xg = float(match['xG']['a']) if match['xG']['a'] is not None else None
            date = match['datetime'][:10]  # 'YYYY-MM-DD'
            result = None
            if home_goals is not None and away_goals is not None:
                result = 'H' if home_goals > away_goals else ('A' if away_goals > home_goals else 'D')

            conn.execute(
                text("""
                    INSERT INTO public_analysis.matches
                    (match_id, date, season, home_team, away_team, home_goals, away_goals, home_xg, away_xg, result)
                    VALUES (:match_id, :date, :season, :home_team, :away_team, :home_goals, :away_goals, :home_xg, :away_xg, :result)
                    ON CONFLICT (match_id) DO NOTHING;
                """),
                {
                    'match_id': match_id,
                    'date': date,
                    'season': season,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_goals': home_goals,
                    'away_goals': away_goals,
                    'home_xg': home_xg,
                    'away_xg': away_xg,
                    'result': result
                }
            )
