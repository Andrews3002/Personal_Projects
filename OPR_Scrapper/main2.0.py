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
WebDriverWait(driver, 30).until(EC.url_to_be('https://depository.oprtt.org/PublicBodyLOB/Prequalified?id=122'))

driver.get('https://depository.oprtt.org/PublicBodyLOB/Prequalified?id=122')

with open("OPR_Entries.json", "w") as file:
    website = driver.page_source
    soup = BeautifulSoup(website, 'lxml')

    baseurl = 'https://depository.oprtt.org'
    lobElementsGroup = soup.find('div', class_='col-md-12') 
    lobElements = lobElementsGroup.find_all('li')

    # lobLinks = [baseurl + link['href'] for lobElement in lobElements for link in lobElement.find_all('a', href=True)]
    lobLinks = []
    oprList = []
    
    cont = 1
    for lobElement in lobElements:
        if cont >= 1326:
            for link in lobElement.find_all('a', href=True):
                lobLinks.append(baseurl + link['href'])
        cont = cont + 1
    
    lobIndex = 0
    for lobLink in lobLinks:
        driver.get(lobLink)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        
        lineOfBusiness = soup.find('b', class_='pull-left').text
        
        companyElements = soup.find_all('tr')  
    
        tableElements = []
        status = []
        score = []
        
        companyLinks = []
        
        print('')
        print('')
        print(f'--------------------------------------------------------------------------------------{lineOfBusiness}')
        print('')
        print('')
        
        cont = 1
        for companyElement in companyElements:
            if lobIndex == 0:
                if cont >= 55 + 1:
                    for link2 in companyElement.find_all('a', href=True):
                            companyLinks.append(baseurl + link2['href'])
                    
                    tableElements = companyElement.find_all('td')
                    if len(tableElements) > 2:
                        status.append(tableElements[1].text)
                        score.append(tableElements[2].text)
                else:
                    cont = cont + 1
                    continue
            else:     
                for link2 in companyElement.find_all('a', href=True):
                    companyLinks.append(baseurl + link2['href'])
            
                tableElements = companyElement.find_all('td')
                if len(tableElements) > 2:
                    status.append(tableElements[1].text)
                    score.append(tableElements[2].text)
                    
            cont = cont + 1

        for outerDataIndex, companyLink in enumerate(companyLinks):
            driver.get(companyLink)
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            
            wholeCard = soup.find('div', class_='card-body')
            companyDataCards = wholeCard.find_all('div', class_='col-md-6 col-12')
            detailsLink = baseurl + companyDataCards[0].div.a['href']
            addressLink = baseurl + companyDataCards[3].div.a['href']
            services = soup.find('li', class_='list-group-item').p.text
            name = soup.find('h3', class_='profile-username text-center').text
            supplierNumber = soup.find('span', class_='text-muted').text
            
            driver.get(addressLink)
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            addressLink2Table = soup.find('table', class_='datatable table table-striped published-table')
            if addressLink2Table is None:
                addressDetails = {field: '' for field in [
                    'BuildingNm', 'Street1Addr', 'Street2Addr', 'Street3Addr', 'CityNm', 
                    'GeographicLocationCd', 'CountryCd', 'PostalCd', 'TelephoneNum', 
                    'AddressTypeTp', 'CreBy', 'CreDttm'
                ]}
            else:
                addressLink2 = baseurl + addressLink2Table.find('a').get('href')
                driver.get(addressLink2)
                page = driver.page_source
                soup = BeautifulSoup(page, 'lxml')

                # Extracting address details
                addressDetails = {field: soup.find('input', {'id': field})['value'] for field in [
                    'BuildingNm', 'Street1Addr', 'Street2Addr', 'Street3Addr', 'CityNm', 
                    'GeographicLocationCd', 'CountryCd', 'PostalCd', 'TelephoneNum', 
                    'AddressTypeTp', 'CreBy', 'CreDttm'
                ]}
            
            driver.get(detailsLink)
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            
            # Extracting details
            details = {field: soup.find('input', {'id': field})['value'] for field in [
                'SupplierNm', 'SupplierTypeCd', 'EmployeesQty', 'NatureOfBusinessOrServicesTxt', 
                'FirmLegalNm', 'Operated_Under_Other_Business_', 'OtherBusinessNm', 
                'Subsidiary_Affiliate_Firm_', 'AffiliatesNm', 'Legal_Query_', 
                'LegalQueryDetailsTxt', 'IncorporationYr', 'IncorporationCountryCd', 
                'CompanyWebsiteUrl', 'CreBy', 'CreDttm'
            ]}

            entry = {
                'Supplier Name': details['SupplierNm'],
                'Status': status[outerDataIndex],
                'Score': score[outerDataIndex],
                'Line Of Business': lineOfBusiness,
                'Supplier Number': supplierNumber,
                'Services': services,
                **addressDetails,
                **details
            }

            oprList.append(entry)
            
            json_entry = json.dumps(entry, indent=4)
            file.write(json_entry + ",\n")
            print(json_entry)
        lobIndex = lobIndex + 1

df = pd.DataFrame.from_dict(oprList)
df.to_csv('OPR.csv', index=False)
print(df)

driver.quit()
