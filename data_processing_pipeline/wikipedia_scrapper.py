import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode

url = "https://en.wikipedia.org/wiki/List_of_pharmaceutical_companies"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

divs = soup.find_all('div', class_='div-col')

data = []

def get_first_sentence(company_url):
    try:
        company_response = requests.get(company_url)
        company_soup = BeautifulSoup(company_response.text, 'html.parser')
        
        first_paragraph = company_soup.find('p')
        if first_paragraph:
            return first_paragraph.text.strip()  # Retornar o texto do parágrafo, sem espaços extras
        else:
            return ""
    except Exception as e:
        print(f"Erro ao buscar dados de {company_url}: {e}")
        return ""

for div in divs:
    for item in div.find_all('li'):
        link = item.find('a')
        
        if link and '(' in item.text and ')' in item.text:
            company_name = link.text
            year_text = re.sub(r'[a-zA-Z]', '', item.text).split('(')[-1].replace('.', ';').replace(':', ';').replace(',', ';').split(';')[-1].replace('–', '-').replace(')', '').replace(' ', '')
            year_text_unidecoded = unidecode(year_text)
            print(year_text_unidecoded)
            
            company_url = "https://en.wikipedia.org" + link['href']
            
            first_sentence = get_first_sentence(company_url)
            first_sentence_unidecoded = unidecode(first_sentence)
            
            data.append([company_name, year_text_unidecoded, first_sentence_unidecoded])

df = pd.DataFrame(data, columns=['Company Name', 'Year', 'Description'])

df.to_csv('./dataset/Pharmaceutical_companies.csv', index=False)

print("CSV criado com sucesso!")
