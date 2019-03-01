'''get pdf from ostep website'''

from collections import defaultdict
from bs4 import BeautifulSoup as BS
from pathlib import Path
import requests


pdfs = defaultdict(list)

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

appendix_idx = 'A'

for i, chap in enumerate(pdfs):
    chap_dir = Path(str(i) + ' ' + chap)
    chap_dir.mkdir(exist_ok=True)
    for title, url in pdfs[chap]:
        title = title.replace('/', '|').replace(':', '_')
        if title[1] == ' ':
            title = '0' + title
        if title.endswith(' code'):
            title = title.rstrip(' code')
        if chap == 'Appendices':
            title = appendix_idx + ' ' + title
            appendix_idx = chr(ord(appendix_idx) + 1)
        elif not title[0].isdigit():
            title = '00 ' + title
        print(title)
        pdf = chap_dir / (title + '.pdf')
        if pdf.exists():
            continue
        with pdf.open('wb') as f:
            f.write(requests.get(url).content)
