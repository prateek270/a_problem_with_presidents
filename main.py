import csv
import datetime as dt
from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import statistics
import numpy as np

def readCSVFile():
    rows = []
    with open("U.S. Presidents Birth and Death Information - Sheet1.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    rows = rows[:-1]
    return header, rows


def addNewHeaders(header):
    header.append('year_of_birth')
    header.append('lived_years')
    header.append('lived_months')
    header.append('lived_days')

    return header

def getLivedDaysColumn(rows):
    daysCol = []
    for row in rows:
        ld = row[8]
        daysCol.append(ld)
    
    return daysCol

def getPresidentsName(rows):
    name = []
    for row in rows:
        pName = row[0]
        name.append(pName)
    
    return name

def populate_data(rows):

    for row in rows:
        dob = row[1]
        try:
            birthObj = dt.datetime.strptime(dob, '%b %d, %Y')
        except ValueError:
            # It didn't work with %b, try with %B
            try:
                birthObj = dt.datetime.strptime(dob, '%B %d, %Y')
            except ValueError:
                # Its not Jun or June, eeek!
                raise ValueError("Date format doesn't match!")
        if dob == np.NaN:
            continue

        dod = row[3]
        deathObj = ''
        if dod != '':
            try:
                deathObj = dt.datetime.strptime(dod, '%b %d, %Y')
            except ValueError:
                # It didn't work with %b, try with %B
                try:
                    deathObj = dt.datetime.strptime(dod, '%B %d, %Y')
                except ValueError:
                    # Its not Jun or June, eeek!
                    raise ValueError("Date format doesn't match!")

        birthYear = birthObj.year
        row.append(birthYear)
        livedYears = getLivedYears(birthObj, deathObj)
        row.append(livedYears)
        row.append(getLivedMonths(birthObj, deathObj, livedYears))
        row.append(getLivedDays(birthObj, deathObj))

    return rows

def getLivedYears(dob_obj, dod_obj):
    effective_dod_obj = dod_obj

    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')

    return (relativedelta(effective_dod_obj, dob_obj).years)


def getLivedMonths(dob_obj, dod_obj, total_years):
    effective_dod_obj = dod_obj

    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')

    return (relativedelta(effective_dod_obj, dob_obj).months + (total_years * 12))


def getLivedDays(dob_obj, dod_obj):
    effective_dod_obj = dod_obj
    if (effective_dod_obj == ''):
        today_str = dt.datetime.strftime(dt.date.today(), '%b %d, %Y')
        effective_dod_obj = dt.datetime.strptime(today_str, '%b %d, %Y')

    a = dt.datetime.strftime(effective_dod_obj, '%b %d, %Y')
    a = dt.datetime.strptime(a, '%b %d, %Y').date()
    b = dt.datetime.strftime(dob_obj, '%b %d, %Y')
    b = dt.datetime.strptime(b, '%b %d, %Y').date()

    return ((a - b).days)
def printTable(header, list, name):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    if name!='statistics.png':
        list.insert(0, header)
        df = pd.DataFrame(list[1:11], columns=header)
    else:
        list.insert(0, ['Statistics Type', 'Value'])
        df = pd.DataFrame(list[1:], columns=list[0])

    ax.table(cellText=df.values, colLabels=df.columns, loc='center', colColours=(['cyan'] * len(header)))

    fig.tight_layout()
    plt.savefig(name, dpi=400)
    plt.show()


def plotGraph(x,y,list):
    ax = plt.gca()

    # Rotating the X-axis values by 90 to make them visible
    ax.tick_params(axis='x', labelrotation=90)

    # Filling color between the two values of Standard Deviation
    #ax.fill_between(x, y_sd_min, y_sd_max, color='blue', alpha=0.15, label='Standard Deviation')

    plt.plot(x,y)
    plt.axhline(y=list[0][1], label='Mean - '+ str(format(list[0][1], ".2f")), linestyle=':',color = "red")
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
    plt.show()

def main():
    header, rows = readCSVFile()
    #print (rows)

    header = addNewHeaders(header)
    #print ("--------------------")
    rows = populate_data(rows)
    #print (rows)
    leastLivedPrez = sorted(rows, key=itemgetter(8))

    #printTable(header,leastLivedPrez, 'leastLived.png')
    mostLivedPrez = sorted(rows, key=itemgetter(8), reverse=True)
    #printTable(header,mostLivedPrez, 'mostLived.png')

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
    print(list)


main()