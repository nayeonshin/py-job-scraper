from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def parse_spans(response):
    """
    Parse spans from response
    :param response: Response
    :return: List[Tag]
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find('ul', class_='pagination-list')
    pages = pagination.find_all('a')

    spans = []
    temp_spans = []

    for page in pages:
        temp_spans.append(page.find('span'))
    if len(str(temp_spans[0])) == 182:  # Current page
        spans.extend(temp_spans[3:-1])
    else:
        spans.extend(temp_spans[:-1])

    return spans


def extract_jobs(last_page_num):
    """
    ???
    :param last_page_num: int
    :return: List[???]
    """
    jobs = []

    response = requests.get(f'{URL}&start={0*LIMIT}')
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('h2', class_='jobTitle')
    for title in titles:
        print(title.find('span', title=True).string)

    return jobs


def get_last_page_num():
    """
    Get the last page's number at URL
    :return: int
    """
    first_response = requests.get(URL)
    spans = parse_spans(first_response)

    for i in range(200, 901, 100):
        response = requests.get(URL + f'&start={i}')
        spans = parse_spans(response)

    return int(spans[-1].string)
