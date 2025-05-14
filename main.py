from driver import Navegador
from scrapping_cotacoes import ScrappingCotacoes
from log_config import configurar_logger
import traceback
import logging

URL = "https://www.bcb.gov.br/conversao"

def main():
    configurar_logger()
    try:
        navegador = Navegador()
        driver = navegador.iniciar()

        cotador = ScrappingCotacoes(driver, navegador)
        moedas = cotador.ler_input("input.txt")
        cotador.acessar_site(URL)
        cotador.configurar_valor_base()
        cotador.obter_cotacoes(moedas)
        cotador.gerar_planilhas()

    except Exception as e:
        logging.error("Erro geral na execução.")
        logging.error(traceback.format_exc())
    finally:
        logging.info("Execução finalizada.")

if __name__ == "__main__":
    main()
