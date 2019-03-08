# -*- coding: utf-8 -
from datetime import *
from math import *
from numpy import dot, arange, inf
import time
from .matrs import get_actual_matrixes2 

# ФИЗИЧЕСКИЕ (ИНВАРИАНТНЫЕ) ПАРАМЕТРЫ ЗЕМЛИ\n")
R = 6371.032      # Средний радиус Земли, [км]
a = 6378.245      # Большая полуось Земного элепсоида вращения, [км] Эллипсоид Красовского
b = 6356.863019   # Малая полуось Земного элепсоида вращения, [км] Эллипсоид Красовского
PI_cache = [1]
def PI_odd_cached(n):
    """
     Вычисление PI_odd с кешированием.
     Результаты запиываются в массив, потом из него извелкаются
    """
    global PI_cache
    while n >= len(PI_cache):
        PI_cache.append(PI_cache[len(PI_cache) - 1] * (2 * len(PI_cache) - 1))
    return PI_cache[n]

factorials_cache = [1]
def factorial_cached(n):
    """
    Вычисление факториала с кешированием
    """
    global factorials_cache
    while len(factorials_cache) <= n:
        factorials_cache.append(factorials_cache[len(factorials_cache) - 1] * len(factorials_cache))
    return factorials_cache[n]


def epsilon(i):
    """
    Функция расчета нормировачного множителя
    """
    if (i < 1):
        eps = 1
    else:
        eps = 2
    return eps

def P(n, m, teta):
    """функция расчета
    Нормированной по Шмидту присоединенной функции Лежандра Pnm(cos(teta))
    n, m - для Pnm, teta - для косинуса и синуса
     """
    pr = [0] * 7
    pr[0] = 1
    for i in range(1, 7):
        pr[i] = pr[i - 1] * (n - m - (2 * (i - 1))) * (n - m - (2 * i - 1))

    dels = [0] * 7
    dels[0] = 1
    for i in range(1, 7):
        dels[i] = dels[i - 1] * (2 * i) * (2 * n - (2 * i - 1))

    s = [0] * 7
    for i in range(0, 7):
        s[i] = pr[i] / dels[i] * ((cos(teta)) ** (n - m - (2 * i)))

    b = epsilon(m) / (factorial_cached(n + m) * factorial_cached(n - m))
    sum = (s[0] - s[1] + s[2] - s[3] + s[4] - s[5] + s[6])
    return PI_odd_cached(n) * sqrt(b) * (sin(teta) ** m) * sum

def dPdtet(n, m, teta):
    """функция расчета производной
    Нормированной по Шмидту присоединенной функции Лежандра по тета
    dPnm(cos(teta))/dteta
    n, m - для Pnm, teta - для косинуса и синуса
    """
    pr = [0] * 7
    pr[0] = 1
    for i in range(1, 7):
        pr[i] = pr[i - 1] * (n - m - (2 * (i - 1))) * (n - m - (2 * (i - 1) + 1))

    dels = [0] * 7
    dels[0] = 1
    for i in range(1, 7):
        dels[i] = dels[i - 1] * (2 * i) * (2 * n - (2 * i - 1))

    s = [0] * 7
    for i in range(0, 7):
        s[i] = pr[i] / dels[i] * ((cos(teta)) ** (n - m - (2 * i)))

    s2 = [0] * 7
    for i in range(0, 7):
        s2[i] = pr[i] / dels[i] * ((n - m - (2 * i)) * ((cos(teta)) ** (n - m - (2 * i) - 1)) * (-sin(teta)))

    b = epsilon(m) / (factorial_cached(n + m) * factorial_cached(n - m))
    sum1 = (s[0] - s[1] + s[2] - s[3] + s[4] - s[5] + s[6])
    sum2 = (s2[0] - s2[1] + s2[2] - s2[3] + s2[4] - s2[5] + s2[6])
    mnoj = PI_odd_cached(n) * sqrt(b)
    slag1 = m * (sin(teta) ** (m - 1)) * cos(teta) * sum1
    slag2 = (sin(teta) ** m) * sum2
    return mnoj * (slag1 + slag2)

