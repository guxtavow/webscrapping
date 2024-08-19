import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import shutil
import time
import datetime
import sys
#import pdb PARA DEBUGAR

#Todos os dados tirados de http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/default.jsf
print()
print("Rodando webscrapping MEI do segmento: CNAE UF/Município/Sexo")

Ano = datetime.datetime.now().year
Nome_Pasta = Ano % 100
Nome_Pasta = str(Nome_Pasta)

def Identificar_Municipio(arquivo, id): # DEF para identificação dos nomes dos municipios pelos ID's
    try:
        with open(arquivo, 'r') as file:
            dados = json.load(file) # abro e carro o json como arquivo
        for item in dados: # itero sobre todos os itens e depois identifico se o item tem um id
            if item['id'] == id:
                return item['name'] # se tiver, trazer o nome do municipio
    except FileNotFoundError:
        print('erro: Arquivo não encontrado')
        return sys.exit()


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
    origem = r"Y:\Econômicas\MEI_Estatísticas\Estado de São Paulo por Sexo\teste"
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
        "download.default_directory": r"Y:\Econômicas\MEI_Estatísticas\Estado de São Paulo por Sexo\teste",
        "directory_upgrade": True
    }

    opcoes_chrome.add_experimental_option("prefs", prefs) 

    driver = webdriver.Chrome(options=opcoes_chrome) 
    driver.get(url)
    time.sleep(3) # 3 segundos para pagina carregar e executar outras funçõe

    Mun = driver.find_element(By.LINK_TEXT,'CNAE UF/Município/Sexo') # acho o elemento pelo link de texto
    Mun.click() # clico nele
    
    selecao_elemento = driver.find_element(By.NAME, 'form:uf') 
    Selecionado = Select(selecao_elemento)
    Selecionado.select_by_value('SP') # seleciono a opção/variavel de valor 'SP'
    time.sleep(5)

    Wait = WebDriverWait(driver, 10) # varivel que permite eu alocar uma trava para aguardar o elemento reaparecer no campo de seleção para seleciona-lo
    selecao_elemento2 = Wait.until(EC.presence_of_element_located((By.ID, 'form:municipioUF')))
    select = Select(selecao_elemento2)
    options = [option.get_attribute("value") for option in select.options]

    # Iterar sobre cada valor de município
    for value in options:
        origem = r"Y:\Econômicas\MEI_Estatísticas\Estado de São Paulo por Sexo\teste" # origem da onde está alocado o arquivo default
        municipios = r"Arquivos\municipios.json" # origem da onde está o arquivo JSON
        nome_arq = Identificar_Municipio(municipios,value) # varivel da def

        time.sleep(2)
        # Obtenho novamente o select e depois seleciono a opção
        selecao_elemento2 = Wait.until(EC.presence_of_element_located((By.ID, 'form:municipioUF')))
        select = Select(selecao_elemento2)
        select.select_by_value(value)
        time.sleep(5)

        nome_arquivo_destino = os.path.join(origem, f"{nome_arq}.csv") # crio uma variavel onde aloco a junção do arquivo baixado e também o renomeio
        if os.path.exists(nome_arquivo_destino): # caso o arquivo já exista na pasta, eu pulo o seu value e vou para o proximo, passando por toda lista
            print(f"O arquivo para o município {nome_arq} já existe. Pulando para o próximo.")
            continue

        print()
        print(f'Consultando Municipio {nome_arq} com Codigo: {value}')
        print()


        # Clicar no botão Consultar
        consulta = Wait.until(EC.element_to_be_clickable((By.NAME, 'form:botaoConsultar'))) # aguardo até o elemento voltar a ser clicavel
        consulta.click()
        time.sleep(8)

        print(f'Exportando...')
        # Clicar no botão Exportar CSV
        exporta = Wait.until(EC.element_to_be_clickable((By.NAME, 'form:botaoExportarCsv')))
        exporta.click()

        print(f'Municipio {nome_arq} exportado!')

        nome_arquivo = 'relatorio_mei.csv'
        nome_novo = f'{nome_arq}.csv'

        arquivo_atual = os.path.join(origem, nome_arquivo) #caminho até o arquivo atual
        time.sleep(8)
        arquivo_novo = os.path.join(origem, nome_novo)#caminho onde sera alocado o arquivo com nome novo

        arquivo_final = os.rename(arquivo_atual,arquivo_novo) # arquivo final sendo renomeado com o nome do MUNICIPIO
                

    mover_arquivo()

    driver.quit() #Fecho a janela

else:
    print("Falha ao acessar a página:", response.status_code)
