import requests

indeed_result = requests.get('https://www.indeed.com/jobs?as_and=python&limit=50')

print(indeed_result.text)
