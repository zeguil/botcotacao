from requests import Request, Session
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

parametros_spg = {
    'symbol': 'SPG',
    'convert': 'BRL'
}
parametros_spe = {
    'symbol': 'SPE',
    'convert': 'BRL'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'f24c5c79-59f8-4868-8a2a-0906526d062d' 
}


def buscar_grupo(grupo):
    campo_pesquisa = driver.find_element_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    sleep(2)
    campo_pesquisa.click()
    campo_pesquisa.send_keys(grupo)
    campo_pesquisa.send_keys(Keys.ENTER)

def enviar_mensagem(mensagem):
    campo_mensagem = driver.find_elements_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
    campo_mensagem[1].click()
    sleep(3)
    campo_mensagem[1].send_keys(mensagem)
    campo_mensagem[1].send_keys(Keys.ENTER)


driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.implicitly_wait(10)
driver.maximize_window()
driver.get("https://web.whatsapp.com/")

while len(driver.find_elements_by_id('side')) < 1:
    sleep(1)

buscar_grupo('Cotação')

valor_antigo_spe = 0
rodadas = 0
while True:
    sessao = Session()
    sessao.headers.update(headers)

    resposta_spg = sessao.get(url, params=parametros_spg)
    resposta_spe = sessao.get(url, params=parametros_spe)

    spg = json.loads(resposta_spg.text)['data']['SPG'][0]['quote']['BRL']['price']
    spe = json.loads(resposta_spe.text)['data']['SPE'][0]['quote']['BRL']['price']

    if spe < valor_antigo_spe:
        calculo = valor_antigo_spe - spe
        porcetagem = int((calculo / valor_antigo_spe) * 100)

        if porcetagem > 5:
            mensagem = (f'------------\n*O SPE CAIU {porcetagem}%*\n*SPG*: _R$ {spg:,.2f}_\n*SPE*: _R$ {spe:,.2f}_')
            enviar_mensagem(mensagem)
        else:
            mensagem = (f'\n------------\n*SPG*: _R$ {spg:,.2f}_\n*SPE*: _R$ {spe:,.2f}_')
            enviar_mensagem(mensagem)

    elif spe > valor_antigo_spe:
        calculo =  spe - valor_antigo_spe
        porcetagem = int((calculo / spe) * 100)

        if porcetagem > 5 and rodadas > 0:
            mensagem = (f'\n------------\n*O SPE SUBIU {porcetagem}%*\n*SPG*: _R$ {spg:,.2f}_\n*SPE*: _R$ {spe:,.2f}_')
            enviar_mensagem(mensagem)

        else:
            mensagem = (f'\n------------\n*SPG*: _R$ {spg:,.2f}_\n*SPE*: _R$ {spe:,.2f}_')
            enviar_mensagem(mensagem)

        
    valor_antigo_spe = spe
    sleep(300)
    rodadas += 1



