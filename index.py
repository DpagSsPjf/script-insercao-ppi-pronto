from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
navegador = webdriver.Chrome()

login = '12801230600'

senha = '123456'

planilha_convercao = 0

dados_convercao = 0

dados_insercao = 0

navegador.get('https://juizdefora-mg.vivver.com/ram/ppi/definicao_pactuacao')
time.sleep(2)

login = navegador.find_element(By.XPATH, '//*[@id="conta"]').send_keys(login)
senha = navegador.find_element(By.XPATH, '//*[@id="password"]').send_keys(senha)
botao_login = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[2]').click()

while len(navegador.find_elements(By.XPATH,'//*[@id="lookup_key_ppi_definicao_pactuacao_ram_lista_municipio_sede_id"]')) < 1:
    time.sleep(1)