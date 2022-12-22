import json
import sys
import time
import csv
from webbrowser import get
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import DBLoad
import Counters
import Printers
import concurrent.futures
import mysql.connector
import platform


# Abre o arquivo .env na pasta que possui as variáveis com os dados de conexão à base de dados
def get_env_variables():
    d = {}
    with open(".env", "r") as f:
        for line in f:
            (k, v) = line.split("=")
            v = v.split("\n")[0]
            d[k] = v
    return d['host'], d['user'], d['password'], d['port'], d['database']

# Inicia uma conexão com a base de dados e retorna o conector


def get_connection():
    host, user, password, port, database = get_env_variables()
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )


# Obtém o driver do browser, para uso com o Selenium
def get_driver():
    options = Options()
    options.headless = True
    executable = './geckodriver.exe' if platform == 'Windows' else './geckodriver'
    service = Service(executable_path=executable)
    # driver = webdriver.Firefox(service=service)
    driver = webdriver.Firefox(service=service, options=options)
    return driver

# Obtém o número de série da impressora


def get_sn(driver):
    return driver.find_element(By.ID, 'UsagePage.DeviceInformation.DeviceSerialNumber').text

# Obtem o total de impressões (contador) já realizadas pela impressora


def get_total_impressoes(driver):
    return driver.find_element(By.ID, 'UsagePage.ImpressionsByMediaSizeTable.Imprimir.TotalTotal').text.replace(',', '')

# Obtém o total de cópias (contador) já realizadas pela impressora


def get_total_copias(driver):
    return driver.find_element(By.ID, 'UsagePage.ImpressionsByMediaSizeTable.Copiar.TotalTotal').text.replace(',', '')

# Obtém o total de digitalizações realizadas pela impressora


def get_total_digitalizacoes(driver):
    return driver.find_element(By.ID, 'UsagePage.ScanCountsDestinationTable.GrandTotal.Value').text.replace(',', '')


# Obtém as informações da impressora
def getAttrsImpressoras(impressora):
    driver = get_driver()
    sn = None
    total_copias = None
    total_digitalizacoes = None
    total_impressoes = None
    try:
        driver.get(
            f'https://{impressora["ip"]}/hp/device/InternalPages/Index?id=UsagePage')
        sn = get_sn(driver)
        total_impressoes = get_total_impressoes(driver)
        total_copias = get_total_copias(driver)
        total_digitalizacoes = get_total_digitalizacoes(driver)
        print(f'trying with ip {impressora["ip"]}')
    except Exception as error:
        print(error)
    finally:
        driver.close()
        driver.quit()
    # Retorna um dicionário com os dados obtidos
    return {'sn': sn, 'total_prints': total_impressoes, 'total_copies': total_copias, 'total_scans': total_digitalizacoes, 'printer_id': impressora["id"]}

# Obtém os contadores da lista de todas as impressoras (execução em paralelo)


def getCounters(impressoras):
    result = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for impressora in impressoras:
            futures.append(executor.submit(
                getAttrsImpressoras, impressora=impressora))
        for future in concurrent.futures.as_completed(futures):
            result.append(future.result())
    return result

# Obtém os contadores da lista de todas as impressoras (execução sequencial)


def getCountersST(impressoras):
    result = []
    for impressora in impressoras:
        print(f'{impressora}')
        impRes = getAttrsImpressoras(impressora=impressora)
        print(impRes)
        result.append(impRes)
    return result


def main():
    # conn = DBLoad.create_connection('./db.sqlite3')
    conn = get_connection()
    printers = Printers.Printer.loadAll(conn)
    result = getCounters(printers)
    for counter in result:
        if counter["sn"] is not None:
            counterObj = Counters.Counter(
                counter["printer_id"], counter["total_prints"], counter["total_copies"], counter["total_scans"])
            try:
                counterObj.save(conn)
            except:
                pass
        else:
            print(
                f'Falha ao salvar a impressora {counter["printer_id"]}. Aparenta estar offline')


if __name__ == '__main__':
    main()
