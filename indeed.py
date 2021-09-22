from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def _check_has_first_page_end():
    """
    Check if the first page is the last page
    :return: bool
    """
    first_response = requests.get(URL)
    soup = BeautifulSoup(first_response.text, 'html.parser')
    pagination = soup.find('div', class_='pagination')

    nav_items = pagination.find_all('li')
    # Gets the 'aria-label' values of li's child elements into a list
    item_labels = [item.findChild()['aria-label'] for item in nav_items]
    # If 'Next' is not in nav, the first page is really the last page.
    return 'Next' not in item_labels


def get_last_page_num():
    """
    Get the last page number
    :return: int
    """
    is_last_page = _check_has_first_page_end()
    item_labels = []
    page_index = 0

    while not is_last_page:
        # Starting at https://www.indeed.com/jobs?q=python&limit=50&start=0,
        # sends a GET request to the url with a different '&start=' number
        response = requests.get(URL + f'&start={page_index * LIMIT}')
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.find('div', class_='pagination')

        nav_items = pagination.find_all('li')
        item_labels = [item.findChild()['aria-label'] for item in nav_items]
        # If 'Next' is in item_labels, is_last_page becomes False.
        # Otherwise, is_last_page becomes True.
        is_last_page = False if 'Next' in item_labels else True

        page_index += 1

    return int(item_labels[-1])


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
        print(f'Scraping page {i}...')
        response = requests.get(f'{URL}&start={i * LIMIT}')
        soup = BeautifulSoup(response.text, 'html.parser')

        job_containers = soup.find_all('div', class_='slider_container')
        for job_container in job_containers:
            jobs.append(_extract_job(job_container))

    return jobs
