import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_shine(max_pages=5):
    jobs = []
    for page in range(1, max_pages+1):
        url = f"https://www.shine.com/job-search/it-jobs-%7Bpage%7D?q=it&qActual=it&farea=1313&farea=4530&farea=4528&farea=4429&farea=1405&farea=4560&farea=2801&farea=2803&farea=4526&findustry=18&findustry=81"
        domain = url.split('/')[2].split('.')[1]
        print(f"Scraping Shine page {page}: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        listings = soup.find_all('div', class_="jobCardNova_bigCard__W2xn3 jdbigCard")
        if not listings:
            break
        for data in listings:
            title_elem = data.find('a')
            title = title_elem.text.strip() if title_elem else "N/A"
            job_url = title_elem['href'] if title_elem and 'href' in title_elem.attrs else "N/A"
            location_elem = data.find('div', class_="jobCardNova_bigCardCenterListLoc__usiPB jobCardNova_limits__G87pQ d-flex justify-content-start align-items-center")
            location = location_elem.find_next('span').text.strip() if location_elem else "N/A"
            try:
                company = data.find('span', class_="jobCardNova_bigCardTopTitleName__M_W_m jdTruncationCompany").text.strip()
            except:
                company = ''
            jobs.append({
                "source": domain.capitalize(),
                "title": title,
                "company": company,
                "location": location,
                "link": job_url
            })
        time.sleep(1)
    print(f"Found {len(jobs)} jobs from Shine.")
    return jobs

def scrape_internshala(max_pages=2):
    jobs = []
    for page in range(1, max_pages+1):
        url = f"https://internshala.com/jobs/page-{page}/"
        domain = url.split('/')[2].replace('.com','')
        print(f"Scraping Internshala page {page}: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        listings = soup.find_all('div', class_="internship_meta experience_meta")
        if not listings:
            break
        for data in listings:
            source = domain
            title_elem = data.find('a', class_="job-title-href")
            title = title_elem.text.strip() if title_elem else "N/A"
            joburl = "https://internshala.com" + title_elem['href'] if title_elem and 'href' in title_elem.attrs else "N/A"
            location_elem = data.find('div', class_="detail-row-1")
            location = location_elem.find_next('span').text.strip() if location_elem and location_elem.find_next('span') else "N/A"
            company_elem = data.find('p', class_="company-name")
            company_name = company_elem.text.strip() if company_elem else "N/A"
            jobs.append({
                "source": source,
                "title": title,
                "company": company_name,
                "location": location,
                "link": joburl
            })
        time.sleep(1)
    print(f"Found {len(jobs)} jobs from Internshala.")
    return jobs

def get_all_technical_fresher_jobs():
    all_jobs = []
    all_jobs.extend(scrape_shine(5))         # 5 pages of Shine
    all_jobs.extend(scrape_internshala(2))   # 2 pages of Internshala
    print(f"\nTotal jobs scraped: {len(all_jobs)}")
    return all_jobs

if __name__ == "__main__":
    jobs = get_all_technical_fresher_jobs()
    print(json.dumps({"jobs": jobs}, indent=2, ensure_ascii=False))
