from bs4 import BeautifulSoup
import requests

INDEED_URL = 'https://www.indeed.com/jobs?q=python&limit=50'


def extract_indeed_pages():
    is_end_of_pages = False
    max_page_num = 0
    page_index = 0

    indeed_result = requests.get(INDEED_URL)
    indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')
    pagination = indeed_soup.find('div', class_='pagination')
    pages = pagination('li')

    for i in range(len(pages) - 1):  # Excludes the next button
        page_num = int(pages[i].findChild().string)
        if page_num > max_page_num:
            max_page_num = page_num

    if pages[-1].findChild()['aria-label'] != 'Next':
        # First page is the last page
        is_end_of_pages = True

    while not is_end_of_pages:
        if pages[-1].findChild()['aria-label'] == 'Next':  # There are more pages.
            indeed_result = requests.get(INDEED_URL + f'&start={(page_index + 1) * 50}')
            indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')
            pagination = indeed_soup.find('div', class_='pagination')
            pages = pagination('li')
            for i in range(1, len(pages)):  # Excludes the previous button
                li_child = pages[i].findChild().string
                if li_child is None:
                    continue
                else:
                    page_num = int(li_child)
                    if page_num > max_page_num:
                        max_page_num = page_num
        else:
            is_end_of_pages = True

        page_index += 1
