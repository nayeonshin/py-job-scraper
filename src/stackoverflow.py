import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"


def _extract_last_page_num() -> int:
    """Get the last page number"""
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    page_elements = soup.find("div", class_="s-pagination").find_all("a")
    last_page_num = page_elements[-2].get_text(strip=True)  # Excludes 'next'
    return int(last_page_num)


def _extract_job(html):
    """
    Get a dictionary of a job's information
    :param html: Tag
    :return: dict[str, str]
    """
    title_element = html.find("h2")
    company_and_location_element = html.find("h3")
    title = company = location = link = ""
    if title_element:
        a = title_element.find("a")
        title = a["title"]
        link = "https://stackoverflow.com" + a["href"]
    if company_and_location_element:
        company_element, location_element = company_and_location_element.find_all(
            "span", recursive=False
        )  # Only gets spans in the first depth
        company, location = company_element.get_text(
            strip=True
        ), location_element.get_text(strip=True)
    return {"title": title, "company": company, "location": location, "link": link}


def _extract_jobs(last_page_num):
    """
    Get a list of job info's dictionaries
    :param last_page_num: int
    :return: list[dict[str, str]]
    """
    jobs = []
    for i in range(1, last_page_num + 1):
        print(f"Scraping Stack Overflow's page {i}...")
        response = requests.get(f"{URL}&pg={i}")
        soup = BeautifulSoup(response.text, "html.parser")
        job_elements = soup.find_all("div", class_="fl1")
        for element in job_elements:
            job = _extract_job(element)
            if list(job.values()) == ["", "", "", ""]:
                # There's no title, company, location, and link.
                continue
            else:
                jobs.append(job)
    return jobs


def get_jobs():
    """
    Extract jobs until the last page
    :return: list[dict[str, str]]
    """
    last_page_num = _extract_last_page_num()
    jobs = _extract_jobs(last_page_num)
    return jobs
