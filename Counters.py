from sqlite3 import Error
from datetime import datetime, date
table = "counters"
pk = "id"

class Counter:
    value=None
    created_at=None
    printer=None
    def __init__(self, printer_id, total_prints, total_copies, total_scans):
        self.total_copies = 'null' if total_copies is None else total_copies
        self.total_prints = 'null' if total_prints is None else total_prints
        self.total_scans = 'null' if total_scans is None else total_scans
        self.printer_id = printer_id

    def save(self, conn):
        try:
            cur = conn.cursor()
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = f'INSERT into {table} (total_prints, total_copies, total_scans,created_at,printer_id) \
                values ({self.total_prints},{self.total_copies},{self.total_scans},\'{self.created_at}\',{self.printer_id})'
            print(query)
            result = cur.execute(query)
            conn.commit()
            return result
        except Error as error:
            print(error)
    
    def getDict(queryResult, column_names):
        arrResult = []
        for qr in queryResult:
            arrResult.append(dict(zip(column_names, qr)))
        return(arrResult)    

    """
    Carrega da base de dados os contadores com base nas condições dadas
    dictAttrs deve ter o formato
    [
        {"field":"nome_do_campo"},
        {"operation":"operação (=, <, >, <=, >=, !=)"}
        {"value":"valor_a_ser_comparado"}
    ]
    """
    def load(dictAttrs, conn):
        try:
            query = f'Select * from {table} where '
            for condition in dictAttrs:
                query.append(f'{condition["field"]}{condition["operation"]}{condition["value"]}')
                if condition != dictAttrs[-1]:
                    query.append(f' and') 

            query = query[0:-1]
            query.append(' order by {pk}')
            cur = conn.cursor()
            column_names = list(map(lambda x: x[0], cur.description))
            return Counter.getDict(cur.execute(f'{query}'), column_names)
        except Exception as error:
            print(error)

    def loadAll(conn):
        cur = conn.cursor()
        result = cur.execute(f'SELECT * from contadores')
        arrResult = []
        column_names = list(map(lambda x: x[0], cur.description))
        for r in result:
            arrResult.append(dict(zip(column_names, r)))
        return arrResult