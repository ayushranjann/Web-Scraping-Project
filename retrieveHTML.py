import requests
from bs4 import BeautifulSoup
import csv  


def fetch_and_save_html(url, filename):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/119.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        pretty_html = soup.prettify()

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(pretty_html)

        print(f"HTML saved to {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

# URL and filename
url = "https://www.sportingnews.com/in/football/scores"
filename = "file.html"
fetch_and_save_html(url, filename)

# ----------- Extract and Save Team Names into CSV -----------

# Open and read the saved HTML
with open("file.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Set to store unique team names
team_names = set()

# Brute-force search through common tags
for tag in soup.find_all(['span', 'div', 'p', 'h2', 'h3', 'a']):
    text = tag.get_text(strip=True)
    if text:
        if 2 <= len(text.split()) <= 4 and text.isalpha() is False:
            team_names.add(text)

# Sort team names
sorted_teams = sorted(team_names)

# Save to CSV
csv_filename = "team_names.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Team Name"])  # Header
    for team in sorted_teams:
        writer.writerow([team])

print(f"\nSaved {len(sorted_teams)} team names to '{csv_filename}' ✅")