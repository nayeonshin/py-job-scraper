from bs4 import BeautifulSoup
import requests

URL = f'https://stackoverflow.com/jobs?q=python'


def extract_last_page_num():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_elements = soup.find('div', class_='s-pagination').find_all('a')
    last_page_num = page_elements[-2].get_text(strip=True) # Excludes 'next'
    return int(last_page_num)


def _extract_job(html):
    title_element = html.find('h2')
    company_and_location_element = html.find('h3')
    title = company = location = ''
    if title_element:
        title = title_element.find('a')['title']
    if company_and_location_element:
        company_element, location_element = company_and_location_element.find_all('span', recursive=False)
        company, location = company_element.get_text(strip=True), location_element.get_text(strip=True)
        print(company)
        print(location)
    # return {
    #   'title': title
    # }


def extract_jobs(last_page_num):
    jobs = []
    for page in range(1, last_page_num + 1):
        response = requests.get(f'{URL}&pg={page}')
        soup = BeautifulSoup(response.text, 'html.parser')
        job_elements = soup.find_all('div', class_='fl1')
        for element in job_elements:
            job = _extract_job(element)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page_num = extract_last_page_num()
    jobs = extract_jobs(last_page_num)
    return jobs


get_jobs()
