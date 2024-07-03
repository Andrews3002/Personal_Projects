from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

baseurl = 'https://warframe.fandom.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

#selenium code to perform http requests and access elements that need to wait for javascript scripts to finish running in order to have data.
driver = webdriver.Chrome()
driver.get('https://warframe.fandom.com/wiki/Warframes')
sleep(1)
website = driver.page_source

#using the request library to draw data from static fixed html websites that don't use javascript scripts to load its data
# website = requests.get('https://warframe.fandom.com/wiki/Warframes')

#beautifulSoup is now used to scrape the actual data that has been dynamically loaded from the website
soup = BeautifulSoup(website, 'lxml')

warframeList = soup.find_all('span', class_='WarframeNavBoxText')

frameLinks = []
frameList = []

for warframe in warframeList:
    for link in warframe.find_all('a', href=True):
        frameLinks.append(baseurl + link['href'])

for link in frameLinks:
    #selenium code to perform http requests and access elements that need to wait for javascript scripts to finish running in order to have data.
    driver.get(link)
    sleep(1)
    page = driver.page_source
    
    #beautifulSoup is now used to scrape the actual data that has been dynamically loaded from the website
    #page = requests.get(link, headers=headers)
    
    soup = BeautifulSoup(page, 'lxml')
    Sex = soup.find('div', {'data-source': 'Sex'}).div.text.strip()
    Name = soup.find('aside', class_='portable-infobox pi-background pi-border-color pi-theme-wikia pi-layout-default').h2.b.text.strip()

    frame = {
        'Name': Name,
        'Sex': Sex
    }   
    
    frameList.append(frame)

print(frameList)

print('')
print('')

import pandas as pd
df = pd.DataFrame.from_dict(frameList)

print(df)

driver.close()







