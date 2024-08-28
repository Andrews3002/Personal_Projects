from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep
import pickle
import json

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

driver.get('https://depository.oprtt.org/PublicBodyLOB/Prequalified?id=122')

username_field = driver.find_element(By.NAME, 'UserName')
password_field = driver.find_element(By.NAME, 'Password')

username_field.send_keys('JMaraj-gheesan@energy.gov.tt')
password_field.send_keys('Dedicate!23')

# Assuming manual captcha or 2FA
WebDriverWait(driver, 30).until(EC.url_to_be('https://depository.oprtt.org/publicbody/details?id=122'))


driver.get('https://depository.oprtt.org/publicbodylob?id=122')

with open("line-data.json", "w") as file:
    website = driver.page_source
    soup = BeautifulSoup(website, 'lxml')

    baseurl = 'https://depository.oprtt.org'
    lobElementsGroup = soup.find('div', class_='card-body row') 
    lobElements = lobElementsGroup.find_all('div', class_='card-header text-muted border-bottom-0')


    lobLinks = []
    lineNames = []
    
    for lobElement in lobElements:
        name = lobElement.find('h5', class_='card-title').text
        lineNames.append(name)
        for link in lobElement.find_all('a', href=True):
            if link.text == 'View':
                lobLinks.append(baseurl + link['href'])
    
    
    
    lobIndex = 0
    for lobLink in lobLinks:
        driver.get(lobLink)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        
        OPRcode = soup.find('input', {'id': 'LineOfBusinessCd'}).get('value')
        OPRlevel = soup.find('input', {'id': 'PreQualificationValueCategoryCd'}).get('value')
        LineName = lineNames[lobIndex]
        
        

        entry = {
            'LOB name': LineName,
            'code': OPRcode,
            'Level': OPRlevel
        }
        
        json_entry = json.dumps(entry, indent=4)
        file.write(json_entry + ",\n")
        print(json_entry)
        lobIndex = lobIndex + 1


driver.quit()
