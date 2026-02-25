import requests
from bs4 import BeautifulSoup
import re

def extract_salary(text):
    # Looks for salary numbers like 1500, 2000 GEL, etc.
    match = re.search(r'(\d{3,5})\s?(GEL|₾)?', text)
    if match:
        return int(match.group(1))
    return None

def scrape_jobs_ge():
    url = "https://jobs.ge/ge/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    seen_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "view=jobs&id=" in href:
            title = a.get_text(strip=True)

            if title:
                full_link = "https://jobs.ge" + href.replace("&amp;", "&")

                if full_link not in seen_links:
                    seen_links.add(full_link)

                    # --- Open job page to extract salary ---
                    job_response = requests.get(full_link, headers=headers)
                    job_soup = BeautifulSoup(job_response.text, "html.parser")

                    job_text = job_soup.get_text()

                    salary = extract_salary(job_text)

                    jobs.append({
                        "title": title,
                        "link": full_link,
                        "salary": salary
                    })

    return jobs
