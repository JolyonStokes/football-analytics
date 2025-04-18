from statsbombpy import sb

def get_competitions():
    return sb.competitions()

def get_matches(competition_id: int, season_id: int):
    return sb.matches(competition_id=competition_id, season_id=season_id)

def get_events(match_id: int):
    return sb.events(match_id=match_id)

def get_lineups(match_id: int):
    return sb.lineups(match_id=match_id)
