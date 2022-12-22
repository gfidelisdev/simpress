from sqlite3 import Error
table = 'printers'
pk='id'

class Printer:
    def __init__(self, sn, ip):
        self.sn = sn
        self.ip = ip

    def save(self, conn):
        try:
            cur = conn.cursor()
            print(f'INSERT into {table} (sn, ip) values ({self.sn},\'{self.ip}\')')
            result = cur.execute(f'INSERT into printers (sn, ip) values (\'{self.sn}\',\'{self.ip}\')')
            conn.commit()
            print(result)
        except Exception as error:
            print(error)

    def getDict(queryResult, column_names):
        arrResult = []
        for qr in queryResult:
            arrResult.append(dict(zip(column_names, qr)))
        return(arrResult)    

    def load(dictAttrs, conn):
        try:
            query = f'Select * from {table} where '
            for key,attr in dictAttrs:
                query.append(f'{key}={attr},')
            query = query[0:-1]
            query.append(' order by {pk}')
            cur = conn.cursor()
            column_names = list(map(lambda x: x[0], cur.description))
            return Printer.getDict(cur.execute(f'{query}'), column_names)
        except Exception as error:
            print(error)

    def loadAll(conn):
        try:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM printers')
            result = cur.fetchall()
            column_names = list(map(lambda x: x[0], cur.description))
            return Printer.getDict(result, column_names)
        except Exception as error:
            print(error)
        