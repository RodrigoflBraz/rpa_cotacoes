import pandas as pd
from datetime import datetime
import re
import time
import logging
import os 
from selenium.webdriver.common.by import By

class ScrappingCotacoes:

    def __init__(self, driver, navegador):
        self.driver = driver
        self.navegador = navegador
        self.dict_cotacoes = {}

    def ler_input(self, caminho_arquivo):
        logging.info("Lendo arquivo de input.")
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo]

    def acessar_site(self, url):
        logging.info(f"Acessando site: {url}")
        self.driver.get(url)
        try:
            botao_cookie = self.navegador.aguardar_elemento(self.driver, 'xpath', r"/html/body/app-root/bcb-cookies/div/div/div/div/button[2]")
            botao_cookie.click()
        except Exception as e:
            logging.warning("Cookie já aceito ou botão não encontrado.")

    def configurar_valor_base(self):
        logging.info("Configurando BRL como moeda base.")
        campo = self.navegador.aguardar_elemento(self.driver, 'xpath', r"/html/body/app-root/app-root/div/div/main/dynamic-comp/div/div[1]/bcb-detalhesconversor/div/div[1]/form/div[2]/div[1]/div/input")
        campo.clear()
        campo.send_keys("1,00")

        self.navegador.aguardar_elemento(self.driver, 'xpath', '//*[@id="button-converter-de"]').click()
        lista = self.navegador.aguardar_elemento(self.driver, 'xpath', '//*[@id="moedaBRL"]')
        for li in lista.find_elements(By.TAG_NAME, 'li'):
            if '(BRL)' in li.text:
                li.click()
                break

    def obter_cotacoes(self, moedas):
        for moeda in moedas:
            logging.info(f"Consultando cotação para: {moeda}")
            try:
                self.navegador.aguardar_elemento(self.driver, 'xpath', '//*[@id="button-converter-para"]').click()
                lista = self.navegador.aguardar_elemento(self.driver, 'xpath', '//*[@id="moedaResultado1"]')
                li_moedas = lista.find_elements(By.TAG_NAME, 'li')

                encontrada = False
                for li in li_moedas:
                    if f'({moeda})' in li.text:
                        li.click()
                        self.navegador.aguardar_elemento(self.driver, 'id', 'button-converter-para').click()
                        time.sleep(2)
                        resultado = self.navegador.aguardar_elemento(self.driver, 'class_name', 'card-body')
                        self.dict_cotacoes[moeda] = resultado.text
                        encontrada = True
                        break

                if not encontrada:
                    self.dict_cotacoes[moeda] = "Cotação da moeda não encontrada."
            except Exception as e:
                logging.error(f"Erro ao buscar cotação de {moeda}: {str(e)}")
                self.dict_cotacoes[moeda] = "Erro na consulta."

    def gerar_planilhas(self):
        hoje = datetime.today().strftime('%d/%m/%Y')
        dict_validos = {}

        for moeda, texto in self.dict_cotacoes.items():
            match = re.search(r"Resultado da conversão:\s*([\d,]+)", texto)
            if match:
                valor = float(match.group(1).replace(",", "."))
                dict_validos[moeda] = round(valor, 3)

        df_valido = pd.DataFrame(list(dict_validos.items()), columns=["Moeda saída", "Valor cotação"])
        df_valido[['Moeda entrada', 'Taxa', 'Data']] = ['BRL', 1, hoje]
        df_valido = df_valido[['Moeda entrada', 'Taxa', 'Moeda saída', 'Valor cotação', 'Data']]
        df_valido.to_excel(os.path.join("output", "cotacoes.xlsx"), index=False)
        logging.info("Arquivo 'cotacoes.xlsx' salvo.")

        df_total = pd.DataFrame(list(self.dict_cotacoes.items()), columns=["Moeda saída", "Valor cotação"])
        df_total[['Moeda entrada', 'Taxa', 'Data']] = ['BRL', 1, hoje]
        df_total = df_total[['Moeda entrada', 'Taxa', 'Moeda saída', 'Valor cotação', 'Data']]
        df_total['Status'] = df_total['Valor cotação'].map(lambda x: 'Consulta Ok' if isinstance(x, str) and "Resultado" in x else 'Erro ou não encontrada')
        df_total.to_excel(os.path.join("output", "resultado_processamento.xlsx"), index=False)
        logging.info("Arquivo 'resultado_processamento.xlsx' salvo.")


