from bs4 import BeautifulSoup
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

webdriver_path = 'C:/Users/alexa/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe/'

chrome_profile_path = "C:/Users/alexa/AppData/Local/Google/Chrome/User Data"

driver = webdriver.Chrome()

driver.get('https://depository.oprtt.org/PublicBodyLOB/Prequalified?id=122')

username_field = driver.find_element(By.NAME, 'UserName')
password_field = driver.find_element(By.NAME, 'Password')

username_field.send_keys('JMaraj-gheesan@energy.gov.tt')
password_field.send_keys('Dedicate!23')

sleep(30)


driver.get('https://depository.oprtt.org/PublicBodyLOB/Prequalified?id=122')

#selenium code to perform http requests and access elements that need to wait for javascript scripts to finish running in order to have data.
sleep(1)

print('Current URL', driver.current_url)        

website = driver.page_source

#use this code to utilize selenium when scrapping a dynamic site that uses javascript to populate its data
# website = requests.get('https://depository.oprtt.org/PublicBodyLOB/Prequalified?id=122')

#use this code when scrapping a static site that has all its data directly stored in its html document
soup = BeautifulSoup(website, 'lxml')


baseurl = 'https://depository.oprtt.org'

lobElementsGroup = soup.find('div', class_='col-md-12') 
lobElements = lobElementsGroup.find_all('li')

lobLinks = []
oprList = []

for lobElement in lobElements:
    for link in lobElement.find_all('a', href=True):
        lobLinks.append(baseurl + link['href'])

