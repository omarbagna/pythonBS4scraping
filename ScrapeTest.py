from bs4 import BeautifulSoup
import requests
import xlsxwriter



#collect html file content from website
html_text = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm').text

#activate beautiful soup to filter the data to be readable
soup = BeautifulSoup(html_text, 'lxml')

#target the area where the desired data is located
menu = soup.find('tbody', class_='lister-list')

#pull all rows containing the desired data
rows = menu.find_all('tr')

#create empty distionaries to hold the scraped data
movies = []
releaseYears = []
viewerRatings = []

row = 1
col = 0


#loop through all rows
for row in rows:
    #target the title column
    titles = row.find_all('td', class_='titleColumn')
    
    #loop through all titles
    for title in titles:
        #pull the movie name from the title column
        name = title.find('a').text

        #pull the movie year from the title column
        year = title.find('span', class_='secondaryInfo').text.strip("()")
        
        #add the movie name to the movie dictionary
        movies.append(name)

        #add the movie year to the releaseYear dictionary
        releaseYears.append(year)
        
    #pull all the data in the ratings column
    ratings = row.find_all('td', class_='ratingColumn imdbRating')
    
    #loop through the ratings data
    for rating in ratings:
       
       #check if there is a rating
       if rating.find('strong') not in rating:
           #if there is no rating in the column
           rate = "No rating"
       else:
           #if there is a rating in the column
           rate = rating.find('strong').text

        #add the rating to the viewerRating dictionary
       viewerRatings.append(rate)



# Create an new Excel file and add a worksheet.
with xlsxwriter.Workbook('IMDB Scraped Data.xlsx') as workbook:
    # Add worksheet
    worksheet = workbook.add_worksheet()

    # Write headers
    worksheet.write(0, 0, 'Movie Title')
    worksheet.write(0, 1, 'Year')
    worksheet.write(0, 2, 'Rating')

    # Write movie title data to excel file
    for i, (movie) in enumerate(movies, start=1):
        worksheet.write(i, 0, movie)

    # Write movie year data to excel file
    for i, (releaseYear) in enumerate(releaseYears, start=1):
        worksheet.write(i, 1, releaseYear)

    # Write movie rating data to excel file
    for i, (viewerRating) in enumerate(viewerRatings, start=1):
        worksheet.write(i, 2, viewerRating)