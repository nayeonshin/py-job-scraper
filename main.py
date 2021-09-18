from indeed import *

last_indeed_page = get_last_page_num()
indeed_jobs = extract_jobs(last_indeed_page)