def Uf(r, lamda, teta, F_g, F_h):
    """
    Функция расчета потенциала индукции геомагнитного поля
    внутреземных источников _U(_r,_lamda,_tetta)
    """
    global R
    N = len(F_g)
    sum_n = 0  # суммирование п,
    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * P(n, m, teta)
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 1)) * sum_m
    potential = R * sum_n
    return potential

def Bxf(r, lamda, teta, F_g, F_h):
    """
    функция расчёта составляющей вектора индукции главного поля X’
    На основе производной dU(r, lamda, teta)/dteta
    """
    global R
    N = len(F_g)
    sum_n = 0  # суммирование п,
    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * dPdtet(n, m, teta)
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return potential

def Byf(r, lamda, teta, F_g, F_h):
    """
    функция расчёта составляющей вектора индукции главного поля  Y’
    На основе производной dU(r, lamda, teta)/dteta
    """
    global R
    N = len(F_g)
    sum_n = 0   # суммирование п,
    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            tmp = m * (F_g[n][m] * sin(m * lamda) - F_h[n][m] * cos(m * lamda))
            half_REZ = tmp * P(n, m, teta)
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
    potential = sum_n / sin(teta)
    return potential

def Bzf(r, lamda, teta, F_g, F_h):
    """
    функция расчёта составляющей вектора индукции главного поля Z`
    На основе производной dU(r, lamda, teta)/dteta
    """
    global R
    N = len(F_g)
    sum_n = 0  # суммирование п,
    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * P(n, m, teta)
            sum_m = sum_m + half_REZ
        sum_n = sum_n + (n + 1) * ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return -potential

def calcMAG(north, east, alt, F_g, F_h):
    global a, b

    h11 = F_h[1][1]
    g11 = F_g[1][1]
    g10 = F_g[1][0]    
# координаты в географической системе (GEO), переведенные в радианы
    latGEO = radians(north)
    longGEO = radians(east)
    altGEO = alt

    tmp = (a ** 2) * (cos(latGEO) ** 2) + (b ** 2) * (sin(latGEO) ** 2)   # чтобы не писать 2 раза
    rE = sqrt((altGEO ** 2) + 2 * altGEO * sqrt(tmp) + ((a ** 4) * (cos(latGEO) ** 2) + (b ** 4) * (sin(latGEO) ** 2)) / tmp)

# расчет углов поворота
# угол поворотота вокруг оси Y
    lamda = atan(h11 / g11)
    try:
        fi = ((pi / 2) - asin((g11 * cos(lamda) + h11 * sin(lamda)) / (g10))) - pi / 2
    except ValueError:
        fi = 0

# перевод в геоцентрическую систему
    xGEO = rE * cos(latGEO) * cos(longGEO)
    yGEO = rE * cos(latGEO) * sin(longGEO)
    zGEO = rE * sin(latGEO)

# матрица координат GEO
    GEO = [xGEO, yGEO, zGEO]

# Поворотные матрицы 3x3
    t5Y = [[cos(fi), 0, sin(fi)],
        [0,       1,    0],
        [-sin(fi),  0, cos(fi)]]

    t5Z = [[cos(lamda), sin(lamda), 0],
        [-sin(lamda), cos(lamda), 0],
        [0,               0,      1]]
# Умножение матриц: t5 = t5Y*t5Z
    t5 = dot(t5Y, t5Z)

# Умножение матриц: MAG = t5*tGEO
    MAG = dot(t5, GEO)
# пересчет в град
    latMAG = degrees(atan((MAG[2]) / (sqrt(MAG[0] ** 2 + MAG[1] ** 2))))
    if(MAG[1] > 0):
        longMAG = degrees(acos((MAG[0]) / (sqrt(MAG[0] ** 2 + MAG[1] ** 2))))
    else:
        longMAG = 360 - degrees((acos((MAG[0]) / (sqrt(MAG[0] ** 2 + MAG[1] ** 2)))))

    return [latMAG, longMAG, sqrt((MAG[0] ** 2) + (MAG[1] ** 2) + (MAG[2] ** 2))]

