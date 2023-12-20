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
from datetime import datetime

# Scrape
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


def getCh(vernum, ver, book, ch):
    try:
        d = {}
        driver.get(
            f"https://www.bible.com/bible/{vernum}/{book}.{ch}.{ver}")
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        verses = soup.select(f'span[data-usfm*="{book}"]')

        for v in verses:
            verse = v.select(
                'span[class*="ChapterContent_content__"]')
            a = v['data-usfm']
            if (a in d.keys()):
                d[a] += " ".join([vsub.string for vsub in verse if vsub.string is not None])
            else:
                d[a] = " ".join(
                    [vsub.string for vsub in verse if vsub.string is not None])

        for key in d:
            with open(f'output.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([key, str(d[key])])
    except Exception as e:
        with open('errorlog.txt', 'a') as f:
            f.write(f"{datetime.now()} ERROR {ver} {book} {ch}: {e}\n")
