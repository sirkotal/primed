import requests
from bs4 import BeautifulSoup
import pandas as pd
#from googletrans import Translator

base_url = "https://www.cuf.pt/saude-a-z"
headers = {"User-Agent": "Mozilla/5.0"}
doencas_data = []

#def translate_text(text):
#    """Traduz o texto para o idioma desejado (padrão: inglês)."""
#    translator = Translator()
#    translation = translator.translate(text=text, src='auto', dest='en')
#    return translation.text

def get_doencas_list(page_content):
    """Extrai os links para as páginas de cada doença a partir do HTML."""
    soup = BeautifulSoup(page_content, 'html.parser')
    
    doencas_links = []
    for a_tag in soup.select(".field-content a"):
        link = a_tag.get("href")
        if link:
            doencas_links.append("https://www.cuf.pt" + link)
    
    return doencas_links

def get_detalhes_completo(doenca_url):
    """Extrai o conteúdo completo da página de doença, formatando títulos e textos."""
    response = requests.get(doenca_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    detalhes = ""
    current_section = None

    for tag in soup.find_all(["h2", "p", "li"]):
        if tag.name == "h2" and tag.get_text(strip=True) != "Consultas":
            current_section = tag.get_text(strip=True)
            detalhes += f"//{current_section}// "
        elif tag.name == "p" and current_section:
            detalhes += tag.get_text(strip=True) + " "
        elif tag.name == "li" and current_section:
            detalhes += tag.get_text(strip=True) + ";/ "
        elif tag.name == "h2" and tag.get_text(strip=True) == "Consultas":
            break

    return detalhes.strip().replace(" ,", "")

page = 0
has_next_page = True
while has_next_page:
    response = requests.get(base_url, headers=headers, params={"page": page})
    if response.status_code != 200:
        print("Erro ao carregar a página:", response.status_code)
        break

    print(f"Scraping page {page}")
    page_content = response.text
    
    doencas_links = get_doencas_list(page_content)
    
    if not doencas_links:
        has_next_page = False
    else:
        for doenca_url in doencas_links:
            print(f"Scraping disease: {doenca_url}")
            detalhes_completo = get_detalhes_completo(doenca_url)
            
            doenca_nome = doenca_url.split("/")[-1].replace("-", " ").capitalize()
            
            doencas_data.append({
                "Doença": doenca_nome,
                "Detalhes": detalhes_completo
            })
        
        page += 1

df = pd.DataFrame(doencas_data)
df.to_csv("./dataset/sources/cuf_sicknesses.csv", index=False, encoding="utf-8")
print("Scraping concluído e dados salvos em doencas_cuf.csv")
