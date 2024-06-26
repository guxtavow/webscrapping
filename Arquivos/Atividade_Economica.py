import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import shutil
import time
import datetime
import sys

#Todos os dados tirados de http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/default.jsf
print()
print("Rodando webscrapping MEI do segmento: Atividade Econômica")

Ano = datetime.datetime.now().year
Nome_Pasta = Ano % 100
Nome_Pasta = str(Nome_Pasta)


def criar_pasta(origin, nome_pasta):
    mes = datetime.datetime.now().month
    mes_nomes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_Nome = mes_nomes[mes-2]
    while True:
        mesPassado = mes - 1 
        mesPassado = str(mesPassado).zfill(2)
        nova_pasta = f"{nome_pasta}-{mesPassado}"
        if not os.path.exists(os.path.join(origin, nova_pasta)):
            nova_pasta_caminho = os.path.join(origin, nova_pasta)
            os.makedirs(nova_pasta_caminho)
            return nova_pasta_caminho
        else:
            print()
            print(f"Os MEIS desse segmento, no mês de {mes_Nome}, já foram extraídos.")
            sys.exit()
           

extensao = ".csv"

def mover_arquivo():
    origem = r"Y:\Econômicas\MEI_Estatísticas\Brasil"
    destino = criar_pasta(origem,Nome_Pasta)
    
    os.listdir(destino)
    
    for nome_arquivo in os.listdir(origem):
        if nome_arquivo.endswith(extensao):
            caminho_origem = os.path.join(origem,nome_arquivo)
            caminho_destino = os.path.join(destino,nome_arquivo)
            shutil.move(caminho_origem, caminho_destino)
            print(f"Arquivo '{nome_arquivo} movido para {destino}.")
            print()
            

url = "http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf" #site do webscrapping

response = requests.get(url) 

if response.status_code == 200:  #se conseguir acessar o site (codigo igual a 200)
    opcoes_chrome = webdriver.ChromeOptions()   #definindo variavel de opções do chrome
    opcoes_chrome.add_argument('--headless') #fazer não aparecer a janela
    opcoes_chrome.add_argument('--disable-gpu')

    prefs = {   #preferencias das opções do chrome
        "profile.default_content_settings.popups": 0,
        "download.default_directory": r"Y:\Econômicas\MEI_Estatísticas\Brasil",
        "directory_upgrade": True
    }

    opcoes_chrome.add_experimental_option("prefs", prefs) #chamo as preferencias

    driver = webdriver.Chrome(options=opcoes_chrome) #inicio o webdriver
    driver.get(url)
    time.sleep(3) #3 segundos para pagina carregar e executar outras funções

    AE = driver.find_element(By.LINK_TEXT,'Atividade Econômica')#acho o elemento pelo link de texto
    AE.click()#clico nele
    time.sleep(3)

    exporta = driver.find_element(By.NAME, 'form:botaoExportarCsv')
    exporta.click()
    time.sleep(7)

    
    mover_arquivo()

    driver.quit() #Fecho a janela

else:
    print("Falha ao acessar a página:", response.status_code)
