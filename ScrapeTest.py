import requests
import random
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

url = 'https://locations.wendys.com/united-states'

def getData(url):
    r = requests.get(url, headers=headers)
    soup = bs(r.text, 'html.parser')
    return soup


WenStates = []

pageItems = getData(url).find_all('li', {'class': 'Directory-listItem'})
for item in pageItems:
    states = {
        'State': item.find('a', {'class': 'Directory-listLink'}).text,
        'Link': 'https://locations.wendys.com/' + item.find('a', {'class': 'Directory-listLink'})['href']
    }

    WenStates.append(states)



WenCities = []

for WenState in WenStates:   
    currentState = WenState['State']
    stateSoup = getData(WenState['Link'])

    pageItems = stateSoup.find_all('li', {'class': 'Directory-listItem'})
    for item in pageItems:
        
        State = currentState
        City = item.find('a', {'class': 'Directory-listLink'}).text  
        locations = int(item.find('span', {'class': 'Directory-listLinkCount'}).text.strip("()"))
        
        if locations == 1:
            initLink = item.find('a', {'class': 'Directory-listLink'})['href']
            initLink = initLink[2 : ]
            finalLink = 'https://locations.wendys.com' + initLink
            subLink = ''   
        else:
            finalLink = ''
            subLink = 'https://locations.wendys.com' + item.find('a', {'class': 'Directory-listLink'})['href'].replace('.','')
            

        cities = {
            'State': State,
            'City': City,
            'Final-Link': finalLink,
            'Sub-Link': subLink,
        }

        WenCities.append(cities)
    


Links = []
print('Scraping Links....')

for WenCity in WenCities:
    
    
    if WenCity['Final-Link'] != '':
        finalLink = WenCity['Final-Link']
        Links.append(finalLink)
    elif WenCity['Sub-Link'] != '':
        citySoup = getData(WenCity['Sub-Link'])
        
        pageItems = citySoup.find_all('div', {'class': 'Teaser-link'})
        for item in pageItems:
            initLink = item.find('a', {'class': 'Link'})['href']
            initLink = initLink[5: ]
            finalLink = 'https://locations.wendys.com' + initLink
            Links.append(finalLink)
            


#print(len(Links))

print('Links Scraped Successfully')

WenCitiesData = []

print('Scraping Data....')

count = 0

for Link in Links:
#    print(Link)
    citySoup = getData(Link)
    pageItems = citySoup.find('div', {'class': 'LocationInfo-content'})


    stateExist = pageItems.find('abbr', {'class': 'c-address-state'})
    if stateExist != None:
        State = pageItems.find('abbr', {'class': 'c-address-state'})['title']
    else:
        State = 'Not Available'
    
    
    cityExist = pageItems.find('span', {'class': 'c-address-city'})
    if cityExist != None:
        City = pageItems.find('span', {'class': 'c-address-city'}).text
    else:
        City = 'Not Available'
    

    zipExist = pageItems.find('span', {'class': 'c-address-postal-code'})
    if zipExist != None:
        Zip = pageItems.find('span', {'class': 'c-address-postal-code'}).text
    else:
        Zip = 'Not Available'

    
    streetExist = pageItems.find('span', {'class': 'c-address-street-1'})
    if streetExist != None:
        Street = pageItems.find('span', {'class': 'c-address-street-1'}).text
    else:
        Street = 'Not Available'
    
    
    numExist = pageItems.find('span', {'class': 'c-phone-number-span c-phone-main-number-span'})
    if numExist != None:
        Number = pageItems.find('span', {'class': 'c-phone-number-span c-phone-main-number-span'}).text
    else:
        Number = 'Not Available'
    
    
    locExist = citySoup.find('a', {'class': 'c-get-directions-button'})
    if locExist != None:
        Location = citySoup.find('a', {'class': 'c-get-directions-button'})['href']
    else:
        Location = 'Not Available'
    

    opened = pageItems.find('div', {'class': 'c-location-hours-details-wrapper js-location-hours'})
    openHours = opened.find_all('tr', {'class': 'c-location-hours-details-row js-day-of-week-row highlight-text highlight-background'})

    date = []

    for openHour in openHours:
        dateTime = openHour['content']


        date.append(dateTime)


    data = {
        'State': State,
        'City': City,
        'Zip-Code': Zip,
        'Street': Street,
        'Number': Number,
        'Location': Location,
        'Open-Hours': date,
    }
    
    count += 1
    print(f'Scraped Data from Link: {count}')
#    print(data)
    WenCitiesData.append(data)
    wait_time = random.randint(15, 45)
    print(f'Waiting for {wait_time} seconds')
    sleep(wait_time)


print('Data Scraped Successfully')

print(len(WenCitiesData))

df = pd.DataFrame(WenCitiesData)
df.to_csv('WendysData.csv', index=False)
print('Successfully Scraped')
