'''get pdf from ostep website'''

from collections import defaultdict
from bs4 import BeautifulSoup as BS
from pathlib import Path
import requests


pdfs = defaultdict(list)

if not Path('ostep.html').exists():
    text = requests.get('http://pages.cs.wisc.edu/~remzi/OSTEP/').text
    with open('ostep.html', 'w') as f:
        f.write(text)

url = 'http://pages.cs.wisc.edu/~remzi/OSTEP/%s'

soup = BS(open('ostep.html').read(), 'lxml')
table = soup('table')[-1]

header = [x.b.string for x in table.tr('td')]
header[2] = header[1]

rows = table('tr')
for row in rows[1:]:
    for i, td in enumerate(row('td')):
        a = td.a
        if a is None:
            continue
        pdfs[header[i]].append((td.text.strip(), url % a['href']))

for i, chap in enumerate(pdfs):
    chap_dir = Path(str(i) + ' ' + chap)
    chap_dir.mkdir(exist_ok=True)
    for title, url in pdfs[chap]:
        title = title.replace('/', '_').replace(':', '_')
        print(title)
        pdf = chap_dir / (title + '.pdf')
        if pdf.exists():
            continue
        with pdf.open('wb') as f:
            f.write(requests.get(url).content)
