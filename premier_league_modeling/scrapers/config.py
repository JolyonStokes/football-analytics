UNDERSTAT_SEASONS = ['2020', '2021', '2022', '2023', '2024']
FBREF_SEASONS = ['2020-2021', '2021-2022', '2022-2023', '2023-2024', '2024-2025']
LEAGUE = 'EPL'  # Premier League
UNDERSTAT_URL_TEMPLATE = f"https://understat.com/league/{LEAGUE}/{{season}}"
FBREF_BASE_URL = "https://fbref.com"
FBREF_SCHEDULE_URL_TEMPLATE = "https://fbref.com/en/comps/9/{season}/schedule/{season}-Premier-League-Scores-and-Fixtures"
TEAM_NAME_MAPPING = {
    "Manchester United": "Man United",
    "Manchester City": "Man City",
    "Tottenham Hotspur": "Spurs",
    "Newcastle United": "Newcastle",
    "Brighton and Hove Albion": "Brighton",
    "West Ham United": "West Ham",
    "Wolverhampton Wanderers": "Wolves",
    "Leicester City": "Leicester",
    "Leeds United": "Leeds",
    "Nottingham Forest": "Nottm Forest",
    "Sheffield United": "Sheffield Utd",
    "AFC Bournemouth": "Bournemouth",
    "Brentford": "Brentford",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Liverpool": "Liverpool",
    "Arsenal": "Arsenal",
    # Add/remove as needed depending on your Understat team names
}
POSITION_METRIC_MAP = {
    "GK": [
        "Save %",
        "PSxG-GA",
        "Crosses Stopped %",
        "Launch %",
        "Avg Length of Goal Kicks",
        "Passes Attempted",
        "Pass Completion %",
        "Defensive Actions Outside Pen Area / 90"
    ],
    "CB": [
        "Aerial Duels Won %",
        "Tackles + Interceptions / 90",
        "Clearances / 90",
        "Pass Completion %",
        "Progressive Passes",
        "Passes into Final Third",
        "Blocks / 90",
        "Miscontrols + Dispossessed"
    ],
    "FB_Wide": [
        "Crosses / 90",
        "Progressive Carries / 90",
        "Dribble Success %",
        "Tackles + Interceptions / 90",
        "Touches (Attacking Third)",
        "xA / 90",
        "Passes into Pen Area",
        "Pressures (Middle Third)"
    ],
    "FB_Inverted": [
        "Pass Completion %",
        "Progressive Passes",
        "Passes into Final Third",
        "Interceptions / 90",
        "Carries into Final Third",
        "Touches (Middle Third)",
        "Miscontrols + Dispossessed",
        "Pressures (Middle or Def Third)"
    ],
    "CM_Holding": [
        "Tackles + Interceptions / 90",
        "Pressures (Def Third) / 90",
        "Blocks / 90",
        "Pass Completion %",
        "Progressive Passes",
        "Passes into Final Third",
        "Recoveries",
        "Miscontrols + Dispossessed"
    ],
    "CM_BoxToBox": [
        "Carries / 90",
        "Progressive Carries / 90",
        "Tackles + Interceptions / 90",
        "Key Passes / 90",
        "Shots / 90",
        "Passes into Final Third",
        "Dribbles Completed %",
        "Pressures (Mid Third)"
    ],
    "CM_Attacking": [
        "Key Passes / 90",
        "Passes into Pen Area",
        "xA / 90",
        "Shots / 90",
        "Shot-Creating Actions / 90",
        "Progressive Carries / 90",
        "Dribble Success %",
        "Turnovers"
    ],
    "ST": [
        "Non-Penalty Goals / 90",
        "xG / 90",
        "Shots / 90",
        "Shot on Target %",
        "Progressive Passes Received / 90",
        "Key Passes / 90",
        "Touches in Attacking Pen Area",
        "Aerial Win %"
    ],
    "Winger": [
        "Dribble Success %",
        "Progressive Carries / 90",
        "xA / 90",
        "Key Passes / 90",
        "Shots / 90",
        "Touches in Attacking Pen Area",
        "Crosses / 90",
        "Carries into Final Third"
    ]
}