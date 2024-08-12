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

username_field = wait.until(EC.presence_of_element_located((By.NAME, 'UserName')))
password_field = wait.until(EC.presence_of_element_located((By.NAME, 'Password')))


username_field.send_keys('JMaraj-gheesan@energy.gov.tt')
password_field.send_keys('Dedicate!23')

# Assuming manual captcha or 2FA
WebDriverWait(driver, 30).until(EC.url_to_be('https://depository.oprtt.org/publicbodylob/Create?id=122'))

with open("LineLayers_Entries.json", "w") as file:
    website = driver.page_source
    soup = BeautifulSoup(website, 'lxml')

    baseurl = 'https://depository.oprtt.org'
    lobElementsGroup = soup.find('div', class_='col-md-8') 
    lobElements = lobElementsGroup.find_all('div', class_='input-group m-1')

    # lobLinks = [baseurl + link['href'] for lobElement in lobElements for link in lobElement.find_all('a', href=True)]

    L1_links = []
    L1_lines = []

    for lobElement in lobElements:
        for link in lobElement.find_all('a', href=True):
            L1_links.append(baseurl + link['href'])
            L1_lines.append(link.text)
            
    l1 = 0    
    for link1 in L1_links:
        
        L1_line = L1_lines[l1]
        
        driver.get(link1)
        website = driver.page_source
        soup = BeautifulSoup(website, 'lxml')
        
        lobElementsGroup = soup.find('div', class_='col-md-8') 
        lobElements = lobElementsGroup.find_all('div', class_='input-group m-1')
        
        L2_links = []
        L2_lines = []
        
        for lobElement in lobElements:
            for link in lobElement.find_all('a', href=True):
                L2_links.append(baseurl + link['href'])
                L2_lines.append(link.text)
                
        l2 = 0
        for link2 in L2_links:
            
            L2_line = L2_lines[l2]
            
            driver.get(link2)
            website = driver.page_source
            soup = BeautifulSoup(website, 'lxml')
            
            lobElementsGroup = soup.find('div', class_='col-md-8') 
            lobElements = lobElementsGroup.find_all('div', class_='input-group m-1')
            
            L3_links = []
            L3_lines = []
            
            for lobElement in lobElements:
                for link in lobElement.find_all('a', href=True):
                    L3_links.append(baseurl + link['href'])
                    L3_lines.append(link.text)
                        
            l3 = 0
            for link3 in L3_links:
                    
                L3_line = L3_lines[l3]
                
                driver.get(link3)
                website = driver.page_source
                soup = BeautifulSoup(website, 'lxml')
                
                lobElementsGroup = soup.find('div', class_='col-md-8') 
                lobElements = lobElementsGroup.find_all('div', class_='custom-control custom-checkbox col-md-8 col-sm-6')
                
                for lobElement in lobElements:
                    for line in lobElement.find_all('label', class_='permissionLbl custom-control-label'):
                        L4_line = line.text
                        entry = {'L1': L1_line, 'L2': L2_line, 'L3': L3_line, 'L4': L4_line}
                        
                    json_entry = json.dumps(entry, indent=4)
                    file.write(json_entry + ",\n")
                    print(json_entry)
                l3 = l3 + 1
            l2 = l2 + 1
        l1 = l1 + 1              

driver.quit()