i = 1
x = 1
for lobLink in lobLinks:
    #use this code to utilize selenium when scrapping a dynamic site that uses javascript to populate its data
    driver.get(lobLink)
    # sleep(1)
    page = driver.page_source
    #use this code when scrapping a static site that has all its data directly stored in its html document
    # page = requests.get(lobLink, headers=headers)
    
    soup = BeautifulSoup(page, 'lxml')
    
    lineOfBusiness = soup.find('b', class_='pull-left').text
    
    companyElements = soup.find_all('tr')  
    
    tableElements = []
    status = []
    score = []
    
    companyLinks = []
    
    print(f'--------------------------------------------------------------------------------------{lineOfBusiness}')
    print('')
    
    for companyElement in companyElements:
        for link2 in companyElement.find_all('a', href=True):
            companyLinks.append(baseurl + link2['href'])
        
        tableElements = companyElement.find_all('td')
        if len(tableElements) > 2:
            status.append(tableElements[1].text)
            score.append(tableElements[2].text)
        
        
    outerDataIndex = 0
    for companyLink in companyLinks:
        #use this code to utilize selenium when scrapping a dynamic site that uses javascript to populate its data
        driver.get(companyLink)
        page = driver.page_source
        #use this code when scrapping a static site that has all its data directly stored in its html document
        # page = requests.get(companyLink, headers=headers)
        
        soup = BeautifulSoup(page, 'lxml')
        
        
        #addressLink = soup.find('div', {'data-source': 'Address'}).a['href']
        wholeCard = soup.find('div', class_='card-body')
        companyDataCards = wholeCard.find_all('div', class_='col-md-6 col-12')
       
        detailsLink = baseurl + companyDataCards[0].div.a['href']
        addressLink = baseurl + companyDataCards[3].div.a['href']   
        services = soup.find('li', class_='list-group-item').p.text
        name = soup.find('h3', class_='profile-username text-center').text
        supplierNumber  = soup.find('span', class_='text-muted').text
        
        driver.get(addressLink)
        page = driver.page_source
        
        
        soup = BeautifulSoup(page, 'lxml')
        
        if soup.find('table', class_='datatable table table-striped published-table') == None:
            continue
         
        addressLink2Table = soup.find('table', class_='datatable table table-striped published-table')
        addressLink2 = baseurl + addressLink2Table.find('a').get('href')
        
        driver.get(addressLink2)
        page = driver.page_source
        
        soup = BeautifulSoup(page, 'lxml')
        
        input_element = soup.find('input', {'id': 'BuildingNm'})
        buildingName = input_element['value']
        input_element = soup.find('input', {'id': 'Street1Addr'})
        streetAddress1 = input_element['value']
        input_element = soup.find('input', {'id': 'Street2Addr'})
        streetAddress2 = input_element['value']
        input_element = soup.find('input', {'id': 'Street3Addr'})
        streetAddress3 = input_element['value']
        input_element = soup.find('input', {'id': 'CityNm'})
        city = input_element['value']
        input_element = soup.find('input', {'id': 'GeographicLocationCd'})
        municipality = input_element['value']
        input_element = soup.find('input', {'id': 'CountryCd'})
        country = input_element['value']
        input_element = soup.find('input', {'id': 'PostalCd'})
        postalCode = input_element['value']
        input_element = soup.find('input', {'id': 'TelephoneNum'})
        telephone = input_element['value']
        input_element = soup.find('input', {'id': 'AddressTypeTp'})
        addressType = input_element['value']
        input_element = soup.find('input', {'id': 'CreBy'})
        AddcreatedBy = input_element['value']
        input_element = soup.find('input', {'id': 'CreDttm'})
        AddcreatedTimestamp = input_element['value'] 
        
        driver.get(detailsLink)
        page = driver.page_source
        
        soup = BeautifulSoup(page, 'lxml')
        
        input_element = soup.find('input', {'id': 'SupplierNm'})
        supplierName = input_element['value']
        input_element = soup.find('input', {'id': 'SupplierTypeCd'})
        supplierType = input_element['value']
        input_element = soup.find('input', {'id': 'EmployeesQty'})
        employeesQuantity = input_element['value']
        input_element = soup.find('input', {'id': 'NatureOfBusinessOrServicesTxt'})
        natureOfBusinessOrServices = input_element['value']
        input_element = soup.find('input', {'id': 'FirmLegalNm'})
        firmLegalName = input_element['value']
        input_element = soup.find('input', {'id': 'Operated_Under_Other_Business_'})
        operatedUnderOtherBusiness = input_element['value']
        input_element = soup.find('input', {'id': 'OtherBusinessNm'})
        otherBusinessName = input_element['value']
        input_element = soup.find('input', {'id': 'Subsidiary_Affiliate_Firm_'})
        subsidiaryAffiliateFirm = input_element['value']
        input_element = soup.find('input', {'id': 'AffiliatesNm'})
        affiliatesName = input_element['value']
        input_element = soup.find('input', {'id': 'Legal_Query_'})
        legalQuery = input_element['value']
        input_element = soup.find('input', {'id': 'LegalQueryDetailsTxt'})
        legalQueryDetails = input_element['value']
        input_element = soup.find('input', {'id': 'IncorporationYr'})
        incorporationOrRegistrationYear = input_element['value']
        input_element = soup.find('input', {'id': 'IncorporationCountryCd'})
        incorporationOrRegistrationCountry = input_element['value']
        input_element = soup.find('input', {'id': 'CompanyWebsiteUrl'})
        websiteAddress = input_element['value']
        input_element = soup.find('input', {'id': 'CreBy'})
        DetcreatedBy = input_element['value']
        input_element = soup.find('input', {'id': 'CreDttm'})
        DetcreatedTimestamp = input_element['value']
        
            

        entry = {
            'Supplier Name': supplierName,
            'Status': status[outerDataIndex],
            'Score': score[outerDataIndex],
            'Line Of Business': lineOfBusiness,
            'Supplier Number': supplierNumber,
            'Services': services,
            'Building Name': buildingName,
            'Street Address 1': streetAddress1,
            'Street Address 2': streetAddress2,
            'Street Address 3': streetAddress3,
            'City Name': city,
            'Supplier Type': supplierType,
            'Employees Quantity': employeesQuantity,
            'Nature of Business or Services': natureOfBusinessOrServices,
            'Firm Legal Name': firmLegalName,
            'Operated Under Other Business': operatedUnderOtherBusiness,
            'Other Business Name': otherBusinessName,
            'Subsidiary/Affiliate Firm': subsidiaryAffiliateFirm,
            'Affiliates Name': affiliatesName,
            'Legal Query': legalQuery,
            'Legal Query Details': legalQueryDetails,
            'Incorporation or Registration Year': incorporationOrRegistrationYear,
            'Incorporation or Registration Country': incorporationOrRegistrationCountry,
            'Website Address': websiteAddress,
            'Municiplity': municipality,
            'Country': country,
            'Postal Code': postalCode,
            'Telephone Number': telephone,
            'Address Type': addressType,
            'Address Created By': AddcreatedBy,
            'Address Created Timestamp': AddcreatedTimestamp,
            'Details Created By': DetcreatedBy,
            'Details Created Timestamp': DetcreatedTimestamp
        } 
         
        oprList.append(entry)
        print(entry)
        print(f'working for inner-most details, entry---{x}')
        x = x+1
        print('')
        outerDataIndex = outerDataIndex+1
        
    print('')
    print('')
    
print(f'working for entry-------------------------------------------------------------{i}')
i = i+1


print(oprList)
print('')
print('')

df = pd.DataFrame.from_dict(oprList)

df.to_csv('OPR.csv', index=False)

print(df)
driver.close()







