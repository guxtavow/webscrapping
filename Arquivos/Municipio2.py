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

print("Rodando webscrapping MEI do segmento: CNAE UF/Município/Sexo")

# ------------------------------ PARAMETROS PAI ------------------------------ #
Ano = datetime.datetime.now().year
Nome_Pasta = str(Ano % 100)
origem = r"Y:\Econômicas\MEI_Estatísticas\default"
destino_final = r"Y:\Econômicas\MEI_Estatísticas\Estado de São Paulo por Sexo"
municipios = r"Arquivos/municipios.json"
# ------------------------------ PARAMETROS PAI ------------------------------ #


# ---------------------------------- FUNÇÕES --------------------------------- #

# Função para identificar o município pelo ID
def Identificar_Municipio(arquivo, id):
    try:
        with open(arquivo, 'r') as file:
            dados = json.load(file)
        for item in dados:
            if item['id'] == id:
                return item['name']
    except FileNotFoundError:
        print('Erro: Arquivo não encontrado')
        sys.exit()

# Função para criar pasta
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
            print(f"Os MEIS desse segmento, no mês de {mes_Nome}, já foram extraídos.")
            sys.exit()

extensao = ".csv"

# Função para mover arquivo
def mover_arquivo():
    origem = r"Y:\Econômicas\MEI_Estatísticas\default"
    destino = criar_pasta(destino_final, Nome_Pasta)
    
    for nome_arquivo in os.listdir(origem):
        if nome_arquivo.endswith(extensao):
            caminho_origem = os.path.join(origem, nome_arquivo)
            caminho_destino = os.path.join(destino, nome_arquivo)
            shutil.move(caminho_origem, caminho_destino)
            print(f"Arquivo '{nome_arquivo}' movido para {destino}.")

# Função para carregar o progresso do último arquivo baixado (Caso seja interrompido no meio do processo)
def carregar_progresso(origem):
    arquivos_existentes = sorted([f for f in os.listdir(origem)])
    if arquivos_existentes:
        ultimo_arquivo = arquivos_existentes[-1]
        return ultimo_arquivo
    


# ---------------------------------- FUNÇÕES --------------------------------- #





# -------------------------- SELENIUM(Webscrapping) -------------------------- #

# Configurações do Selenium
url = "http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf" 
response = requests.get(url)

if response.status_code == 200:
    opcoes_chrome = webdriver.ChromeOptions()
    opcoes_chrome.add_argument('--headless')
    opcoes_chrome.add_argument('--disable-gpu')

    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": r"Y:\Econômicas\MEI_Estatísticas\default",
        "directory_upgrade": True
    }

    opcoes_chrome.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=opcoes_chrome)
    driver.get(url)
    time.sleep(3)

    Mun = driver.find_element(By.LINK_TEXT, 'CNAE UF/Município/Sexo')
    Mun.click()
    
    selecao_elemento = driver.find_element(By.NAME, 'form:uf')
    Selecionado = Select(selecao_elemento)
    Selecionado.select_by_value('SP')
    time.sleep(5)

    Wait = WebDriverWait(driver, 10)
    selecao_elemento2 = Wait.until(EC.presence_of_element_located((By.ID, 'form:municipioUF')))
    select = Select(selecao_elemento2)
    options = [option.get_attribute("value") for option in select.options]


    # Carregar progresso
    ultimo_municipio = carregar_progresso(origem)
    if ultimo_municipio:
        # Identificar o value do último município processado a partir do arquivo
        ultimo_value = None
        for item in json.load(open(municipios)):
            if item['name'] == ultimo_municipio:
                ultimo_value = item['id']
                break

        if ultimo_value and ultimo_value in options:
            start_index = options.index(ultimo_value) + 1
        else:
            start_index = 0
    else:
        start_index = 0

    # Iterar sobre cada valor de município
    for value in options[start_index:]:
        nome_arq = Identificar_Municipio(municipios, value)

        nome_arquivo_destino = os.path.join(origem, f"{nome_arq}.csv")
        if os.path.exists(nome_arquivo_destino):
            print(f"O arquivo para o município {nome_arq} já existe. Pulando para o próximo.")
            continue

        time.sleep(2)
        selecao_elemento2 = Wait.until(EC.presence_of_element_located((By.ID, 'form:municipioUF')))
        select = Select(selecao_elemento2)
        select.select_by_value(value)
        time.sleep(5)

        print(f'Consultando Municipio {nome_arq} com Codigo: {value}')

        consulta = Wait.until(EC.element_to_be_clickable((By.NAME, 'form:botaoConsultar')))
        consulta.click()
        time.sleep(8)

        print(f'Exportando...')
        exporta = Wait.until(EC.element_to_be_clickable((By.NAME, 'form:botaoExportarCsv')))
        exporta.click()

        print(f'Municipio {nome_arq} exportado!')

        nome_arquivo = 'relatorio_mei.csv'
        nome_novo = f'{nome_arq}.csv'

        arquivo_atual = os.path.join(origem, nome_arquivo)
        time.sleep(8)
        arquivo_novo = os.rename(arquivo_atual, os.path.join(origem, nome_novo))

    mover_arquivo()
    driver.quit()
    

else:
    print("Falha ao acessar a página:", response.status_code)

# -------------------------- SELENIUM(Webscrapping) -------------------------- #
