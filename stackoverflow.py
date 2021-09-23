from bs4 import BeautifulSoup
import requests

URL = f'https://stackoverflow.com/jobs?q=python'


def extract_last_page_num():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_elements = soup.find('div', class_='s-pagination').find_all('a')
    last_page_num = page_elements[-2].get_text(strip=True) # Excludes 'next'
    return int(last_page_num)


def extract_jobs(last_page_num):
    jobs = []
    for page in range(1, last_page_num + 1):
        response = requests.get(f'{URL}&pg={page}')
        soup = BeautifulSoup(response.text, 'html.parser')
        job_elements = soup.find_all('div', class_='fl1')
        for element in job_elements:
            print(element.text)


def get_jobs():
    last_page_num = extract_last_page_num()
    jobs = extract_jobs(last_page_num)
    return jobs


get_jobs()
