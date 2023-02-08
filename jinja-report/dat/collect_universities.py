#!/usr/bin/env python3


import os
import re
import requests
from bs4 import BeautifulSoup


base_url = 'https://www.4icu.org/reviews/'

pg = 2
dat = {}

while 1:

    url = os.path.join(base_url, 'index%d.htm' % pg)
    print('processing %s' % url)

    page = requests.get(url)
    status = page.status_code
    if status != 200:
        break

    soup = BeautifulSoup(page.content, 'html.parser')
    tabledata = soup.find_all('td')

    for i in range(0, len(tabledata), 2):
        university = tabledata[i].text.strip().replace(',', ' - ')
        country = tabledata[i+1].text.strip()
        dat[university] = country

    pg += 1

with open('university-data.csv', 'w') as f:
    f.write('university,country\n')
    for k, v in dat.items():
        f.write('%s,%s\n' % (k, v))

#html = list(soup.children)[2]
#body = [c for c in html.children][3]
