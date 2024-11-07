import requests
from bs4 import BeautifulSoup
import pandas as pd
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

base_url = "https://www.cuf.pt/saude-a-z"
headers = {"User-Agent": "Mozilla/5.0"}
output_dir = "./dataset/sources/cuf/"

def translate_text(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

def get_doencas_list(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    doencas_links = ["https://www.cuf.pt" + a.get("href") for a in soup.select(".field-content a") if a.get("href")]
    return doencas_links

def get_detalhes_completo(doenca_url):
    response = requests.get(doenca_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    detalhes = ""
    current_section = None

    for tag in soup.find_all(["h2", "p", "li"]):
        if tag.name == "h2" and tag.get_text(strip=True) != "Consultas":
            current_section = translate_text(tag.get_text(strip=True))
            detalhes += f"//{current_section}// "
        elif tag.name == "p" and current_section:
            detalhes += translate_text(tag.get_text(strip=True)) + " "
        elif tag.name == "li" and current_section:
            detalhes += translate_text(tag.get_text(strip=True)) + ";/ "
        elif tag.name == "h2" and tag.get_text(strip=True) == "Consultas":
            break

    return detalhes.strip().replace(" ,", "")

def process_page(page):
    response = requests.get(base_url, headers=headers, params={"page": page})
    if response.status_code != 200:
        print(f"Erro ao carregar a página {page}: {response.status_code}")
        return
    
    print(f"Scraping page {page}")
    page_content = response.text
    doencas_links = get_doencas_list(page_content)
    
    doencas_data = []
    for doenca_url in doencas_links:
        print(f"Scraping disease: {doenca_url}")
        detalhes_completo = get_detalhes_completo(doenca_url)
        
        doenca_nome = translate_text(doenca_url.split("/")[-1].replace("-", " ").capitalize())
        
        doencas_data.append({
            "Doença": doenca_nome,
            "Detalhes": detalhes_completo
        })
    
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"cuf_sicknesses_page_{page + 1}.csv")
    df = pd.DataFrame(doencas_data)
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Dados da página {page} salvos em {csv_path}")

page = 0
has_next_page = True
max_threads = 5

with ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = []
    while has_next_page:
        futures.append(executor.submit(process_page, page))
        page += 1
        
        response = requests.get(base_url, headers=headers, params={"page": page})
        has_next_page = response.status_code == 200 and bool(get_doencas_list(response.text))

    for future in as_completed(futures):
        future.result()

print("Scraping concluído e dados salvos em arquivos CSV individuais para cada página.")
