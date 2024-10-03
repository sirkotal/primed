import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_pharmaceutical_companies"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

divs = soup.find_all('div', class_='div-col')

data = []

for div in divs:
    for item in div.find_all('li'):
        link = item.find('a')
        
        if link and '(' in item.text and ')' in item.text:
            company_name = link.text
            year_text = item.text.split('(')[-1].replace(')', '').strip()
            data.append([company_name, year_text])

df = pd.DataFrame(data, columns=['Company Name', 'Year'])

df.to_csv('./dataset/Pharmaceutical_companies.csv', index=False)
