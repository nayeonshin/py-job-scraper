import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def _check_has_first_page_end() -> bool:
    """Check if the first page has a link to the last page"""
    first_response = requests.get(URL)
    soup = BeautifulSoup(first_response.text, "html.parser")
    pagination = soup.find("div", class_="pagination")

    nav_items = pagination.find_all("li")
    item_labels = [item.findChild()["aria-label"] for item in nav_items]
    # If 'Next' is not in nav, the first page has the last page link.
    return "Next" not in item_labels


def _extract_last_page_num() -> int:
    """Get the last page number"""
    is_last_page = _check_has_first_page_end()
    item_labels = []
    page_index = 0

    while not is_last_page:
        response = requests.get(URL + f"&start={page_index * LIMIT}")
        soup = BeautifulSoup(response.text, "html.parser")
        pagination = soup.find("div", class_="pagination")

        nav_items = pagination.find_all("li")
        item_labels = [item.findChild()["aria-label"] for item in nav_items]
        is_last_page = False if "Next" in item_labels else True

        page_index += 1

    return int(item_labels[-1])


def _format_location(location: str) -> str:
    """Get a location with spaces around plus and template"""
    return location.replace("+", " + ").replace("•", " • ")


def _extract_job(html):
    """
    Get a dictionary of a job's information
    :param html: Tag
    :return: dict[str, str]
    """
    title = html.find("span", title=True).string
    company = html.find("span", class_="companyName").string
    location = _format_location(html.find("div", class_="companyLocation").text)
    job_id = html.parent["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}&tk=1fg49gh9apiab801&from=serp&vjs=3",
    }


def _extract_jobs(last_page_num: int):
    """
    Get a list of job info's dictionaries
    :return: list[dict[str, str]]
    """
    jobs = []

    for i in range(last_page_num):
        print(f"Scraping Indeed's page {i}...")
        response = requests.get(f"{URL}&start={i * LIMIT}")
        soup = BeautifulSoup(response.text, "html.parser")

        job_containers = soup.find_all("div", class_="slider_container")
        for job_container in job_containers:
            jobs.append(_extract_job(job_container))

    return jobs


def get_jobs():
    """
    Extract jobs until the last page
    :return: list[dict[str, str]]
    """
    last_page_num = _extract_last_page_num()
    jobs = _extract_jobs(last_page_num)
    return jobs
