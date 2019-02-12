# -*- coding: utf-8 -
from datetime import *
from math import *
# from random import randint, uniform, seed, choice #для тестов
from numpy import dot
import time
#from module.calculator import calculate, days_z
from .matrixes import * 

def days_z(year, month, day):
    """
    Номер дня от начала года
    вход year - год, month - номер месяца, day - номер день в месяце
    """
    #               ян фе ма ап ма ию ию ав се ок но де
    day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0:
        day_in_month[1] += 1  # високосный год

    sum = 0
    for i in range(month - 1):
        sum += day_in_month[i]
    sum += day
    return sum


# ФИЗИЧЕСКИЕ (ИНВАРИАНТНЫЕ) ПАРАМЕТРЫ ЗЕМЛИ\n")
R = 6371.032      # Средний радиус Земли, [км]
a = 6378.245      # Большая полуось Земного элепсоида вращения, [км] Эллипсоид Красовского
b = 6356.863019   # Малая полуось Земного элепсоида вращения, [км] Эллипсоид Красовского
Age = 2015.0      # Эпоха

F_g = [0]
F_h = [0]

def PI_odd(n):
    res = 1
    for i in range(1, n + 1):
        res *= (2 * i - 1)
    return res

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

    b = epsilon(m) / (factorial(n + m) * factorial(n - m))
    sum = (s[0] - s[1] + s[2] - s[3] + s[4] - s[5] + s[6])
    return PI_odd(n) * sqrt(b) * (sin(teta) ** m) * sum

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

    b = epsilon(m) / (factorial(n + m) * factorial(n - m))
    sum1 = (s[0] - s[1] + s[2] - s[3] + s[4] - s[5] + s[6])
    sum2 = (s2[0] - s2[1] + s2[2] - s2[3] + s2[4] - s2[5] + s2[6])
    mnoj = PI_odd(n) * sqrt(b)
    slag1 = m * (sin(teta) ** (m - 1)) * cos(teta) * sum1
    slag2 = (sin(teta) ** m) * sum2
    return mnoj * (slag1 + slag2)

def Uf(r, lamda, teta):
    """
    Функция расчета потенциала индукции геомагнитного поля
    внутреземных источников _U(_r,_lamda,_tetta)
    """
    global F_h, F_g
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

def Bxf(r, lamda, teta):
    """
    функция расчёта составляющей вектора индукции главного поля X’
    На основе производной dU(r, lamda, teta)/dteta
    """
    global F_h, F_g
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

def Byf(r, lamda, teta):
    """
    функция расчёта составляющей вектора индукции главного поля  Y’
    На основе производной dU(r, lamda, teta)/dteta
    """
    global F_h, F_g
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

def Bzf(r, lamda, teta):
    """
    функция расчёта составляющей вектора индукции главного поля Z`
    На основе производной dU(r, lamda, teta)/dteta
    """
    global F_h, F_g
    sum_n = 0  # суммирование п,
    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        pi_odd_n = PI_odd(n)
        for m in range(0, n + 1):  # суммирование по m
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * P(n, m, teta)
            sum_m = sum_m + half_REZ
        sum_n = sum_n + (n + 1) * ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return -potential


#def coords(UT, Ynum, teta, lamda, alt):
#    """
#    B2 - вектор индукции магнитного поля магнитосферных токов, вычисляемый
#    солнечно-магнитосферной системе координат
#    Ynum - порядковый номер дня в году [1..365]
#    n_p - концентрация протонов в солнечном ветре [м^-3]
#    n_alpha - концентрация альфа-частиц в солнечном ветре [м^-3]
#    n_m - концентрация малых ионных компонентов [м^-3]
#    psi - угол наклона геомагнитного диполя к плоскости ортогональной линии
#    Земля-Солнце, [град]
#    v - скорость солнечного ветра
#    teta, lamda, alt - географические координаты
#    Возвращает X, Y, Z - Солнечно-магнитосферные координаты в единицах [R - радиус Земли]
#    """
#    n_p = 3800000  # n_p - концентрация протонов в солнечном ветре [м^-3]
#    v = 415100     # v - скорость солнечного ветра
#    R = 6371.032          # Средний радиус Земли

#    n_alpha = 0.06 * n_p  # Расчет концентрации альфа-частиц в солнечном ветре [м^-3]
#    n_m = 0.001 * n_p    # Расчет концентрации малых ионных компонентов [м^-3]

