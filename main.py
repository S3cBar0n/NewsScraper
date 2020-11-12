from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd
import datetime as dt
import os.path


try:
    if os.path.isfile('news_scrape.csv'):
        csv_file = open('news_scrape.csv', 'a', encoding='utf-8-sig')
        csv_writer = csv.writer(csv_file)

    else:
        csv_file = open('news_scrape.csv', 'w', encoding='utf-8-sig')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['subjects', 'date', 'headline', 'summary', 'link'])
except Exception as e:
    print(e)
    exit()

subject = []

with open('subjects.csv', encoding='utf-8-sig', newline='') as f:
    for row in csv.reader(f):
        subject.append(row[0])

sites = []

with open('sites.csv', encoding='utf-8-sig', newline='') as file:
    for row in csv.reader(file):
        sites.append(row[0])

for site in sites:
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'lxml')

    # This is for when I have more than just this site for data

    for article in soup.find_all('div', class_='body-post clear'):
        for subjects in subject:
            if article.find_all(text=lambda t: t and subjects in t):

                headline = article.h2.text
                summary = article.find('div', class_='home-desc').text
                link = article.find('a', class_='story-link')['href']
                date = dt.date.today()

                print(headline, summary, link, sep='\n')
                print()

                try:
                    csv_writer.writerow([subjects, date, headline, summary, link])
                except Exception as e:
                    print(e)
            else:
                continue


csv_file.close()

df = pd.read_csv('news_scrape.csv', encoding='utf-8-sig')
df.drop_duplicates(subset=['link'], keep='first', inplace=True)
df.to_csv('news_scrape.csv', index=False)
