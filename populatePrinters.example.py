from contadores import get_driver, get_sn, get_connection
import Printers
import concurrent.futures

# Lista de IPs das impressoras - strings - alterar para os ips das impressoras da regional
IP_LIST = [
    '192.168.10.101',
    '192.168.10.102',
    '192.168.10.103',
    '192.168.10.104',
    '192.168.10.105',

]


def savePrinter(driver, ip, conn):
    try:
        driver.get(f'https://{ip}/hp/device/InternalPages/Index?id=UsagePage')
        sn = get_sn(driver)

        # sn = f'BRG{ip.split(".")[3]}'  # para gerar um database mock
        print(f'SN: {sn} == IP: {ip}')
        printer = Printers.Printer(sn=sn, ip=ip)
        return f'Impressora {ip}:{sn} inserida com sucesso', printer.save(conn)
    except Exception as error:
        return f'{error}'


def createPrintersInDatabase(conn):
    try:
        result = []
        driver = get_driver()
        print(f'driver: {driver}')
        for ip in IP_LIST:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                futures.append(executor.submit(
                    savePrinter, driver=driver, ip=ip, conn=conn))
            for future in concurrent.futures.as_completed(futures):
                result.append(future.result())
        driver.quit()
        return result
    except Exception as error:
        return f'{error}'


def main():
    conn = get_connection()
    createPrintersInDatabase(conn)


if __name__ == "__main__":
    main()