## ---Перевод вектора индукции магнитного поля из географическй системы
## координат
## в солнечно-магнитосферную---
#    alpha1 = radians(11.43)  # угол между осью вращения Земли и осью геомагнитного диполя
#    alpha2 = radians(23.5)   # угол наклона плоскости экватора к плоскости эклиптики
#    U0 = 12  # часов
#    K = 15   # градусов/час
#    fi_SE = radians(360 * (172 - Ynum) / 365)
#    # fi_se - угол между линией Земля-Солнце и проекцией оси вращения Земли
#    # на плоскость эклиптики, [град]

#    fi_m = radians((K * UT - 69))
#    # fi_m - угол между плоскостью полуночного мередиана и мередианальной
#    # плоскостью, содержащей северный магнитный полюс
#    beta0 = asin(sin(alpha2) * cos(fi_SE))   # Склонение Солнца
#    psi = asin(-sin(beta0) * cos(alpha1) + cos(beta0) * sin(alpha1) * cos(fi_m))
#    # psi - угол наклона геомагниного диполя к плоскости ортогональной
#    # линии Земля-Солнце

#    beta1 = radians(K * (UT - U0))  # западная долгота полуденного мередиана

#    beta2 = acos((cos(alpha1) + sin(beta0) * sin(psi)) / cos(psi) * cos(beta0))
#    # угол между полуденным географическим меридианом и плоскостью y = 0 в
#    # солнечно-магнитосферных координатах

#    mat1 = [
#        [cos(beta0), 0, sin(beta0)],
#        [0, 1, 0],
#        [-sin(beta0), 0, cos(beta0)]
#    ]

#    mat2 = [
#        [cos(beta1), -sin(beta1), 0],
#        [sin(beta1), cos(beta1),  0],
#        [0,                0,    1]
#    ]
#    T_array = dot(mat1, mat2)  # Матрица поворота к солнечно-магнитосферным координатам
#    # Матрица перевода из сферических в декартовы координаты
#    S_array = [
#        [sin(teta) * cos(lamda),   cos(teta) * cos(lamda),   (-1) * sin(lamda)],
#        [sin(teta) * sin(lamda),   cos(teta) * sin(lamda),   cos(lamda)],
#        [cos(teta),                      (-1) * sin(teta),         0]
#    ]

#    Q_array = dot(T_array, S_array)

#    spherCoord = [alt, teta, lamda]
#    return dot(Q_array, spherCoord)


def calcMAG(north, east, alt, year):
# Сферические гармонические коэффициенты для эпохи 2015-2020
    h11_igrf = 4797.1
    g11_igrf = -1501
    g10_igrf = -29442

    g10_sv = 10.3
    g11_sv = 18.1
    h11_sv = -22.6

    h11 = h11_igrf + h11_sv * (year - Age)
    g11 = g11_igrf + g11_sv * (year - Age)
    g10 = g10_igrf + g10_sv * (year - Age)
    global a, b
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
    t5Y = [
        [cos(fi), 0, sin(fi)],
        [0,       1,    0],
        [-sin(fi),  0, cos(fi)]
    ]

    t5Z = [
        [cos(lamda), sin(lamda), 0],
        [-sin(lamda), cos(lamda), 0],
        [0,               0,      1]
    ]
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


def calculate(north, east, alt, year, UT):
    """
    Расчёт параметров геомагнитного поля в заданной точке в заданное время
    north - северная широта(южня со знаком "-")
    east - долгота
    alt - высота над уровнем моря
    year - дата(например 2015.5 - июль 2015 года(половина года прошла))
    UT - ???

    """
    global a
    global b
    global F_h, F_g
    print([a, b])
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
    r = sqrt((alt ** 2) + 2 * alt * tmp +
             ((a ** 4) * cosfi2 + (b ** 4) * sinfi2) / (tmp ** 2))

    (F_g, F_h) = get_actual_matrixes(year)
    # Актуализация матриц сферических гармонических коэффициентов



# составляющие вектора индукции геомагнитного поля внутриземных источников
    try:
        BX = Bxf(r, lamda, teta)
    except ZeroDivisionError:
        BX = 1
    try:
        BY = Byf(r, lamda, teta)
    except ValueError:
        BY = 1
    except ZeroDivisionError:
        BY = 1
    try:
        BZ = Bzf(r, lamda, teta)
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
    U = Uf(r, lamda, teta)


    #datenow = date.today()
    #Ynum = days_z(datenow.year, datenow.month, datenow.day)

   # (X_, Y_, Z_) = coords(UT, Ynum, teta, lamda, alt)
###########

    [latMAG, longMAG, absMAG] = calcMAG(north, east, alt, year)

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

