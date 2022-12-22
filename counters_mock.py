from Printers import Printer
from Counters import Counter
from random import randrange
from contadores import get_connection


def getPrinters():
    pass


def getCounter(printer, lastPrintersCounter, created_at):
    if printer["id"] in lastPrintersCounter:
        # if lastPrintersCounter:
        print(lastPrintersCounter[printer["id"]])
        return Counter(printer_id=printer["id"],
                       total_prints=lastPrintersCounter[printer["id"]]["total_prints"]+randrange(
                           21),
                       total_copies=lastPrintersCounter[printer["id"]]["total_copies"]+randrange(
                           21),
                       total_scans=lastPrintersCounter[printer["id"]
                                                       ]["total_scans"]+randrange(21),
                       created_at=created_at)
    else:
        return Counter(printer_id=printer["id"], total_prints=0, total_copies=0, total_scans=0, created_at=created_at)
    pass


def createCounters(printers, startYear, endYear):
    counters = []
    lastPrintersCounters = {}
    # deve ser endYear + 1 pois o range não inclui o valor do segundo item
    for year in range(startYear, endYear+1):
        for month in range(1, 13):
            for day in range(1, 32):
                for printer in printers:
                    if day <= 28:
                        counter = getCounter(
                            printer, lastPrintersCounters, f'{year}-{month}-{day} 00:00:01')
                        lastPrintersCounters[printer["id"]] = counter.toDict()
                        counters.append(counter)
                    elif day > 28 and day < 30:
                        if month != 2:
                            counter = getCounter(
                                printer, lastPrintersCounters, f'{year}-{month}-{day} 00:00:01')
                            lastPrintersCounters[printer["id"]
                                                 ] = counter.toDict()
                            counters.append(counter)
                    else:
                        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                            counter = getCounter(
                                printer, lastPrintersCounters, f'{year}-{month}-{day} 00:00:01')
                            lastPrintersCounters[printer["id"]
                                                 ] = counter.toDict()
                            counters.append(counter)
    return counters


def main():
    conn = get_connection()
    printers = Printer.loadAll(conn)
    counters = createCounters(printers, 2020, 2024)
    for counter in counters:
        print(counter.toDict())
        counter.save(conn)


if __name__ == '__main__':
    main()
