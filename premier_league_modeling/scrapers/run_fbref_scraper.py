import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fbref_fixture_scraper import get_season_fixture_links
from fbref_scraper import parse_match_stats
from database.load_team_stats import insert_team_stats
from utils import get_db_engine
import pandas as pd

SEASONS = [
    "2020-2021",
    "2021-2022",
    "2022-2023",
    "2023-2024",
    "2024-2025"
]

# Function to check if a match already exists in the 'matches' table
def get_existing_match_ids(engine):
    query = "SELECT match_id FROM public_analysis.team_stats;"
    result = pd.read_sql(query, engine)
    return result['match_id'].to_list()

def run_full_scrape():
    engine = get_db_engine()
    for season in SEASONS:
        print(f"\n📅 Starting scrape for season: {season}")
        fixture_list = get_season_fixture_links(season)
        scraped_matches = get_existing_match_ids(engine)
        fixture_list = [
            match for match in fixture_list if match['match_url'] and match['match_url'].split('/')[-2] not in scraped_matches
        ]
        print(len(fixture_list),' fixtures')


        if not fixture_list:
            print(f"⚠️ No fixtures found for {season}. Skipping season.")
            continue

        for match in fixture_list:
            if not match['match_url']:
                print(match)
                print(f"⚠️ No match report yet for {match['date']} {match['home_team']} vs {match['away_team']}. Skipping.")
                continue
            
            try:
                team_stats_rows = parse_match_stats(match)
                if team_stats_rows:
                    insert_team_stats(team_stats_rows, engine)
                    print(f"✅ Inserted stats for match: {match['home_team']} vs {match['away_team']} on {match['date']}")
                else:
                    print(f"⚠️ No team stats scraped for {match['match_url']}")
            except Exception as e:
                print(f"❌ Error scraping match {match['match_url']}: {e}")

if __name__ == "__main__":
    run_full_scrape()
