import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import shutil
import time
import datetime


Ano = datetime.datetime.now().year
Nome_Pasta = Ano % 100
Nome_Pasta = str(Nome_Pasta)


def criar_pasta(origin, nome_pasta):
    count = 1
    new_pasta = f"{nome_pasta}-{count}"
    if not os.path.exists(new_pasta):
        nova_pasta = os.path.join(origin,new_pasta)
        os.makedirs(nova_pasta)
        return nova_pasta
    else:
        while True:
            nova_pasta = f"{nome_pasta}-{count}"
            if not os.path.exists(nova_pasta):
                os.makedirs(nova_pasta)
                return nova_pasta
            count += 1


extensao = ".csv"

def mover_arquivo():

    origem = r"C:\Users\e_gustavoaa\Documents\projetos\webscrapping\Atividade Economica\\"
    destino = criar_pasta(origem,Nome_Pasta)
    
    os.listdir(destino)
    
    for nome_arquivo in os.listdir(origem):
        if nome_arquivo.endswith(extensao):
            caminho_origem = os.path.join(origem,nome_arquivo)
            caminho_destino = os.path.join(destino,nome_arquivo)
            shutil.move(caminho_origem, caminho_destino)
            print(f"Arquivo '{nome_arquivo} movido para {destino}.")
            

url = "http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf" #site do webscrapping

response = requests.get(url) 

if response.status_code == 200:  #se conseguir acessar o site (codigo igual a 200)
    opcoes_chrome = webdriver.ChromeOptions()   #definindo variavel de opções do chrome

    prefs = {   #preferencias das opções do chrome
        "profile.default_content_settings.popups": 0,
        "download.default_directory": r"C:\Users\e_gustavoaa\Documents\projetos\webscrapping\Atividade Economica\\",
        "directory_upgrade": True
    }

    opcoes_chrome.add_experimental_option("prefs", prefs) #chamo as preferencias

    driver = webdriver.Chrome(options=opcoes_chrome) #inicio o webdriver
    driver.get(url)
    time.sleep(3) #3 segundos para pagina carregar e executar outras funções

    AE = driver.find_element(By.LINK_TEXT,'Atividade Econômica')#acho o elemento pelo link de texto
    AE.click()#clico nele

    exporta = driver.find_element(By.NAME, 'form:botaoExportarCsv')
    exporta.click()
    time.sleep(7)

    
    mover_arquivo()

    driver.quit() #Fecho a janela

else:
    print("Falha ao acessar a página:", response.status_code)