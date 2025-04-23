from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Comment
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import FBREF_BASE_URL, FBREF_SCHEDULE_URL_TEMPLATE

def get_rendered_html(url, wait_time=15):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    try:
        # ✅ Explicit wait for ANY fixture table (ID starts with 'sched_')
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[id^='sched_']"))
        )
        print("✅ Fixture table detected after JS render.")
    except Exception as e:
        print(f"⚠️ Timeout or issue waiting for fixture table: {e}")

    page_source = driver.page_source
    driver.quit()
    return page_source

def get_fixture_table_from_comments(soup):
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    print(f"🟢 Searching {len(comments)} comment blocks for the fixture table...")

    for idx, comment in enumerate(comments):
        comment_soup = BeautifulSoup(comment, 'html.parser')
        potential_tables = comment_soup.find_all('table')
        for table in potential_tables:
            table_id = table.get('id', '')
            headers = [th.get('data-stat') for th in table.find('thead').find_all('th')]
            if table_id.startswith('sched_') and 'home_team' in headers and 'away_team' in headers:
                print(f"✅ Found fixture table inside comment block #{idx + 1} (ID: {table_id})")
                return table

    print("❌ No fixture table found in comments.")
    return None


def get_season_fixture_links(season):
    url = FBREF_SCHEDULE_URL_TEMPLATE.format(season=season)
    print(f"📅 Scraping fixture list for season {season}: {url}")

    html = get_rendered_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    # ✅ Directly locate the rendered table — no comments needed!
    table = soup.select_one("table[id^='sched_']")

    if not table:
        print(f"⚠️ Could not find the fixture table for season {season}.")
        return []

    print(f"✅ Found fixture table for season {season}.")

    matches = []
    rows = table.find('tbody').find_all('tr')

    for row in rows:
        date_cell = row.find('td', {'data-stat': 'date'})
        home_cell = row.find('td', {'data-stat': 'home_team'})
        away_cell = row.find('td', {'data-stat': 'away_team'})
        match_link_cell = row.find('td', {'data-stat': 'match_report'})

        if not date_cell or not home_cell or not away_cell:
            continue  # Skip blank rows or headers

        date = date_cell.text.strip()
        home_team = home_cell.text.strip()
        away_team = away_cell.text.strip()

        match_url = None
        if match_link_cell:
            match_link_tag = match_link_cell.find('a')
            if match_link_tag:
                match_url = FBREF_BASE_URL + match_link_tag['href']

        matches.append({
            'date': date,
            'home_team': home_team,
            'away_team': away_team,
            'match_url': match_url
        })

    print(f"✅ Found {len(matches)} matches for season {season}.")
    return matches



# ✅ Example test:
if __name__ == "__main__":
    season = "2023-2024"
    fixtures = get_season_fixture_links(season)
    print(fixtures[:5])  # Show first 5 matches for confirmation


