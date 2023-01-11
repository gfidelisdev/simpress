from datetime import datetime, date
table = "counters"
pk = "id"


class Counter:
    value = None
    created_at = None
    printer_id = None

    def __init__(self, printer_id, total_prints, total_copies, total_scans, total_prints_color=None, total_copies_color=None, created_at=None):
        self.total_copies = 'null' if total_copies is None else total_copies
        self.total_prints = 'null' if total_prints is None else total_prints
        self.total_copies_color = 'null' if total_copies_color is None else total_copies_color
        self.total_prints_color = 'null' if total_prints_color is None else total_prints_color
        self.total_scans = 'null' if total_scans is None else total_scans
        self.printer_id = printer_id
        self.created_at = created_at

    def setCreatedAt(self, created_at):
        if created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.created_at == created_at

    def save(self, conn, created_at=None):
        try:
            cur = conn.cursor()
            self.setCreatedAt(self.created_at)
            query = f'INSERT into {table} (total_prints, total_copies, total_scans, total_prints_color, total_copies_color ,created_at,printer_id) \
                values ({self.total_prints},{self.total_copies},{self.total_scans},\
                    {self.total_prints_color},{self.total_copies_color},\
                    \'{self.created_at}\',{self.printer_id})'
            print(query)
            result = cur.execute(query)
            conn.commit()
            return result
        except Exception as error:
            print(error)

    def toDict(self):
        return {
            "created_at": self.created_at,
            "total_copies": self.total_copies,
            "total_scans": self.total_scans,
            "total_prints": self.total_prints,
            "total_copies_color": self.total_copies_color,
            "total_prints_color":self.total_prints_color,
            "printer_id": self.printer_id
        }

    def getDict(queryResult, column_names):
        arrResult = []
        for qr in queryResult:
            arrResult.append(dict(zip(column_names, qr)))
        return (arrResult)

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
                query.append(
                    f'{condition["field"]}{condition["operation"]}{condition["value"]}')
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
        result = cur.execute(f'SELECT * from {table}')
        arrResult = []
        column_names = list(map(lambda x: x[0], cur.description))
        for r in result:
            arrResult.append(dict(zip(column_names, r)))
        return arrResult
