'''concat pdfs into a book'''
from pathlib import Path
from PyPDF2 import PdfFileMerger

current_dir = Path('.')
pdfs = []
for d in sorted(current_dir.iterdir()):
    if not d.is_dir():
        continue
    for file in sorted(d.iterdir()):
        if file.suffix == '.pdf':
            pdfs.append(file)

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf.open('rb'),
                  bookmark=pdf.name.split('.')[0].replace('_', ':')
                  .replace('|', '/'))

with open('ostep.pdf', 'wb') as fout:
    merger.write(fout)
