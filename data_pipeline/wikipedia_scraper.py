import requests
from bs4 import BeautifulSoup
import soupsieve as sv
import pandas as pd
import re
from html import unescape
from unidecode import unidecode


def get_first_sentence(company_url):
    try:
        company_response = requests.get(company_url)
        company_soup = BeautifulSoup(company_response.text, 'html.parser')
        
        paragraphs = company_soup.find_all('p')
        paragraphs = sv.filter(':not(table.infobox p)', paragraphs) # we don't want data from the table on the right side
        
        for paragraph in paragraphs:
            span = paragraph.find('span', class_="geo-inline-hidden noexcerpt")
            is_empty = len(paragraph.get_text()) <= 1
            if not span and not is_empty:
                return paragraph.get_text(strip=True)

    except Exception as e:
        print(f"Erro ao buscar dados de {company_url}: {e}")
        return ""

def get_companies():
    url = "https://en.wikipedia.org/wiki/List_of_pharmaceutical_companies"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all('div', class_='div-col')

    data = []

    for div in divs:
        for item in div.find_all('li'):
            link = item.find('a')
            
            if link and '(' in item.text and ')' in item.text:
                company_name = unidecode(unescape(link.text))
                year_text = re.sub(r'[a-zA-Z]', '', item.text).split('(')[-1].replace('.', ';').replace(':', ';').replace(',', ';').split(';')[-1].replace('–', '-').replace(')', '').replace(' ', '')
                year_text_unidecoded = unidecode(unescape(year_text))
                
                company_url = "https://en.wikipedia.org" + link['href']
                
                first_sentence = get_first_sentence(company_url)
                first_sentence_unidecoded = unidecode(unescape(first_sentence))
                
                data.append([company_name, year_text_unidecoded, first_sentence_unidecoded])

    df = pd.DataFrame(data, columns=['Company Name', 'Year', 'Description'])

    df.to_csv('dataset/pharmaceutical_companies.csv', index=False)

    print("Successfully wrote data to pharmaceutical_companies.csv")


def get_diseases():
    url = "https://en.wikipedia.org/wiki/List_of_autoimmune_diseases"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table', class_='wikitable')

    data = []

    for table in tables[0:len(tables)-2]:
        for item in table.find_all('tr'):
            lines = []
            for line in item.find_all('td'):
                lines.append(unidecode(unescape(line.text.strip())))
                
            if 4 <= len(lines) <= 6:
                data.append([lines[0], lines[1], lines[2], lines[3], lines[4]])

    df = pd.DataFrame(data, columns=['Disease', 'Primary organ/body part affected', 'Autoantibodies', 'Acceptance as an autoimmune disease', 'Prevalence rate (US)'])

    df.to_csv('dataset/diseases.csv', index=False)

    print("Successfully wrote data to diseases.csv")

# get_companies()
# get_diseases()
