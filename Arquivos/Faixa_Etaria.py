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
print("Rodando webscrapping MEI do segmento: Faixa Etária Brasil/UF/Município")
print()

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

    origem = r"Y:\Econômicas\MEI_Estatísticas\Faixa Etária São Paulo"
    destino = criar_pasta(origem,Nome_Pasta)
    
    os.listdir(destino)

    for nome_arquivo in os.listdir(origem):
        if nome_arquivo.endswith(extensao):
            caminho_origem = os.path.join(origem,nome_arquivo)
            caminho_destino = os.path.join(destino,nome_arquivo)
            shutil.move(caminho_origem, caminho_destino)
            print(f"Arquivo '{nome_arquivo} movido para {destino}.")
            print()

url = "http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf" 

response = requests.get(url) 

if response.status_code == 200:
    opcoes_chrome = webdriver.ChromeOptions()
    opcoes_chrome.add_argument('--headless')
    opcoes_chrome.add_argument('--disable-gpu')

    prefs = {  
        "profile.default_content_settings.popups": 0,
        "download.default_directory": r"Y:\Econômicas\MEI_Estatísticas\Faixa Etária São Paulo",
        "directory_upgrade": True
    }

    opcoes_chrome.add_experimental_option("prefs", prefs) 

    driver = webdriver.Chrome(options=opcoes_chrome) 
    driver.get(url)
    time.sleep(3) #3 segundos para pagina carregar e executar outras funções

    Mun = driver.find_element(By.LINK_TEXT,'Faixa Etária Brasil/UF/Município')#acho o elemento pelo link de texto
    Mun.click()#clico nele
    
    selecao_elemento = driver.find_element(By.NAME, 'form:uf') 
    Selecionado = Select(selecao_elemento) 
    Selecionado.select_by_value('SP')#seleciono a opção/variavel de valor 'SP'
    time.sleep(8)

    consulta = driver.find_element(By.NAME,'form:botaoConsultar')
    consulta.click()
    time.sleep(8) 

    exporta = driver.find_element(By.NAME, 'form:botaoExportarCsv')
    exporta.click()
    time.sleep(4)
    
    mover_arquivo()

    driver.quit() #Fecho a janela

else:
    print("Falha ao acessar a página:", response.status_code)
