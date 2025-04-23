import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import requests
import json
import re
from bs4 import BeautifulSoup
from config import UNDERSTAT_SEASONS, UNDERSTAT_URL_TEMPLATE
from utils import get_db_engine
from database.load_data import insert_new_matches

from sqlalchemy import text

import codecs  # ✅ Needed for correct decoding

def scrape_understat_season(season):
    url = UNDERSTAT_URL_TEMPLATE.format(season=season)
    print(f"Scraping Understat for season {season}: {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        script = next(s for s in soup.find_all('script') if 'datesData' in s.text)
    except StopIteration:
        print(f"⚠️ No 'datesData' script tag found for season {season}. Skipping.")
        return []

    # Updated, more flexible regex:
    match = re.search(r"datesData\s*=\s*JSON\.parse\(\s*(['\"])(.*?)\1\s*\)", script.text)
    if not match:
        print(f"⚠️ 'datesData' not found in script tag for season {season}. Skipping.")
        return []

    json_data = match.group(2)
    decoded_json = codecs.decode(json_data, 'unicode_escape')
    matches = json.loads(decoded_json)

    return matches

if __name__ == "__main__":
    engine = get_db_engine()
    with engine.connect() as conn:
        existing_ids = conn.execute(
            text("SELECT match_id FROM public_analysis.matches;")
        )
        existing_ids = set(row[0] for row in existing_ids)

    for season in UNDERSTAT_SEASONS:
        matches = scrape_understat_season(season)
        insert_new_matches(matches, existing_ids, engine, season)
        print(f"✅ Completed season {season}.")

    print("🎉 Scraping and loading finished.")