def getCoordinates(north, east, alt):
    """
    Преобразование географических координат
    В сферические
    Аргументы:
    north - широта(северная+, южная -)
    east - долгота(восточная +, западная -)
    alt - высота над уровнем моря
    Возвращает [lamda, teta, r]

    """
    global a, b

    lamda = radians(east)
    fi = radians(north)
    a2 = a ** 2  # сокращения чтобы не писать несколько раз
    b2 = b ** 2
    cosfi2 = (cos(fi) ** 2)
    sinfi2 = (sin(fi) ** 2)
    tmp = sqrt(a2 * cosfi2 + b2 * sinfi2)

    # Широта в сферических координатах
    fi_sh = atan(((b2 + alt * tmp) / (a2 + alt * tmp)) * tan(fi))
    # Полярный угол
    teta = (pi / 2) - fi_sh
    # поправка на геоид (полярное сжатие Земли)
    r = sqrt((alt ** 2) + 2 * alt * tmp + ((a ** 4) * cosfi2 + (b ** 4) * sinfi2) / (tmp ** 2))
    return [lamda, teta, r, fi, fi_sh]


def calculate(north, east, alt, year, UT):
    """
    Расчёт параметров геомагнитного поля в заданной точке в заданное время
    north - северная широта(южня со знаком "-")
    east - долгота
    alt - высота над уровнем моря
    year - дата(например 2015.5 - июль 2015 года(половина года прошла))
    UT - ???

    """
    [lamda, teta, r, fi, fi_sh] = getCoordinates(north, east, alt) 
    

    [Age, N, IGRF_g, IGRF_h, SV_g, SV_h, F_g, F_h] = get_actual_matrixes2(year)
    # Актуализация матриц сферических гармонических коэффициентов


# составляющие вектора индукции геомагнитного поля внутриземных источников
    try:
        BX = Bxf(r, lamda, teta, F_g, F_h)
    except ZeroDivisionError:
        BX = 1
    try:
        BY = Byf(r, lamda, teta, F_g, F_h)
    except ValueError:
        BY = 1
    except ZeroDivisionError:
        BY = 1
    try:
        BZ = Bzf(r, lamda, teta, F_g, F_h)
    except ZeroDivisionError:
        BZ = 1

# прямоугольные составляющи вектора индукции в точке с координатами fi,
# lamda,r, [нТл]
    Bx = BX * cos(fi - fi_sh) + BZ * sin(fi - fi_sh)
    By = BY
    Bz = BZ * cos(fi - fi_sh) - BX * sin(fi - fi_sh)

# полный вектор геомагнитного поля анутриземных исочников, [нТл]
    B = sqrt(Bx * Bx + By * By + Bz * Bz)

# Магнитное склонение, [град]
    D = degrees(atan(By / Bx))
# Магнитное наклонение, [град]
    I = degrees(asin(Bz / B))

# Широта северного магнитного полюса
    FI = degrees(atan(IGRF_g[1][0] / sqrt(IGRF_g[1][1] ** 2 + IGRF_h[1][1] ** 2)))

# Долгота северного магнитного полюса
    LAMDA = degrees(atan(IGRF_h[1][1] / IGRF_g[1][1]))

# Магнитный момент геомагнитного диполя
    M = (r ** 3) * sqrt(IGRF_g[1][0] ** 2 + IGRF_g[1][1] ** 2 + IGRF_h[1][1] ** 2)
    U = Uf(r, lamda, teta, F_g, F_h)

    [latMAG, longMAG, absMAG] = calcMAG(north, east, alt, F_g, F_h)

    proto_f = [0] * 16
    proto_f[0] = teta
    proto_f[1] = lamda
    proto_f[2] = N
    proto_f[3] = U
    proto_f[4] = Bx
    proto_f[5] = By
    proto_f[6] = Bz
    proto_f[7] = B
    proto_f[8] = D
    proto_f[9] = I
    proto_f[10] = FI
    proto_f[11] = LAMDA
    proto_f[12] = M
    proto_f[13] = latMAG
    proto_f[14] = longMAG
    proto_f[15] = absMAG

    return proto_f



def getIsolines(year):
    f = open('calc/log2014.txt', 'r')
    line = f.readline()
    return line
