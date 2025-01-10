from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import math
navegador = webdriver.Chrome()
acoes = ActionChains(navegador)

login = '12801230600'

senha = '123456'

planilha_convercao = 'dados_convercao.xlsx'

planilha_dados = 'dados_sisreg.xlsx'

colunas_convercao = ['cod_unico_sisreg','cod_interno_sisreg','cod_procedimento','cod_CBO','esp_CBO']

colunas_dados_sisreg = ['Cod. Unificado', 'Cod. Interno', 'PPI Total', 'PPI Usada', 'PPI Saldo']

df = pd.read_excel(planilha_convercao, dtype={coluna: str for coluna in colunas_convercao})

dados_insercao = pd.read_excel(planilha_dados, dtype={coluna: str for coluna in colunas_dados_sisreg})

navegador.get('https://juizdefora-mg.vivver.com/ram/ppi/definicao_pactuacao')
time.sleep(2)

login = navegador.find_element(By.XPATH, '//*[@id="conta"]').send_keys(login)
senha = navegador.find_element(By.XPATH, '//*[@id="password"]').send_keys(senha)
botao_login = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[2]').click()

while len(navegador.find_elements(By.XPATH,'//*[@id="lookup_key_ppi_definicao_pactuacao_ram_lista_municipio_sede_id"]')) < 1:
    time.sleep(1)

def inserir_dados_padroes():
    municipio_sede = navegador.find_element(By.XPATH, '//*[@id="lookup_key_ppi_definicao_pactuacao_ram_lista_municipio_sede_id"]').send_keys('2')

    ano = navegador.find_element(By.XPATH, '//*[@id="ppi_definicao_pactuacao_ano"]').send_keys('2025')

    mes = navegador.find_element(By.XPATH, '//*[@id="div_dados_pactuacao"]/div[9]/div[3]/div/span/span[1]/span/span[2]/b').click()

    mes_input = navegador.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys('janeiro')

    acoes.send_keys(Keys.ENTER).perform()

def inserir_dados_variaveis(cod_interno_sisreg):
    procedimento_filtrado = df.loc[df['cod_interno_sisreg'] == cod_interno_sisreg].values.flatten()

    print(procedimento_filtrado)

    procedimento = procedimento_filtrado[2]

    cbo = procedimento_filtrado[3]

    especialidade_cbo = procedimento_filtrado[4]

    camp_procedimento = navegador.find_element(By.XPATH, '//*[@id="lookup_key_ppi_definicao_pactuacao_adm_procedimento_id"]').send_keys(procedimento)

    time.sleep(0.3)

    camp_cbo = navegador.find_element(By.XPATH, '//*[@id="lookup_key_ppi_definicao_pactuacao_adm_especialidade_id"]').send_keys(cbo)

    time.sleep(0.3)

    if math.isnan(especialidade_cbo) == False:
        camp_especialidade_cbo = navegador.find_element(By.XPATH, '//*[@id="lookup_key_ppi_definicao_pactuacao_cbo_especialidade_id"]').send_keys(especialidade_cbo)

        time.sleep(0.3)
    
for i, row in dados_insercao.iterrows():
    codigo_intern_sisreg = row['Cod. Interno']

    quantidade = row['PPI Total']

    municipio = row['Municipio']

    inserir_dados_padroes()

    inserir_dados_variaveis(codigo_intern_sisreg)

    campo_quantidade = navegador.find_element(By.XPATH, '//*[@id="ppi_definicao_pactuacao_quantidade_pactuada"]').send_keys(quantidade)

    selc_municipio = navegador.find_element(By.XPATH, '//*[@id="select2-lookup_name_ppi_definicao_pactuacao_ram_lista_municipio_referencia_id-container"]').click()

    time.sleep(0.3)

    campo_municipio = navegador.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(municipio)

    time.sleep(1)

    button_pesquisar = navegador.find_element(By.XPATH, '//*[@id="btn_pesquisar"]').click()

    time.sleep(1)

    ppi = navegador.find_element(By.XPATH, '//*[@id="table_grid"]/tbody/tr/td[3]')
    
    time.sleep(1)

    acoes.double_click(ppi).perform()

    time.sleep(2)

    replicar = navegador.find_element(By.XPATH, '//*[@id="btn_replicar"]').click()

    time.sleep(1)

    ano_final = navegador.find_element(By.XPATH, '//*[@id="ppi_definicao_pactuacao_replica_ano"]').send_keys('2025')

    select_mes_final=navegador.find_element(By.XPATH, '//*[@id="select2-ppi_definicao_pactuacao_replica_mes-container"]').click()

    time.sleep(0.3)

    select_element = navegador.find_element(By.ID, "ppi_definicao_pactuacao_replica_mes")

    select = Select(select_element)
  
    select.select_by_value('12')

    time.sleep(10000)