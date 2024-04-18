import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time



url = "http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf" #site do webscrapping

response = requests.get(url)

if response.status_code == 200:  #se conseguir acessar o site (codigo igual a 200)
    opcoes_chrome = webdriver.ChromeOptions()   #definindo variavel de opções do chrome

    prefs = {   #preferencias das opções do chrome
        "profile.default_content_settings.popups": 0,
        "download.default_directory": r"C:\Users\e_gustavoaa\Documents\projetos\webscrapping\\",
        "directory_upgrade": True
    }

    opcoes_chrome.add_experimental_option("prefs", prefs) #chamo as preferencias

    driver = webdriver.Chrome( options=opcoes_chrome) #inicio o webdriver
    driver.get(url)
    time.sleep(3) #3 segundos para pagina carregar e executar outras funções

    UF = driver.find_element(By.LINK_TEXT,'CNAE/UF')#acho o elemento pelo link de texto
    UF.click()#clico nele

    
    selecao_elemento = driver.find_element(By.NAME, 'form:uf') #DEFINO O ELEMENTO E QUAL INFO IREI PEGAR DESSA VARIAVEL
    Selecionado = Select(selecao_elemento) #ESSA VARIAVEL QUE IREI USAR

    Selecionado.select_by_value('SP')#seleciono a opção/variavel de valor 'SP'

    consulta = driver.find_element(By.NAME,'form:botaoConsultar')
    consulta.click()
    time.sleep(2)

    exporta = driver.find_element(By.NAME, 'form:botaoExportarCsv')
    exporta.click()
    time.sleep(7)

    driver.quit() #Fecho a janela

else:
    print("Falha ao acessar a página:", response.status_code)
