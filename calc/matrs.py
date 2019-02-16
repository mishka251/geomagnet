# -*- coding: utf-8 -
from os import listdir, getcwd


def matrixFromFile(filename):
    f = open(filename, 'r')
    mat = []     
    all_lines = f.readlines() 
    lines_cnt = len(all_lines) - 2
    lines = all_lines[1:lines_cnt + 1]#строки с числами

    for line in lines:
        l = []
        for str in line.split(', '):
            s = str.strip('],.][\n')
            if s != '':
                l.append(float(s))
        if len(l) > 0:
            mat.append(l)
    return mat

def matrixIsSquare(matrix):
    """
    проверка матрицы на квадратную. 
    Для тестов ввода
    """
    n = len(matrix)
    for i in range(n):
        if len(matrix[i]) != n:
            return False
    return True

def get_actual_matrixes2(year):
    """
    Взятие актуальных матриц из папки
    Для заданного года
    """

    dir = "calc/matrixesFiles/"

    files = listdir(dir)

    years = [ int(year[1:5]) for year in files if year.startswith('g') ]

    Age = max([x for x in years if x < year])

    SV_g = matrixFromFile(dir + "SV_g.txt")
    SV_h = matrixFromFile(dir + "SV_h.txt")

    IGRF_g = matrixFromFile(dir + "g" + str(Age) + ".txt")
    IGRF_h = matrixFromFile(dir + "h" + str(Age) + ".txt")

    if not (matrixIsSquare(IGRF_g) or matrixIsSquare(IGRF_h)):
        print('Ошибка, матрицы IGRF не квадратные')
        return []

    if not (matrixIsSquare(SV_g) or matrixIsSquare(SV_h)):
        print('Ошибка, матрицы SV не квадратные')
        return []

    if len(SV_g) != len(SV_h) or len(SV_g) != len(IGRF_g) or len(SV_g) != len(IGRF_h):
        print("Ошибка, размеры матриц разные")
        return []

    N = len(IGRF_g)

    F_IGRF_g = [0] * N
    F_IGRF_h = [0] * N


    for i in range(0, N):
        F_IGRF_g[i] = [0] * N
        F_IGRF_h[i] = [0] * N
        for j in range(0, N):
            F_IGRF_g[i][j] = IGRF_g[i][j] + (SV_g[i][j]) * (year - Age)
            F_IGRF_h[i][j] = IGRF_h[i][j] + (SV_h[i][j]) * (year - Age)

    return [Age, N, IGRF_g, IGRF_h, SV_g, SV_h, F_IGRF_g, F_IGRF_h]