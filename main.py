from bs4 import BeautifulSoup
import csv
import requests
import lxml
import pandas as pd
import datetime as dt
import os.path

# Create an array that stores the links of the articles and have each of the if/for statements check to see if the link has been pulled before trying to scrape

# Checks to see if our outfile for the news articles has been created in the PWD.
try:
    if os.path.isfile('news_scrape.csv'):
        csv_file = open('news_scrape.csv', 'a', encoding='utf-8-sig')
        csv_writer = csv.writer(csv_file)
    # If the file does not exist, creates it
    else:
        csv_file = open('news_scrape.csv', 'w', encoding='utf-8-sig')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['subjects', 'scraped', 'headline', 'summary', 'link', 'posted'])
except Exception as e:
    print(e)
    exit()

try:
    # Opens our subjects.csv and stores it in an array
    subject = []
    with open('subjects.csv', encoding='utf-8-sig', newline='') as f:
        for row in csv.reader(f):
            subject.append(row[0])
except Exception as e:
    print(e)
    print("subjects.csv could not be loaded or does not exist, please verify you have that file in the root directory of this project with atleast one subject.")

try:
    # Opens our sites.csv and stores it in an array
    sites = []
    with open('sites.csv', encoding='utf-8-sig', newline='') as file:
        for row in csv.reader(file):
            sites.append(row[0])
except Exception as e:
    print(e)
    print("sites.csv could not be loaded or does not exist, please verify you have that file in the root directory of this project with atleast one site URL.")

for site in sites:
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'lxml')

    # Scrapes news from the website The Hacker News
    if "thehackernews" in site:
        for article in soup.find_all('div', class_='body-post clear'):
            for subjects in subject:
                if article.find_all(text=lambda t: t and subjects in t):
                    try:
                        headline = article.h2.text
                        summary = article.find('div', class_='home-desc').text
                        link = article.find('a', class_='story-link')['href']
                        date = dt.date.today()
                    except Exception as e:
                        print(e)
                        continue

                    print(headline, summary, link, sep='\n')
                    print()

                    try:
                        csv_writer.writerow([subjects, date, headline, summary, link])
                    except Exception as e:
                        print(e)
                else:
                    continue

    # Scrapes news from Threatpost
    elif "threatpost" in site:
        for article in soup.find_all('article'):
            for subjects in subject:
                if article.find_all(text=lambda t: t and subjects in t):

                    try:
                        headline = article.h2.text
                        summary = article.find('p').text
                        link = article.find('a')['href']
                        date = dt.date.today()
                        posted = article.find('time').text
                    except Exception as e:
                        print(e)
                        continue
                    # Prints our scraped data to the console for logging and an extra line to keep it clean
                    print(headline, summary, link, posted, sep='\n')
                    print()
                    # Tries to write the data to the news_scape.csv and skips that article if it runs into trouble
                    try:
                        csv_writer.writerow([subjects, date, headline, summary, link, posted])
                    except Exception as e:
                        print(e)
                else:
                    continue

    # Scrapes news from Krebs on security
    elif "krebsonsecurity" in site:
        for article in soup.find_all('div', class_='post-smallerfont'):
            for subjects in subject:
                if article.find_all(text=lambda t: t and subjects in t):

                    try:
                        headline = article.h2.text
                        summary = article.find('p').text
                        link = article.find('a')['href']
                        date = dt.date.today()
                    except Exception as e:
                        print(e)
                        continue
                    # Prints our scraped data to the console for logging and an extra line to keep it clean
                    print(headline, summary, link, sep='\n')
                    print()
                    # Tries to write the data to the news_scape.csv and skips that article if it runs into trouble
                    try:
                        csv_writer.writerow([subjects, date, headline, summary, link])
                    except Exception as e:
                        print(e)
                else:
                    continue

    # Scrapes news from ZDNet
    elif "zdnet" in site:
        for article in soup.find_all('div', {"class": "content"}):
            for subjects in subject:
                if article.find_all(text=lambda t: t and subjects in t):
                    link = article.find('a')['href']
                    exclude = ['video', 'product']
                    if not any(exclusion in link for exclusion in exclude):
                        try:
                            headline = article.find('a').text
                            summary = article.find('p', {"class": "summary"}).text
                            link = "https://www.zdnet.com" + link
                            date = dt.date.today()
                            posted = article.find('span').text
                        except Exception as e:
                            print(e)
                            continue
                        # Prints our scraped data to the console for logging and an extra line to keep it clean
                        print(headline, summary, link, posted, sep='\n')
                        print()
                        # Tries to write the data to the news_scape.csv and skips that article if it runs into trouble
                        try:
                            csv_writer.writerow([subjects, date, headline, summary, link, posted])
                        except Exception as e:
                            print(e)
                    else:
                        print('Contains a video or Ad... Skipping...')
                else:
                    continue

    # This is a catch all for all other sites with generic article layouts
    else:
        for article in soup.find_all('article'):
            for subjects in subject:
                if article.find_all(text=lambda t: t and subjects in t):

                    try:
                        headline = article.h2.text
                        summary = article.find('p').text
                        link = article.find('a')['href']
                        date = dt.date.today()
                        posted = article.find('time').text
                    except Exception as e:
                        print(e)
                        continue
                    # Prints our scraped data to the console for logging and an extra line to keep it clean
                    print(headline, summary, link, posted, sep='\n')
                    print()
                    # Tries to write the data to the news_scape.csv and skips that article if it runs into trouble
                    try:
                        csv_writer.writerow([subjects, date, headline, summary, link, posted])
                    except Exception as e:
                        print(e)
                else:
                    continue

csv_file.close()

# This goes in after the data has been scraped and removed duplicates

df = pd.read_csv('news_scrape.csv', encoding='utf-8-sig')
df.drop_duplicates(subset=['link'], keep='first', inplace=True)
df.to_csv('news_scrape.csv', index=False)
