'''
This is a script to collect the verses of the Bible translations using Bible.com as the base site
It outputs 1 CSV version per version with the columns BOOK,CHAPTER,VERSE NUM,VERSE
This is built on the understanding that Bible.com follows the SLUG pattern:
  ...bible.com/bible/<version code>/<book>.<ch>.<version acronym>
You can observe this by loading up a Bible at bible.com and changing the language, chapters, and versions
'''

# imports
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Get list of version keys
versions = []
with open("versions.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        versions.append(row)

# Get list of book keys
books = []
with open("books.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        books.append(row)

# Scrape
if (1):
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    for ver in versions:
        for book in books:
            for ch in range(1, int(book[2]) + 1):
                try:
                    d = {}
                    driver.get(
                        f"https://www.bible.com/bible/{ver[2]}/{book[1]}.{ch}.{ver[1]}")
                    content = driver.page_source
                    soup = BeautifulSoup(content, 'html.parser')

                    verses = soup.select(f'span[data-usfm*="{book[1]}"]')

                    for v in verses:
                        verse = v.select(
                            'span[class*="ChapterContent_content__"]')
                        a = v['data-usfm']
                        if (a in d.keys()):
                            d[a] += " ".join([vsub.string for vsub in verse])
                        else:
                            d[a] = " ".join([vsub.string for vsub in verse])

                    for key in d:
                        with open(f'{ver[1]}.csv', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([key, str(d[key])])

                except Exception as e:
                    with open('errorlog.txt', 'a') as f:
                        f.write(f"ERROR {ver[1]} {book} {ch}: {e}\n")
