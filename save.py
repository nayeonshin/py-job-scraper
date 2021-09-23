import csv
from time import strftime

FILE_NAME = 'Python-Jobs-' + strftime('%Y%m%d')


def save_to_file(jobs):
    """
    Write list jobs into csv
    :param jobs: list[dict[str, str]]
    :return: None
    """
    file = open(f'{FILE_NAME}.csv', mode='w', encoding="utf-8", newline='')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'location', 'link'])
    for job in jobs:
        writer.writerow(list(job.values()))
