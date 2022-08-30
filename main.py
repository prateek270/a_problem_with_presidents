import csv
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from dateutil.relativedelta import relativedelta
from operator import itemgetter

def readCSVFile():
    rows = []
    with open("U.S. Presidents Birth and Death Information - Sheet1.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    rows = rows[:-1]
    return header, rows


def getLivedDaysColumn(rows):
    daysCol = []
    for row in rows:
        ld = row[8]
        daysCol.append(ld)
    
    return daysCol

def getPresidentsName(rows):
    names = []
    for row in rows:
        pName = row[0]
        names.append(pName)
    
    return names

def addData(rows):
    for row in rows:
        dob = row[1]
        try:
            birthObj = dt.datetime.strptime(dob, '%b %d, %Y')
        except ValueError:
            try:
                birthObj = dt.datetime.strptime(dob, '%B %d, %Y')
            except ValueError:
                raise ValueError("Date format doesn't match!")
        if dob == np.NaN:
            continue

        dod = row[3]
        deathObj = ''
        if dod != '':
            try:
                deathObj = dt.datetime.strptime(dod, '%b %d, %Y')
            except ValueError:
                try:
                    deathObj = dt.datetime.strptime(dod, '%B %d, %Y')
                except ValueError:
                    raise ValueError("Date format doesn't match!")

        birthYear = birthObj.year
        row.append(birthYear)
        if deathObj == '':
            today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
            deathObj = dt.datetime.strptime(today_str, '%b %d, %Y')
            
        livedYears = relativedelta(deathObj, birthObj).years
        row.append(livedYears)
        livedMonths = relativedelta(deathObj, birthObj).months + (livedYears * 12)
        row.append(livedMonths)
        row.append(getLivedDays(birthObj, deathObj))

    return rows


def getLivedDays(birthObj, deathObj):
    a = dt.datetime.strftime(deathObj, '%b %d, %Y')
    a = dt.datetime.strptime(a, '%b %d, %Y').date()
    b = dt.datetime.strftime(birthObj, '%b %d, %Y')
    b = dt.datetime.strptime(b, '%b %d, %Y').date()

    return ((a - b).days)

def printTable(header, list, name):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    headerLen = len(header)
    if name != 'statistics.png':
        list.insert(0, header)
        df = pd.DataFrame(list[1:11], columns=header)
    else:
        list.insert(0, ['Statistics Type', 'Value'])
        df = pd.DataFrame(list[1:], columns=list[0])
        headerLen = 2

    ax.table(cellText=df.values, colLabels=df.columns, loc='center', colColours=(['cyan'] * headerLen))

    fig.tight_layout()
    plt.savefig(name, dpi=400)
    plt.show()


def plotGraph(x,y,list):
    ax = plt.gca()

    ax.tick_params(axis='x', labelrotation=90)

    plt.plot(x,y)
    plt.axhline(y=list[0][1], label='Mean - '+ str(format(list[0][1])), linestyle=':',color = "red")
    plt.axhline(y=list[2][1], label='Median - '+ str(format(list[2][1])), linestyle='-',color = "brown")
    plt.axhline(y=list[3][1], label='Mode - '+ str(format(list[3][1])), linestyle='dotted',color = "orange")
    plt.axhline(y=list[4][1], label='Max - '+ str(format(list[4][1])), linestyle='--',color = "green")
    plt.axhline(y=list[5][1], label='Min - '+ str(format(list[5][1])), linestyle='--',color = "green")

    plt.xlabel('Name of the president')
    plt.ylabel('Number of days lived')
    plt.title("Line graph to show number of days lived by each president")
    plt.xticks(rotation = 90)
    plt.tick_params(axis='x', which='major', labelsize=8)
    legend = ax.legend(loc='lower left')
    plt.savefig("graph.png", dpi=300)
    plt.show()

def main():
    header, rows = readCSVFile()
    #print (rows)
    header.append('year_of_birth')
    header.append('lived_years')
    header.append('lived_months')
    header.append('lived_days')

    #print ("--------------------")
    rows = addData(rows)
    #print (rows)
    leastLivedPresidents = sorted(rows, key=itemgetter(8))

    printTable(header,leastLivedPresidents, 'leastLived.png')
    mostLivedPresidents = sorted(rows, key=itemgetter(8), reverse=True)
    printTable(header,mostLivedPresidents, 'mostLived.png')

    livedDays = getLivedDaysColumn(rows)
    presidentsName = getPresidentsName(rows)

    mean = np.mean(livedDays)
    median = np.median(livedDays)
    modeVal = statistics.mode(livedDays)
    maxVal = np.max(livedDays)
    minVal = np.min(livedDays)
    standardDeviation = np.std(livedDays)
    weightedAvg = np.average(livedDays)


    list = []
    list.append(['Mean', mean])
    list.append(['Weighted Average', weightedAvg])
    list.append(['Median', median])
    list.append(['Mode', modeVal])
    list.append(['Max', maxVal])
    list.append(['Min', minVal])
    list.append(['Standard Deviation', standardDeviation])
    #printTable(header,list, 'statistics.png')
    plotGraph(presidentsName,livedDays, list)
    #print(list)

main()