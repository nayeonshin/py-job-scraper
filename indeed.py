from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'
spans = []


def parse_spans(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find('ul', class_='pagination-list')
    pages = pagination.find_all('a')

    temp_spans = []

    for page in pages:
        temp_spans.append(page.find('span'))
    if len(str(temp_spans[0])) == 182:  # Current page
        spans.extend(temp_spans[3:-1])
    else:
        spans.extend(temp_spans[:-1])


def extract_jobs(last_page_num):
    jobs = []

    for page in range(last_page_num):
        response = requests.get(f'{URL}&start={page*LIMIT}')
        soup = BeautifulSoup(response.text, 'html.parser')

    return jobs


def get_last_page_num():
    result = requests.get(URL)
    parse_spans(result)

    for i in range(200, 901, 100):
        result = requests.get(URL + f'&start={i}')
        parse_spans(result)

    return int(spans[-1].string)
