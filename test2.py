import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Assign a user-agent to the header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

# Assign the base target website url
url = 'https://www.menuism.com/restaurant-locations'

# A reusable function to pull website raw HTML code
def getData(url):
    r = requests.get(url, headers=headers)
    soup = bs(r.text, 'lxml')
    return soup


# An empty list to hold all restaurant links
RestaurantLinks = []

# Create a list item containing all li elements with restaurant links in them
pageItems = getData(url).find('div', class_ = 'row columnized-list list-unstyled')

pageLinks = pageItems.find_all('li')

# Loop through all the elements collected above
for item in pageLinks:
    # Collect the URL of each restaurant
    Restaurants = {
        'Link': item.find('a')['href']
    }

    # Append the list for holding restaurant links with each restaurant link collected
    RestaurantLinks.append(Restaurants)

print (f' Scraping data from {len(RestaurantLinks)} restaurants\n')


RestaurantStatesLinks = []

for RestaurantLink in RestaurantLinks:

    stateSoup = getData(RestaurantLink['Link'])

    pageItems = stateSoup.find('ul', class_ = 'list-unstyled-links')

    pageLinks = pageItems.find_all('a')

    for pageLink in pageLinks:

        if 'us' in pageLink['title']:
            RestaurantStateLink= {
                'Link': pageLink['href']
            }
            #print (pageLink.text)
        
        else:
            pass

        RestaurantStatesLinks.append(RestaurantStateLink)


#print (len(RestaurantStatesLinks))

count = 0

RestaurantData = []

for RestaurantStateLink in RestaurantStatesLinks:

    citySoup = getData(RestaurantStateLink['Link'])

    pageItems = citySoup.find('ul', class_ = 'list-unstyled-links')

    pageLinks = pageItems.find_all('a')

    for pageLink in pageLinks:

        dataSoup = getData(pageLink['href'])

        targetItems = dataSoup.find('div', class_ = 'restaurant-card')

        streetExist = targetItems.find('span', itemprop = 'streetAddress')
        if streetExist != None:
            street = streetExist.text.strip()

            if street == '':
                street = 'Not Available'
            else:
                pass
        else:
            street = 'Not Available'


        cityExist = targetItems.find('span', itemprop = 'addressLocality')
        if cityExist != None:
            city = cityExist.text.strip()

            if city == '':
                city = 'Not Available'
            else:
                pass
        else:
            city = 'Not Available'
            

        stateExist = targetItems.find('span', itemprop = 'addressRegion')
        if stateExist != None:
            state = stateExist.text.strip()

            if state == '':
                state = 'Not Available'
            else:
                pass
        else:
            state = 'Not Available'
            

        zipCodeExist = targetItems.find('span', itemprop = 'postalCode')
        if zipCodeExist != None:
            zipCode = zipCodeExist.text.strip()

        else:
            zipCode = 'Not Available'
            

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


        finalData = {
            'Restaurant': restaurantName,
            'State': state,
            'City': city,
            'Zip-Code': zipCode,
            'Phone': number,
            'Address': f"{street} {city}, {state}, {zipCode}",
            'Longitude': longitude,
            'Latitude': latitude,
            'Source': pageLink['href'],
        }

        print (finalData)
        
        count += 1
        
        print(f'Scraped Data from Link: {count}\n')

        RestaurantData.append(finalData)