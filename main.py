import csv
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from numpy import NaN


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
        if dob == NaN:
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

        row.append(1)
        row.append(2)
        row.append(3)
        row.append(4)

    return rows
def printPresidentsList(header, list):
    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    list.insert(0, header)

    df = pd.DataFrame(list[1:], columns=header)

    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    fig.tight_layout()

    plt.show()


def main():
    header, rows = readCSVFile()
    #print (rows)

    header = addNewHeaders(header)
    #print ("--------------------")
    rows = populate_data(rows)
    #print (rows)

    printPresidentsList(header,rows)


main()