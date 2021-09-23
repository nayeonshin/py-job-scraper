from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stackoverflow_jobs
from save import *

indeed_jobs = get_indeed_jobs()
stackoverflow_jobs = get_stackoverflow_jobs()
jobs = stackoverflow_jobs + indeed_jobs
save_to_file(jobs)
