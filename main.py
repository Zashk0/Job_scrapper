import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import re
pattern = r"\/([^\/]+?)-[^\/]+\/$"

def fetch_dev_bg_job_listings(num_pages):
    job_listings = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }

    for page in range(1,num_pages):
        
        base_url = f"https://dev.bg/company/jobs/back-end-development/?_paged={page}"
        time.sleep(random.randint(1, 3))  # Random delay to mimic human behavior
        response = requests.get(base_url, headers=headers)
        print(f"Fetching page {page + 1}: HTTP Status Code: {response.status_code}")
        if response.status_code != 200:
            print("Failed to retrieve data. Check the URL and network status.")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', class_='inner-right listing-content-wrap')  # Assuming job listings are in this div class

        if not job_cards:
            print("No job cards found. Check the page structure and class names.")
            continue

        for card in job_cards:
            job_link = card.find('a', class_='overlay-link ab-trigger')
            if job_link:
                job_url = job_link['href']
                title = re.search(pattern, job_url)
                company_name = card.find('h6', class_='job-title ab-title-placeholder ab-cb-title-placeholder').text.strip()
                print(title.group(1))
                
                job_listings.append([title.group(1), company_name, job_url])

    return job_listings

def save_to_csv(job_listings, filename):
    if job_listings:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Job Title', 'Company', 'URL'])
            writer.writerows(job_listings)
        print(f"Job listings successfully saved to {filename}.")
    else:
        print("No job listings extracted to save to CSV.")

# Example usage
job_listings = fetch_dev_bg_job_listings(num_pages=3)
save_to_csv(job_listings, 'dev_bg_job_listings.csv')
