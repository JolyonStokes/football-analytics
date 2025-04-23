import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_rendered_match_html(url, wait_time=10):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, "team_stats"))
        )
    except:
        print("⚠️ Timeout waiting for page to load match stats properly.")

    page_source = driver.page_source
    driver.quit()
    return page_source

def parse_team_stats_extra(soup):
    extra_block = soup.find('div', id='team_stats_extra')
    if not extra_block:
        print("⚠️ Could not find 'team_stats_extra' section.")
        return {}

    stat_labels = [
        "Fouls", "Corners", "Crosses", "Touches",
        "Tackles", "Interceptions", "Aerials Won", "Clearances",
        "Offsides", "Goal Kicks", "Throw Ins", "Long Balls"
    ]

    stat_sections = extra_block.find_all('div', recursive=False)
    team_data = {'home': {}, 'away': {}}

    for section in stat_sections:
        blocks = section.find_all('div')
        if len(blocks) < 5:
            continue

        home_team_name = blocks[0].text.strip()
        away_team_name = blocks[2].text.strip()

        for i in range(3, len(blocks), 3):
            if i + 2 >= len(blocks):
                break
            home_value = int(blocks[i].text.strip())
            stat_name = blocks[i + 1].text.strip()
            away_value = int(blocks[i + 2].text.strip())

            if stat_name in stat_labels:
                team_data['home'][stat_name] = home_value
                team_data['away'][stat_name] = away_value

    return team_data, home_team_name, away_team_name

def extract_total_shots(stats_block):
    section = stats_block.find('th', string="Shots on Target")
    if not section:
        return None, None
    shots_row = section.find_parent('tr').find_next_sibling('tr')
    if not shots_row:
        return None, None

    home_text = shots_row.find_all('td')[0].get_text(strip=True)
    away_text = shots_row.find_all('td')[1].get_text(strip=True)

    # Example text: '1 of 6 — 17%' → we want the '6' and '17' is the percentage
    try:
        home_total = int(home_text.split('of')[1].split()[0])
        away_total = int(away_text.split('of')[1].split()[0])
    except (IndexError, ValueError):
        home_total, away_total = None, None

    return home_total, away_total

def parse_value(value):
        """Helper function to parse the value and return it as float or None."""
        value_text = value.text.replace('%', '').strip()
        return float(value_text) if value_text else None


def extract_two_strong_values(stats_block, section_header):
        section = stats_block.find('th', string=section_header)
        if not section:
            return None, None
        values_row = section.find_parent('tr').find_next_sibling('tr')
        if values_row:
            values = values_row.find_all('strong')
            if len(values) == 2:
                home_text = values[0].text.replace('%', '').strip()
                away_text = values[1].text.replace('%', '').strip()
                home = float(home_text) if home_text else None
                away = float(away_text) if away_text else None
                return home, away
        return None, None


def parse_match_stats(match):
    url = match['match_url']
    if not url:
        print(f"⚠️ No match report available for {match['date']} {match['home_team']} vs {match['away_team']}. Skipping.")
        return []

    print(f"Scraping match stats: {url}")
    html = get_rendered_match_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    stats_data = []
    stats_block = soup.find('div', id='team_stats')
    if not stats_block:
        print(f"⚠️ Could not find match stats block for {url}. Skipping.")
        return []


    # Core stats:
    possession_home, possession_away = extract_two_strong_values(stats_block, "Possession")
    passing_home, passing_away = extract_two_strong_values(stats_block, "Passing Accuracy")
    shots_on_target_home, shots_on_target_away = extract_two_strong_values(stats_block, "Shots on Target")
    saves_home, saves_away = extract_two_strong_values(stats_block, "Saves")
    total_shots_home, total_shots_away = extract_total_shots(stats_block)

    # Passes Attempted (extracted from Passing Accuracy text):
    passing_section = stats_block.find('th', string="Passing Accuracy")
    if passing_section:
        passing_row = passing_section.find_parent('tr').find_next_sibling('tr')
        if passing_row:
            home_pass_text = passing_row.find_all('td')[0].get_text(strip=True)
            away_pass_text = passing_row.find_all('td')[1].get_text(strip=True)

            try:
                home_attempted = int(home_pass_text.split('of')[1].split()[0])
                away_attempted = int(away_pass_text.split('of')[1].split()[0])
            except (IndexError, ValueError):
                home_attempted, away_attempted = None, None
        else:
            home_attempted, away_attempted = None, None
    else:
        home_attempted, away_attempted = None, None

    # Cards:
    cards_section = stats_block.find('th', string="Cards")
    cards_row = cards_section.find_parent('tr').find_next_sibling('tr') if cards_section else None
    if cards_row:
        home_yellow = len(cards_row.find_all('td')[0].find_all('span', class_='yellow_card'))
        away_yellow = len(cards_row.find_all('td')[1].find_all('span', class_='yellow_card'))
        home_red = len(cards_row.find_all('td')[0].find_all('span', class_='red_card'))
        away_red = len(cards_row.find_all('td')[1].find_all('span', class_='red_card'))
    else:
        home_yellow, away_yellow, home_red, away_red = None, None, None, None

    # Extra stats:
    extra_stats, extra_home_team, extra_away_team = parse_team_stats_extra(soup)
    if (extra_home_team != match['home_team']) or (extra_away_team != match['away_team']):
        print(f"⚠️ Team name mismatch! Fixture: {match['home_team']} vs {match['away_team']} | Stats Extra: {extra_home_team} vs {extra_away_team}")

    for side, team in enumerate([match['home_team'], match['away_team']]):
        opponent = match['away_team'] if side == 0 else match['home_team']
        extra_side = 'home' if side == 0 else 'away'

        team_stats = {
            'match_id': url.split('/')[-2],
            'date': match['date'],
            'team': team,
            'opponent': opponent,
            'possession': possession_home if side == 0 else possession_away,
            'passing_accuracy': passing_home if side == 0 else passing_away,
            'shots': total_shots_home if side == 0 else total_shots_away,
            'shots_on_target_pct': shots_on_target_home if side == 0 else shots_on_target_away,
            'save_pct': saves_home if side == 0 else saves_away,
            'passes_attempted': home_attempted if side == 0 else away_attempted,
            'yellow_cards': home_yellow if side == 0 else away_yellow,
            'red_cards': home_red if side == 0 else away_red,
        }

        # Add extra stats:
        for stat_label in extra_stats.get(extra_side, {}):
            clean_label = stat_label.lower().replace(' ', '_')
            team_stats[clean_label] = extra_stats[extra_side][stat_label]

        stats_data.append(team_stats)

    return stats_data

