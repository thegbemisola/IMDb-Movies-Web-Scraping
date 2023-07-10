# Importing Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import requests
from bs4 import BeautifulSoup


#Making a list of the urls since they are split into 5 pages
urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating',
       'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt',
       'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=101&ref_=adv_nxt',
       'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=151&ref_=adv_nxt',
       'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=201&ref_=adv_nxt']


# Making a list to store the scrapped information
df_list = []

# Looping through each url
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_data = soup.find_all('div', class_= 'lister-item-content')

    #looping through each movie description
    for movie in movie_data:
        movie_name = movie.h3.a.text
        year = movie.h3.find('span', class_ ="lister-item-year text-muted unbold").text.replace('(', '').replace(')', '').replace('I', '')
        runtime = movie.p.find('span', class_ ="runtime").text.replace(' min', '')
        genre = movie.p.find('span',  class_ ="genre").text.strip()
        rating = movie.find('strong').text
        metascore = movie.find('span',  class_ ="metascore").text.strip() if movie.find('span', class_ = 'metascore') else''
        values = movie.find_all('span',  attrs = {'name':"nv"} )
        votes = values[0].text.replace(',', '')
        gross = values[1].text.replace('$', '').replace('M', '') if len(values) >  2 else ''
        rank = values[1].text.replace('#', '') if len(values) == 2 else values[2].text.replace('#', '')

         #Append to list of dictionaries
        df_list.append({'movie_name': movie_name,
                            'year': year,
                       'runtime(min)': runtime,
                       'genre': genre,
                       'rating': rating,
                       'metascore': metascore,
                       'votes': votes,
                       'gross($)(M)': gross, 
                       'rank': rank})
    df = pd.DataFrame(df_list, columns = ['movie_name', 'year', 'runtime(min)', 'genre', 'rating', 
                                          'metascore', 'votes', 'gross($)(M)', 'rank'])



# Save data to excel file
df.to_excel("IMDb Movies.xlsx", index=False)

