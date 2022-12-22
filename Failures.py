from datetime import datetime, date
table = "failures"
pk = "id"


class Failure:
    id = None
    value = None
    failure_time = None
    printer_id = None

    def __init__(self, printer_id, failure_time=None):
        self.printer_id = printer_id
        self.created_at = failure_time

    def setFailureTime(self, failure_time):
        if failure_time is None:
            self.failure_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.failure_time == failure_time

    def save(self, conn):
        try:
            cur = conn.cursor()
            self.setFailureTime(self.failure_time)
            query = f'INSERT into {table} (printer_id, failure_time) \
                values ({self.printer_id},\'{self.failure_time}\')'
            print(query)
            result = cur.execute(query)
            conn.commit()
            return result
        except Exception as error:
            print(error)

    def toDict(self):
        return {
            "id": self.id,
            "failure_time": self.failure_time,
            "printer_id": self.printer_id
        }

    def getDict(queryResult, column_names):
        arrResult = []
        for qr in queryResult:
            arrResult.append(dict(zip(column_names, qr)))
        return (arrResult)

    """
    Carrega da base de dados as falhas com base nas condições dadas
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
                query.append(
                    f'{condition["field"]}{condition["operation"]}{condition["value"]}')
                if condition != dictAttrs[-1]:
                    query.append(f' and')

            query = query[0:-1]
            query.append(' order by {pk}')
            cur = conn.cursor()
            column_names = list(map(lambda x: x[0], cur.description))
            return Failure.getDict(cur.execute(f'{query}'), column_names)
        except Exception as error:
            print(error)

    def loadAll(conn):
        cur = conn.cursor()
        result = cur.execute(f'SELECT * from {table}')
        arrResult = []
        column_names = list(map(lambda x: x[0], cur.description))
        for r in result:
            arrResult.append(dict(zip(column_names, r)))
        return arrResult
