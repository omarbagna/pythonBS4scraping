import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep


# Assign a user-agent to the header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}


# A reusable function to pull website raw HTML code
def getData(url):
    r = requests.get(url, headers=headers)
    soup = bs(r.text, 'lxml')
    return soup


print ('Scraping data from links....\n')


pageLinks = pd.read_csv('LinksCount.csv')['Link'].to_list()

linksScraped = pd.read_csv('US Restaurants Locations.csv')['Source'].to_list()

#print(pageLinks)

toBeScraped = (len(pageLinks))-(len(linksScraped))
 
print(f'{len(pageLinks)} Total links\n')

print(f'{len(linksScraped)} links Already Scraped\n')

print(f'{toBeScraped} links to be Scraped\n')

print('Skipping already Scraped links...\n')


count = len(linksScraped)


pauseLimit = [i for i in range(1, 251000) if i % 5000 == 0]


for pageLink in pageLinks:

    linksScraped = pd.read_csv('US Restaurants Locations.csv')['Source'].to_list()
    
    if pageLink in linksScraped:

        pass

    else:

        if count not in pauseLimit:


            dataSoup = getData(pageLink)


            targetItems = dataSoup.find('div', class_ = 'restaurant-card')


            streetExist = targetItems.find('span', itemprop = 'streetAddress')
            if streetExist != None:
                street = streetExist.text.strip()

                if street == '':
                    street = '--'
                else:
                    pass
            else:
                street = '--'


            cityExist = targetItems.find('span', itemprop = 'addressLocality')
            if cityExist != None:
                city = cityExist.text.strip()

                if city == '':
                    city = '--'
                else:
                    pass
            else:
                city = '--'
                

            stateExist = targetItems.find('span', itemprop = 'addressRegion')
            if stateExist != None:
                state = stateExist.text.strip()

                if state == '':
                    state = '--'
                else:
                    pass
            else:
                state = '--'
                

            zipCodeExist = targetItems.find('span', itemprop = 'postalCode')
            if zipCodeExist != None:
                zipCode = zipCodeExist.text.strip()

            else:
                zipCode = '--'
                

            restaurantNameExist = targetItems.find('div', class_ = 'restaurant-title')
            if restaurantNameExist != None:
                restaurantName = restaurantNameExist.find('h1').text.strip()

                if restaurantName == '':
                    restaurantName = 'Not Available'
                else:
                    pass
            else:
                restaurantName = 'Not Available'


            phoneNumberExist = targetItems.find('p', class_ = 'phone-primary hidden-xs')
            if phoneNumberExist != None:
                number = phoneNumberExist.text.strip()

                if number == '':
                    number = 'Not Available'
                else:
                    pass
            else:
                number = 'Not Available'


            longitudeExist = targetItems.find('meta', itemprop = 'longitude')
            if longitudeExist != None:
                longitude = longitudeExist['content']
            else:
                longitude = 'Not Available'


            latitudeExist = targetItems.find('meta', itemprop = 'latitude')
            if latitudeExist != None:
                latitude = latitudeExist['content']
            else:
                latitude = 'Not Available'


            finalData = [{
                'Restaurant': restaurantName,
                'State': state,
                'City': city,
                'Zip-Code': zipCode,
                'Phone': number,
                'Address': f"{street} {city}, {state}, {zipCode}",
                'Longitude': longitude,
                'Latitude': latitude,
                'Source': pageLink,
            }]

            #print (finalData)
            
            count += 1
            
            print(f'Scraping Data from Link: {count}\n')

            df = pd.DataFrame(finalData)
            df.to_csv('US Restaurants Locations.csv', mode='a', index=False, header=False)
        
        else:
            
            sleep(45)
            
            print (f'{count} links scraped, waiting for 45 seconds...\n')

            count += 1

        

print ('Data Successfully Scraped!')