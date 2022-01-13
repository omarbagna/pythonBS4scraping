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

print (f'{len(RestaurantLinks)} Restaurants\n')

print (f'Performing Step One .... \n')

RestaurantStatesLinks = []

for RestaurantLink in RestaurantLinks:

    stateSoup = getData(RestaurantLink['Link'])

    pageItems = stateSoup.find('ul', class_ = 'list-unstyled-links')

    pageLinks = pageItems.find_all('a')

    for pageLink in pageLinks:


        if pageLink['title'][-2:] == 'us':

            #print (pageLink['title'])

            RestaurantStateLink= {
                'Link': pageLink['href']
            }
            #print (pageLink.text)
        
        else:
            pass

        RestaurantStatesLinks.append(RestaurantStateLink)



print (f'Step One Completed Successfully ...')

print (f'Performing Step Two .... \n')

linksScraped = pd.read_csv('LinksCount.csv')['Link'].to_list()

print(f'{len(linksScraped)} Links Already Collected\n')

count = len(linksScraped)

checked = 0

RestaurantCitiesLinks = []

for RestaurantStateLink in RestaurantStatesLinks:

    
        
    citySoup = getData(RestaurantStateLink['Link'])

    pageItems = citySoup.find('ul', class_ = 'list-unstyled-links')

    pageLinks = pageItems.find_all('a')

    for pageLink in pageLinks:

        linksScraped = pd.read_csv('LinksCount.csv')['Link'].to_list()

        if pageLink['href'] in linksScraped:

            checked += 1

            print(f'{checked} Links Scraped Passing...')

        else:

            print('Continuing Data Scrape from link:')

            RestaurantCityLink= [{
                'Link': pageLink['href']
            }]

            df = pd.DataFrame(RestaurantCityLink)
            df.to_csv('LinksCount.csv', mode='a', index=False, header=False)

            count += 1

            print (count)
            
            RestaurantCitiesLinks.append(RestaurantCityLink)
            

df = pd.DataFrame(RestaurantCitiesLinks)
df.to_csv('Restaurant Cities Links.csv', index=False)

print (f'Step Two Completed Successfully ...')

print (len(RestaurantCitiesLinks))