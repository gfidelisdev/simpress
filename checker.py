import csv

def readFile(filename):
    f = open(filename, newline='')
    return csv.DictReader(f, delimiter=';', quotechar='"')


def main():
    csvIni = readFile('./Pasta4.CSV')
    i=1
    k=1
    csvOut = open('.out.csv', 'w', newline='')
    fieldNames = ['Host Group', 'Host', 'Item', 'FROM_UNIXTIME(his.clock)', 'value', 'mes']
    writer = csv.DictWriter(csvOut, fieldnames=fieldNames, delimiter=';')
    writer.writeheader()
    for rowIni in csvIni:
        j=1
        csvEnd = readFile('./Pasta4-end.CSV')
        for rowEnd in csvEnd:
            # print(f'{i} - {j}')
            j=j+1
            if rowIni['Host'] == rowEnd['Host'] and rowIni['Item'] == rowEnd['Item']:
                total = int(rowEnd["value"])-int(rowIni["value"])
                print(f'{k}: {rowIni["Host"]} ::: {rowEnd["Host"]} === {rowIni["Item"]} : {rowEnd["Item"]} --- {rowIni["value"]} : {rowEnd["value"]} : total==> {total}')
                k = k+1
                writer.writerow({'Host Group':rowIni["Host"], 'Host':rowIni["Host"], 'Item': rowIni["Item"], 'FROM_UNIXTIME(his.clock)': rowIni["FROM_UNIXTIME(his.clock)"],'value':total, 'mes':rowIni["mês"]})
                
        i=i+1


if __name__ == '__main__':
    main()