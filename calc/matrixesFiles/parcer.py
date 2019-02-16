# -*- coding: utf-8 -
from xlrd import *
from os import linesep

def printMatrix(matr, file):
    f = open(file, 'w')
    f.write('[')
    f.write(linesep)
    for i in range(len(matr)):
        f.write(str(matr[i]))
        f.write(linesep)
    f.write(']')
    f.close()
        

file = "IGRF12coeffs.xls"

rb = open_workbook(file,formatting_info=True)
sheet = rb.sheet_by_index(0)

cols = sheet.ncols
rows = sheet.nrows

matrixes = cols - 3-1# g/h, n, m, SV

h_mats = [0]*matrixes
g_mats = [0]*matrixes
N = 14
for i in range(matrixes):
    h_mats[i] = [0]*N
    g_mats[i] = [0]*N
    for j in range(N):
        h_mats[i][j] = [0]*N
        g_mats[i][j] = [0]*N

years = [0]*(matrixes)
SV_g = [0]*N
SV_h = [0]*N
for i in range(N):
    SV_g[i] = [0]*N 
    SV_h[i] = [0]*N 

col_start = 3
col_end = cols - 1
row = sheet.row_values(3)
for col in range(col_start, col_end):
    years[col-col_start] = int(row[col])
print(years)

for rownum in range(4, rows):  #с 4 строки идут данные

    row = sheet.row_values(rownum)

    rowtype = row[0]
    n = int(row[1])
    m = int(row[2])


    for matr in range(matrixes):
        if rowtype=='g':
            g_mats[matr] [n][m] = row[3+matr]
        else:
            h_mats[matr] [n][m] = row[3+matr]
    if rowtype =='g':
        SV_g[n][m] = row[cols-1]
    else:
        SV_h[n][m] = row[cols-1]

printMatrix(SV_g, 'SV_g.txt')
printMatrix(SV_h, 'SV_h.txt')


for i in range(matrixes):
    printMatrix(g_mats[i], 'g'+str(years[i])+'.txt')

    printMatrix(h_mats[i], 'h'+str(years[i])+'.txt')

