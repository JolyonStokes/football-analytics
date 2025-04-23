from sqlalchemy import text


def insert_team_stats(team_stats_rows, engine):
    if not team_stats_rows:
        return

    # Step 1: Insert the team stats only (skip match insertion)
    insert_query = """
    INSERT INTO public_analysis.team_stats (
        match_id, date, team, opponent, possession, passing_accuracy, passes_attempted,
        shots, shots_on_target_pct, save_pct, yellow_cards, red_cards,
        fouls, corners, crosses, tackles, interceptions, aerials_won, clearances,
        offsides, goal_kicks, throw_ins, long_balls
    )
    VALUES (
        :match_id, :date, :team, :opponent, :possession, :passing_accuracy, :passes_attempted,
        :shots, :shots_on_target_pct, :save_pct, :yellow_cards, :red_cards,
        :fouls, :corners, :crosses, :tackles, :interceptions, :aerials_won, :clearances,
        :offsides, :goal_kicks, :throw_ins, :long_balls
    )
    ON CONFLICT (match_id, team) DO NOTHING;
    """
    with engine.begin() as conn:
        conn.execute(text(insert_query), team_stats_rows)

