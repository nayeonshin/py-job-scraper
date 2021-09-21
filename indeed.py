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


def _extract_job(html):
    """
    Get a dictionary of a job's information
    :param html: Tag
    :return: dict[str, str]
    """
    title = html.find('span', title=True).string
    company = html.find('span', class_='companyName').string
    location = html.find('div', class_='companyLocation').text
    job_id = html.parent['data-jk']

    return {
      'title': title,
      'company': company,
      'location': location,
      'link': f'https://www.indeed.com/viewjob?jk={job_id}&tk=1fg49gh9apiab801&from=serp&vjs=3'
    }


def extract_jobs(last_page_num):
    """
    Get a list of job info's dictionaries
    :param last_page_num: int
    :return: list[dict[str, str]]
    """
    jobs = []

    for i in range(last_page_num):
        print(f'Scrapping page {i}...')
        response = requests.get(f'{URL}&start={i * LIMIT}')
        soup = BeautifulSoup(response.text, 'html.parser')
        job_containers = soup.find_all('div', class_='slider_container')
        for job_container in job_containers:
            print(type(job_container))
            jobs.append(_extract_job(job_container))

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
