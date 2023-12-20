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


def getCh(vernum, ver, book, ch):
    '''
    getCh gets the verses in a specified chapter
    '''
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


if (1):
    # Scrape - only load once
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # function calls

    getCh(2692, "NASB2020", "1TI", 2)
    getCh(2692, "NASB2020", "1TI", 3)
    getCh(2692, "NASB2020", "1TI", 4)
    getCh(2692, "NASB2020", "1TI", 5)
    getCh(2692, "NASB2020", "1TI", 6)


if (0):
    niv = []
    kjv = []
    nkjv = []
    nasb = []
    nrsv = []
    with open("NIV.csv") as f:
        for row in f:
            niv.append(row.split(",")[0])
    with open("KJV.csv") as f:
        for row in f:
            kjv.append(row.split(",")[0])
    with open("NKJV.csv") as f:
        for row in f:
            nkjv.append(row.split(",")[0])
    with open("NASB2020.csv") as f:
        for row in f:
            nasb.append(row.split(",")[0])
    with open("NRSV.csv") as f:
        for row in f:
            nrsv.append(row.split(",")[0])

    # NIV and KJV - done - 3John1:15 not in KJV (combined with 14)
    # NIV and NKJV - done - 3John1:15 not in NKJV (combined with 14)
    # NIV and NASB - done - 13 verses taken out of NASB
    # repeatniv = []
    # for x in nasb:
    #     if x in repeatniv:
    #         print(x)
    #     else:
    #         repeatniv.append(x)
    print(f"{[x for x in nrsv if x not in niv]}")
