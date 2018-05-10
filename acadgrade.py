import json
from getpass import getpass
from pathlib import Path

import mechanicalsoup


home_dir = Path.home()
data_file = home_dir.joinpath('.acadgrade')

if Path.exists(data_file):
    with open(data_file) as f:
        saved_data = json.load(f)
else:
    saved_data = {}

browser = mechanicalsoup.StatefulBrowser()

browser.open('https://auto.iitg.ernet.in/acadgrade/index.jsp')
browser.select_form()

if 'uid' not in saved_data or 'pass' not in saved_data:
    saved_data['uid'] = input('Please enter your webmail username:\n')
    saved_data['pass'] = getpass('Please enter your webmail password:\n')
    with open(data_file, 'w') as f:
        json.dump(saved_data, f)

browser['uid'] = saved_data['uid']
browser['pass'] = saved_data['pass']

browser.submit_selected()

page = browser.get_current_page()
data = page.find_all('tr')[1:]

print(f"Hello {saved_data['uid']}, your current course status is as follows:")

course_status = {}
for row in data:
    row_data = list(map(lambda cell: cell.text, row.find_all('td')))
    name, status = row_data[1], row_data[3]
    print(f'Course: {name}, Status: {status}')
