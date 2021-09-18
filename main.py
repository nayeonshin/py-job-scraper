from bs4 import BeautifulSoup
import requests

# Goal: To get all the possible jobs
# Get each page until aria-level is Next
# If aria-level is Next, update the requests.get()'s url to
# ...&start=something
# If there's no aria-level == Next
# End the loop

page_index = 0
is_end_of_pages = False
li_children = []

indeed_result = requests.get('https://www.indeed.com/jobs?q=python&limit=50')
indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')
pagination = indeed_soup.find('div', class_='pagination')
pages = pagination('li')

for i in range(len(pages) - 1):  # Excludes last li, which is the next button
    child = pages[i].findChild()
    if child.name == 'a':
        li_children.append(child.find('span', class_='pn'))
    else:
        li_children.append(child)

print(li_children)

# while not is_end_of_pages:
#     if pages[-1].findChild()['aria-label'] == 'Next':  # There are more pages.
#         indeed_result = requests.get('https://www.indeed.com/jobs?q=python&limit=50'
#                                      + f'&start={(page_index + 1) * 50}')
#         indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')
#         pagination = indeed_soup.find('div', class_='pagination')
#         pages = pagination('li')
#         # print(pages)
#     else:
#         is_end_of_pages = True
#
#     page_index += 1
#     if page_index == 2:
#         break
