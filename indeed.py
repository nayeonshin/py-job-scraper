from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def parse_spans(response):
    """
    Parse spans from response
    :param response: Response
    :return: list[Tag]
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


def _extract_job(title, company, location):
    """
    Return a dictionary of a job's information
    :param title: Tag
    :param company: Tag
    :param location: Tag
    :return: dict[str, str]
    """
    return {
        'title': title.find('span', title=True).string,
        'company': company.string,
        'location': location.text
    }


def extract_jobs(last_page_num):
    """
    ???
    :param last_page_num: int
    :return: list[dict[str, str]]
    """
    jobs = []

    response = requests.get(f'{URL}&start={0 * LIMIT}')
    soup = BeautifulSoup(response.text, 'html.parser')
    title_elements = soup.find_all('h2', class_='jobTitle')
    company_elements = soup.find_all('span', class_="companyName")
    location_elements = soup.find_all('div', class_='companyLocation')

    for i in range(LIMIT):
        job = _extract_job(title_elements[i], company_elements[i],
                           location_elements[i])
        jobs.append(job)

    return jobs


def get_max_page_num():
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
