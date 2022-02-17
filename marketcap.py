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

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)
driver.maximize_window()
driver.get("https://web.whatsapp.com/")

while len(driver.find_elements_by_id('side')) < 1:
    sleep(1)

driver.find_element_by_xpath('<div title="Search input textbox" role="textbox" class="_13NKt copyable-text selectable-text" contenteditable="true" data-tab="3" dir="ltr"></div>').click()
driver.find_element_by_xpath('<div title="Search input textbox" role="textbox" class="_13NKt copyable-text selectable-text" contenteditable="true" data-tab="3" dir="ltr"></div>').send_keys('Space T.I')
driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]').click()
driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]').click()


valor_antigo_spe = 0
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

        if porcetagem > 11:
            print(f'''
            *O SPE CAIU {porcetagem}%*
            SPG: R$ {spg:,.2f}
            SPE: R$ {spe:,.2f}
            ''')
        else:
            print(f'''
            SPG: R$ {spg:,.2f}
            SPE: R$ {spe:,.2f}
            ''')

    elif spe > valor_antigo_spe:
        calculo =  spe - valor_antigo_spe
        porcetagem = int((calculo / spe) * 100)

        if porcetagem > 11:
            print(f'''
            *O SPE SUBIU {porcetagem}%*
            SPG: R$ {spg:,.2f}
            SPE: R$ {spe:,.2f}
            ''')

        else:
            print(f'''
            SPG: R$ {spg:,.2f}
            SPE: R$ {spe:,.2f}
            ''')

        
    valor_antigo_spe = spe
    sleep(180)




# print(f'SPG: R$ {spg:,.2f}')
# print(f'SPE: R$ {spe:,.2f}')