import requests
import random

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from database.db import cria_tabelas, novo_anuncio

BASE_URL = 'https://www.wimoveis.com.br/aluguel/apartamentos/df/brasilia/sudoeste'

def get_soup(url):
    ua = UserAgent()
    user_agent = ua.random
    print("\n*******************************************")
    print(f"Buscando URL: {url}")
    print(f"User agent: {user_agent}")
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("disable-gpu");

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    return BeautifulSoup(driver.page_source, "lxml")


def get_ultima_pagina(paginas):
    ultima_pagina = 0
    for pagina in paginas:
        try:
            p = int(pagina.get_text())
            if p > ultima_pagina:
                ultima_pagina = p
        except:
            pass
            
    return ultima_pagina


def get_anuncios(soup, pagina):
    anuncios = soup.find_all('div', class_=lambda value: value and value.startswith('CardContainer-sc-'))
    anuncios_encontrados = len(anuncios)
    print(f"{anuncios_encontrados} anuncios encontrados na pagina {pagina}.")

    lista_anuncios = []
    if anuncios_encontrados > 0:
        for anuncio in anuncios:
            div_principal = anuncio.find('div', class_=lambda value: value and value.startswith('PostingCardLayout-sc-'))
            preco = anuncio.find('div', class_=lambda value: value and value.startswith('Price-'))
            custos = anuncio.find('div', class_=lambda value: value and value.startswith('Expenses-'))
            endereco = anuncio.find('div', class_=lambda value: value and value.startswith('LocationAddress-'))
            caracteristicas = anuncio.find('h3', class_=lambda value: value and value.startswith('PostingMainFeaturesBlock-'))
            lista_caracteristicas = []
            for c in  caracteristicas.find_all('span'):
                lista_caracteristicas.append(c.text)

            img = anuncio.find_all('img')
            imagem = "sem imagem"
            descricao = "sem descricao"
            if img:
                imagem = img[0].get('src')
                descricao = img[0].get('alt')


            obj = {
                'id': div_principal.get('data-id'),
                'descricao': descricao,
                'url': 'https://www.wimoveis.com.br' + div_principal.get('data-to-posting'),
                'endereco': endereco.text,
                'preco': preco.text,
                'custos': custos.text,
                'imagem': imagem,
                'caracteristicas': ' | '.join(lista_caracteristicas)
            }

            lista_anuncios.append(obj)

    return lista_anuncios


if __name__ == "__main__":
    cria_tabelas()
    novo_anuncio()

    exit()
    soup = get_soup(BASE_URL)

    paginas = soup.find_all('a', class_=lambda value: value and value.startswith('PageItem-sc-'))
    ultima_pagina = get_ultima_pagina(paginas)

    lista = []
    lista = lista + get_anuncios(soup, 1) # busca os anuncios da primeira pagina
    """
    for _ in range(1, ultima_pagina):
        p = _ + 1
        next_url = f"{BASE_URL}/pagina-{p}"
        soup = get_soup(next_url)
        sleep(random.randint(2, 10))
        lista = lista + get_anuncios(soup, p)

    """
    print(len(lista))
    print("")
    print(lista[0])

    print("* Script Finalizado *")