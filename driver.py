from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import logging

class Navegador:

    def iniciar(self):
        opcoes = Options()
        opcoes.add_argument('--start-maximized')
        servico = Service(ChromeDriverManager().install().replace(r'/THIRD_PARTY_NOTICES.chromedriver', r'\chromedriver.exe'))
        logging.info("Inicializando navegador.")
        return webdriver.Chrome(service=servico, options=opcoes)

    def aguardar_elemento(self, driver, tipo, locador, timeout=40):
        logging.info(f"Aguardando elemento: {tipo} - {locador}")
        for _ in range(timeout):
            try:
                if tipo == 'id':
                    return driver.find_element(By.ID, locador)
                elif tipo == 'xpath':
                    return driver.find_element(By.XPATH, locador)
                elif tipo == 'name':
                    return driver.find_element(By.NAME, locador)
                elif tipo == 'class_name':
                    return driver.find_element(By.CLASS_NAME, locador)
                elif tipo == 'tag_name':
                    return driver.find_element(By.TAG_NAME, locador)
                elif tipo == 'css_selector':
                    return driver.find_element(By.CSS_SELECTOR, locador)
                elif tipo == 'link_text':
                    return driver.find_element(By.LINK_TEXT, locador)
                elif tipo == 'partial_link_text':
                    return driver.find_element(By.PARTIAL_LINK_TEXT, locador)
                elif tipo == 'js':
                    return driver.execute_script(locador)
            except Exception:
                sleep(1)
        raise TimeoutError(f"[ERRO] Elemento {locador} ({tipo}) não encontrado após {timeout} segundos.")
