from typing import Callable
from math import *
from matrs import getActualMatrixes 
from numpy import arange

R = 6371.032      # —редний радиус «емли, [км]
a = 6378.245      # Ѕольшая полуось «емного элепсоида вращения, [км] Ёллипсоид расовского
b = 6356.863019   # ћалая полуось «емного элепсоида вращения, [км] Ёллипсоид расовского
PI_cache = [0] * 14

factorials_cache = [1] * 28
pr = {}
dels = {}
dr_cache = {}
b_cache = {}
def PI_odd_cached(n:int) -> int:
    """
     вычисление PI_odd с кешированием.
     результаты запиываются в массив, потом из него извелкаются
    """
    return PI_cache[n]

def factorial_cached(n:int) -> int:
    """
    вычисление факториала с кешированием
    """
    return factorials_cache[n]

def epsilon(i:int) -> "1 or 2":
    """
    функция расчета нормировачного множителя
    """
    if (i < 1):
        eps = 1
    else:
        eps = 2
    return eps
P_cache = []
dP_cache = []
dP2_cache = []

def initCache():
    """
    инициализация значений для кэша

    """
    global pr, dels, factorials_cache, b_cache, db_cache, P_cache, dP_cache, dP2_cache

    for n in range(0, 15):
        pr[n] = {}
        for m in range(0, 15):
            pr[n][m] = [0] * 7
            pr[n][m][0] = 1
            for i in range(1, 7):
                pr[n][m][i] = pr[n][m][i - 1] * (n - m - (2 * (i - 1))) * (n - m - (2 * i - 1))

    for n in range(0, 15):
        dels[n] = [0] * 7
        dels[n][0] = 1
        for i in range(1, 7):
           dels[n][i] = dels[n][i - 1] * (2 * i) * (2 * n - (2 * i - 1))

    factorials_cache[0] = 1
    for i in range(1, 28):
        factorials_cache[i] = factorials_cache[i - 1] * i

    PI_cache[0] = 1
    for i in range(1, 14):
        PI_cache[i] = PI_cache[i - 1] * (2 * i - 1)

    for n in range(1, 14):
        b_cache[n] = {}
        for m in range(0, n + 1):
            b_cache[n][m] = sqrt(epsilon(m) / (factorial_cached(n + m) * factorial_cached(n - m)))

    for n in range(1, 14):
        dr_cache[n] = {}
        for m in range(0, n + 1):
            dr_cache[n][m] = [pr[n][m][i] / dels[n][i] for i in range(7)]

    dP_cache = [0] * 15
    dP2_cache = [0] * 15
    P_cache = [0] * 15

    for n in range(1, 14):
        P_cache[n] = [0] * (n + 1)
        dP_cache[n] = [0] * (n + 1)
        dP2_cache[n] = [0] * (n + 1)
        for m in range(0, n + 1):
            P_cache[n][m] = {}
            dP_cache[n][m] = {}
            dP2_cache[n][m] = {}
            for teta in arange(-pi - 0.001, pi + 0.001, 0.001):
                cc = createCosCache(teta, -15, 15)
                P_cache[n][m][round(teta, 3)] = P(n, m, teta, cc, sin(teta))
                dP_cache[n][m][round(teta, 3)] = dPdtet(n, m, teta, cc, sin(teta))
                dP2_cache[n][m][round(teta, 3)] = d2Pdtet2(n, m, teta, cc, sin(teta))



def P_cached(n, m, teta):
    return P_cache[n][m][round(teta, 3)]


def dP_cached(n, m, teta):
    return dP_cache[n][m][round(teta, 3)]

def d2P_cached(n, m, teta):
    return dP2_cache[n][m][round(teta, 3)]

def P(n:int, m:int, teta:float, cos_cache:dict, sint:float) -> float:
    """
    функция расчета
    Нормированной по Шмидту присоединенной функции Лежандра Pnm(cos(teta))
    n, m - для Pnm, teta - для косинуса и синуса
     """

    dr_c = dr_cache
    s0 = dr_c[n][m][0] * cos_cache[n - m]#pow_cost0
    s1 = dr_c[n][m][1] * cos_cache[n - m - 2]#pow_cost2
    s2 = dr_c[n][m][2] * cos_cache[n - m - 4]#pow_cost4
    s3 = dr_c[n][m][3] * cos_cache[n - m - 6]#pow_cost6
    s4 = dr_c[n][m][4] * cos_cache[n - m - 8]#pow_cost8
    s5 = dr_c[n][m][5] * cos_cache[n - m - 10]#pow_cost10
    s6 = dr_c[n][m][6] * cos_cache[n - m - 12]#pow_cost12

    sum = (s0 - s1 + s2 - s3 + s4 - s5 + s6)

    return PI_odd_cached(n) * b_cache[n][m] * (sint ** m) * sum

def createCosCache(teta, minDeg, maxDeg):
    cost = cos(teta)
    res = {}
    res[minDeg] = cost ** minDeg
    for i in range(minDeg + 1, maxDeg + 1):
        res[i] = res[i - 1] * cost
    return res


def dPdtet(n:int, m:int, teta:float, cos_cache:dict, sint:float) -> float:
    """
    функция расчета производной
    Нормированной по Шмидту присоединенной функции Лежандра по тета
    dPnm(cos(teta))/dteta
    n, m - для Pnm, teta - для косинуса и синуса
    """
   
    cost = cos_cache[1]
   
 
    dr_c = dr_cache
    s0_0 = dr_c[n][m][0] * cos_cache[n - m]#pow_cost0
    s0_1 = dr_c[n][m][1] * cos_cache[n - m - 2]#pow_cost2
    s0_2 = dr_c[n][m][2] * cos_cache[n - m - 4]#pow_cost4
    s0_3 = dr_c[n][m][3] * cos_cache[n - m - 6]#pow_cost6
    s0_4 = dr_c[n][m][4] * cos_cache[n - m - 8]#pow_cost8
    s0_5 = dr_c[n][m][5] * cos_cache[n - m - 10]#pow_cost10
    s0_6 = dr_c[n][m][6] * cos_cache[n - m - 12]#pow_cost12
    
    s1_0 = dr_c[n][m][0] * (n - m) * cos_cache[n - m - 1]#pow_cost1
    s1_1 = dr_c[n][m][1] * (n - m - 2) * cos_cache[n - m - 3]#pow_cost3
    s1_2 = dr_c[n][m][2] * (n - m - 4) * cos_cache[n - m - 5]#pow_cost5
    s1_3 = dr_c[n][m][3] * (n - m - 6) * cos_cache[n - m - 7]#pow_cost7
    s1_4 = dr_c[n][m][4] * (n - m - 8) * cos_cache[n - m - 9]#pow_cost9
    s1_5 = dr_c[n][m][5] * (n - m - 10) * cos_cache[n - m - 11]#pow_cost11
    s1_6 = dr_c[n][m][6] * (n - m - 12) * cos_cache[n - m - 13]#pow_cost13

    sum1 = (s0_0 - s0_1 + s0_2 - s0_3 + s0_4 - s0_5 + s0_6)
    sum2 = (s1_0 - s1_1 + s1_2 - s1_3 + s1_4 - s1_5 + s1_6) * (-sint)
    slag1 = m * cost * sum1
    slag2 = sint * sum2
    return PI_odd_cached(n) * b_cache[n][m] * (sint ** (m - 1)) * (slag1 + slag2)

def Uf(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    Функция расчета потенциала индукции геомагнитного поля
    внутреземных источников U(r,lamda,tetta)
    """
    N = len(F_g)
    sum_n = 0  

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0.0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 1)) * sum_m
    potential = R * sum_n
    return potential

def Bxf(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля XТ
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0.0  

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * dP_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return potential

def Byf(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля  YТ
    На основе производной dU(r, lamda, teta)/dteta
    """
   # global R
    N = len(F_g)
    sum_n = 0   # суммирование п,

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = m * (F_g[n][m] * sin(m * lamda) - F_h[n][m] * cos(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
    potential = sum_n / sin(teta)
    return potential

def Bzf(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля Z`
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + (n + 1) * ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return -potential

def getCoordinates(north:float, east:float, alt:float) -> "[lamda, teta, r, fi, fi_sh]":
    """
    ѕреобразование географических координат
    в сферические
    јргументы:
    north - широта(северная+, южная -)
    east - долгота(восточная +, западная -)
    alt - высота над уровнем моря
    возвращает [lamda, teta, r]

    """

    lamda = radians(east)
    fi = radians(north)
    a2 = a ** 2  # сокращения чтобы не писать несколько раз
    b2 = b ** 2
    cosfi2 = (cos(fi) ** 2)
    sinfi2 = (sin(fi) ** 2)
    tmp = sqrt(a2 * cosfi2 + b2 * sinfi2)

    # Широта в сферических координатах
    fi_sh = atan(((b2 + alt * tmp) / (a2 + alt * tmp)) * tan(fi))
    # ѕолярный угол
    teta = (pi / 2) - fi_sh
    # поправка на геоид (полярное сжатие «емли)
    r = sqrt((alt ** 2) + 2 * alt * tmp + ((a ** 4) * cosfi2 + (b ** 4) * sinfi2) / (tmp ** 2))
    return [lamda, teta, r, fi, fi_sh]


def getCoordinates2(north:float, east:float):
    """
    ѕреобразование географических координат
    в сферические
    јргументы:
    north - широта(северная+, южная -)
    east - долгота(восточная +, западная -)
    alt - высота над уровнем моря  = 0
    возвращает [lamda, teta, r]

    """
    global a, b

    lamda = radians(east)
    dlamdadeast = pi / 180
    dlamdadnort = 0
    fi = radians(north)
    dfidnort = pi / 180
    dfideast = 0
    a2 = a ** 2  # сокращения чтобы не писать несколько раз
    b2 = b ** 2
    cosfi2 = (cos(fi) ** 2)
    sinfi2 = (sin(fi) ** 2)
    # Широта в сферических координатах
    fi_sh = atan((b2 / a2) * tan(fi))
    dfi_shdnort = 1 / (1 + ((b2 / a2) * tan(fi)) ** 2) * (b2 / a2 * (1 / (cos(fi) ** 2)) * dfidnort)
    dfi_shdeast = 0
    # ѕолярный угол
    teta = (pi / 2) - fi_sh
    dtetadnort = -dfi_shdnort
    dtetadeast = 0

    a4 = a ** 4  # сокращения чтобы не писать несколько раз
    b4 = b ** 4 

    dcos2 = 2 * cos(fi) * (-sin(fi)) * dfidnort
    dsin2 = 2 * sin(fi) * cos(fi) * dfidnort

    tmp = sqrt(a2 * cosfi2 + b2 * sinfi2)

    dtmp = 1 / (2 * tmp) * (a2 * dcos2 + b2 * dsin2)


    ch = (a4 * cosfi2 + b4 * sinfi2)
    zn = (tmp ** 2)

    dch = (a4 * dcos2 + b4 * dsin2)
    dzn = 2 * tmp * dtmp

    r = sqrt(ch / zn)

    drdnort = 1 / (2 * r) * ((dch * zn - dzn * ch) / (zn ** 2))

    return [lamda, dlamdadnort, dlamdadeast, teta, dtetadnort, dtetadeast, r, drdnort, fi, dfidnort, dfideast, fi_sh, dfi_shdnort, dfi_shdeast]

def d2Pdtet2(n:int, m:int, teta:float, cos_cache:dict, sint:float) -> float:
    """функция расчета производной
    Нормированной по Шмидту присоединенной функции Лежандра по тета
    dPnm(cos(teta))/dteta
    n, m - для Pnm, teta - для косинуса и синуса
    """

    cost = cos(teta)


    s0_0 = dr_cache[n][m][0] * cos_cache[n - m]
    s0_1 = dr_cache[n][m][1] * cos_cache[n - m - 2]
    s0_2 = dr_cache[n][m][2] * cos_cache[n - m - 4]
    s0_3 = dr_cache[n][m][3] * cos_cache[n - m - 6]
    s0_4 = dr_cache[n][m][4] * cos_cache[n - m - 8]
    s0_5 = dr_cache[n][m][5] * cos_cache[n - m - 10]
    s0_6 = dr_cache[n][m][6] * cos_cache[n - m - 12]
    
    s1_0 = dr_cache[n][m][0] * (n - m) * cos_cache[n - m - 1]
    s1_1 = dr_cache[n][m][1] * (n - m - 2) * cos_cache[n - m - 3]
    s1_2 = dr_cache[n][m][2] * (n - m - 4) * cos_cache[n - m - 5]
    s1_3 = dr_cache[n][m][3] * (n - m - 6) * cos_cache[n - m - 7]
    s1_4 = dr_cache[n][m][4] * (n - m - 8) * cos_cache[n - m - 9]
    s1_5 = dr_cache[n][m][5] * (n - m - 10) * cos_cache[n - m - 11]
    s1_6 = dr_cache[n][m][6] * (n - m - 12) * cos_cache[n - m - 13]

    s3_0 = dr_cache[n][m][0] * (n - m) * (((n - m - 1) * cos_cache[n - m - 2] * (sint ** 2)) + (cos_cache[n - m - 1] * (-cost)))
    s3_1 = dr_cache[n][m][1] * (n - m - 2) * (((n - m - 3) * cos_cache[n - m - 4] * (sint ** 2)) + (cos_cache[n - m - 3] * (-cost)))
    s3_2 = dr_cache[n][m][2] * (n - m - 4) * (((n - m - 5) * cos_cache[n - m - 6] * (sint ** 2)) + (cos_cache[n - m - 5] * (-cost)))
    s3_3 = dr_cache[n][m][3] * (n - m - 6) * (((n - m - 7) * cos_cache[n - m - 8] * (sint ** 2)) + (cos_cache[n - m - 7] * (-cost)))
    s3_4 = dr_cache[n][m][4] * (n - m - 8) * (((n - m - 9) * cos_cache[n - m - 10] * (sint ** 2)) + (cos_cache[n - m - 9] * (-cost)))
    s3_5 = dr_cache[n][m][5] * (n - m - 10) * (((n - m - 11) * cos_cache[n - m - 12] * (sint ** 2)) + (cos_cache[n - m - 11] * (-cost)))
    s3_6 = dr_cache[n][m][6] * (n - m - 12) * (((n - m - 13) * cos_cache[n - m - 14] * (sint ** 2)) + (cos_cache[n - m - 13] * (-cost)))
    

    sum1 = (s0_0 - s0_1 + s0_2 - s0_3 + s0_4 - s0_5 + s0_6)
    sum2 = (s1_0 - s1_1 + s1_2 - s1_3 + s1_4 - s1_5 + s1_6) * (-sint)
    sum3 = (s3_0 - s3_1 + s3_2 - s3_3 + s3_4 - s3_5 + s3_6)
    mnoj = PI_odd_cached(n) * b_cache[n][m]  

    slag11 = m * (m - 1) * (sint ** (m - 2)) * (cost ** 2) * sum1
    slag12 = -m * (sint ** m) * sum1
    slag13 = m * (sint ** (m - 1)) * cost * sum2

    slag21 = m * (sint ** (m - 1)) * cost * sum2 
    slag22 = (sint ** m) * sum3

    return mnoj * (slag11 + slag12 + slag13 + slag21 + slag22)

########################################

#####################################
#    BX, BY, BZ (nort, east)
####################################
def BXf(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, teta, r, fi, fi_sh] = getCoordinates(n, e, 0) 
   try:
       bx = Bxf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bx = 0
   try:
       bz = Bzf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bz = 0
   Bx = bx * cos(fi - fi_sh) + bz * sin(fi - fi_sh) 
   return Bx

def BYf(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, teta, r, fi, fi_sh] = getCoordinates(n, e, 0) 
   try:
       by = Byf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       by = 0
   return   by


def BZf(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, teta, r, fi, fi_sh] = getCoordinates(n, e, 0) 
   try:
       bx = Bxf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bx = 0
   try:
       bz = Bzf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bz = 0
   Bz = bz * cos(fi - fi_sh) - bx * sin(fi - fi_sh) 
   return Bz

def Bf(n, e, F_g, F_h):
    bx = BXf(n, e, F_g, F_h)
    by = BYf(n, e, F_g, F_h)
    bz = BZf(n, e, F_g, F_h)
    return sqrt(bx * bx + by * by + bz * bz)

#############################################

############################################
#    dBXdR, dBXdL, dBXdT
#############################################
def dBXfdT(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля XТ
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  # суммирование п,

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * d2P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return potential

def dBXfdL(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля XТ
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  # суммирование п,

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = m * (-F_g[n][m] * sin(m * lamda) + F_h[n][m] * cos(m * lamda))
            half_REZ = tmp * dP_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return potential

def dBXfdR(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля XТ
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  # суммирование п,

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * dP_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + sum_m * (n + 2) * R * ((R / r) ** (n + 1)) * (-1 / r ** 2)
    potential = sum_n
    return potential

##########################################

##########################################
#  dBZdL, dBZdR, dBXdT
##########################################
def dBZfdT(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля Z`
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  # суммирование п,

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * dP_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + (n + 1) * ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return -potential

def dBZfdL(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля Z`
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  # суммирование п,

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = m * (-F_g[n][m] * sin(m * lamda) + F_h[n][m] * cos(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + (n + 1) * ((R / r) ** (n + 2)) * sum_m
    potential = sum_n
    return -potential

def dBZfdR(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля Z`
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  
    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n - (n + 1) * sum_m * (n + 2) * R * ((R / r) ** (n + 1)) * (1 / r ** 2)  
    potential = sum_n
    return -potential

##########################################

#########################################
#   dBYdR, dBYdL, dBYdL
########################################
def dBYfdR(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля  YТ
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0   

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = m * (F_g[n][m] * sin(m * lamda) - F_h[n][m] * cos(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n - (n + 2) * R * ((R / r) ** (n + 1)) * (1 / r ** 2) * sum_m 
    potential = sum_n / sin(teta)
    return potential

def dBYfdL(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля  YТ
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0  

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = m * m * (F_g[n][m] * cos(m * lamda) + F_h[n][m] * sin(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
    potential = sum_n / sin(teta)
    return potential

def dBYfdT(r:float, lamda:float, teta:float, F_g:list, F_h:list) -> float:
    """
    функция расчёта составляющей вектора индукции главного поля  YТ
    На основе производной dU(r, lamda, teta)/dteta
    """
    N = len(F_g)
    sum_n = 0 
    dsum_n = 0

    for n in range(1, N):  # N - максимальная степень норм.  по Шмидту присоединенных функций Лежандра
        sum_m = 0
        dsumM = 0
        for m in range(0, n + 1):  # суммирование по m
            if F_g[n][m] == 0 and F_h[n][m] == 0:
                continue
            tmp = m * (F_g[n][m] * sin(m * lamda) - F_h[n][m] * cos(m * lamda))
            half_REZ = tmp * P_cached(n, m, teta) 
            sum_m = sum_m + half_REZ
            dsumM+= tmp * dP_cached(n, m, teta) 
        sum_n = sum_n + ((R / r) ** (n + 2)) * sum_m
        dsum_n+= ((R / r) ** (n + 2)) * dsumM
    potential = (dsum_n * sin(teta) - cos(teta) * sum_n) / (sin(teta) * sin(teta))   
    return potential

#########################################


#########################################
#  dBXdN, dBXdE
########################################
def dBXfdN(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, _, _, teta, dtetadnort, _, r, drdnort, fi, dfidnort, _, fi_sh, dfi_shdnort, _] = getCoordinates2(n, e) 

   try:
       bx = Bxf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bx = 0

   try:
       bz = Bzf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bz = 0
  
   try:
       dbxdtet = dBXfdT(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbxdtet = 0

   try:
       dbxdr = dBXfdR(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbxdr = 0
   try:
       dbzdteta = dBZfdT(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbzdteta = 0

   try:
       dbzdr = dBZfdR(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbzdr = 0


   dbxdnort = dbxdtet * dtetadnort + dbxdr * drdnort
   dbzdnort = dbzdteta * dtetadnort + dbzdr * drdnort

   dBXdnort = dbxdnort * cos(fi - fi_sh) + bx * (-sin(fi - fi_sh) * (dfidnort - dfi_shdnort)) + dbzdnort * sin(fi - fi_sh) + bz * (cos(fi - fi_sh) * (dfidnort - dfi_shdnort))

   return dBXdnort


def dBXfdE(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, _, dlamdadeast, teta, _, _, r,_, fi, _, _, fi_sh, _, _] = getCoordinates2(n, e) 

   try:
       dbxdlamda = dBXfdL(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbxdlamda = 0
   try:
       dbzdlamda = dBZfdL(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbzdlamda = 0
   dbxdeast = dbxdlamda * dlamdadeast
   dbzdeast = dbzdlamda * dlamdadeast 

   dBXdeast = dbxdeast * cos(fi - fi_sh) + dbzdeast * sin(fi - fi_sh) 
   return dBXdeast

################################

###############################
#  dBYdN, dBYdE
###############################
def dBYfdN(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, _, _, teta, dtetadnort, _, r, drdnort, fi, dfidnort, _, fi_sh, dfi_shdnort, _] = getCoordinates2(n, e)

   dbdn = dBYfdR(r, lamda, teta, F_g, F_h) * drdnort + dBYfdT(r, lamda, teta, F_g, F_h) * dtetadnort

   return dbdn

def dBYfdE(n:float, e:float, F_g:list, F_h:list) -> float:
    [lamda, _, dlamdadeast, teta, _, _, r,_, fi, _, _, fi_sh, _, _] = getCoordinates2(n, e) 
    dbde = dBYfdL(r, lamda, teta, F_g, F_h) * dlamdadeast
    return dbde

###################################

##################################
#    dBZdN, dBZdE
##################################
def dBZfdN(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, _, _, teta, dtetadnort, _, r, drdnort, fi, dfidnort, _, fi_sh, dfi_shdnort, _] = getCoordinates2(n, e) 

   try:
       bx = Bxf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bx = 0

   try:
       bz = Bzf(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       bz = 0
  
   try:
       dbxdtet = dBXfdT(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbxdtet = 0

   try:
       dbxdr = dBXfdR(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbxdr = 0
   try:
       dbzdteta = dBZfdT(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbzdteta = 0

   try:
       dbzdr = dBZfdR(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbzdr = 0


   dbxdnort = dbxdtet * dtetadnort + dbxdr * drdnort
   dbzdnort = dbzdteta * dtetadnort + dbzdr * drdnort

   dBXdnort = dbzdnort * cos(fi - fi_sh) + bz * (-sin(fi - fi_sh) * (dfidnort - dfi_shdnort)) + dbxdnort * sin(fi - fi_sh) + bx * (cos(fi - fi_sh) * (dfidnort - dfi_shdnort))

   return dBXdnort

def dBZfdE(n:float, e:float, F_g:list, F_h:list) -> float:
   [lamda, _, dlamdadeast, teta, _, _, r,_, fi, _, _, fi_sh, _, _] = getCoordinates2(n, e) 

   try:
       dbxdlamda = dBXfdL(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbxdlamda = 0
   try:
       dbzdlamda = dBZfdL(r, lamda, teta, F_g, F_h)
   except ZeroDivisionError:
       dbzdlamda = 0
   dbxdeast = dbxdlamda * dlamdadeast 
   dbzdeast = dbzdlamda * dlamdadeast 

   dBXdeast = dbzdeast * cos(fi - fi_sh) - dbxdeast * sin(fi - fi_sh) 
   return dBXdeast


def dBfdN(n, e, F_g, F_h):
    bx = BXf(n, e, F_g, F_h)
    by = BYf(n, e, F_g, F_h)
    bz = BZf(n, e, F_g, F_h)

    dBX = dBXfdN(n, e, F_g, F_h)
    dBY = dBYfdN(n, e, F_g, F_h)
    dBZ = dBZfdN(n, e, F_g, F_h)

    dB = 1 / (2 * sqrt(bx ** 2 + by ** 2 + bz ** 2)) * (2 * bx * dBX + 2 * by * dBY + 2 * bz * dBZ)
    return dB

def dBfdE(n, e, F_g, F_h):
    bx = BXf(n, e, F_g, F_h)
    by = BYf(n, e, F_g, F_h)
    bz = BZf(n, e, F_g, F_h)

    dBX = dBXfdE(n, e, F_g, F_h)
    dBY = dBYfdE(n, e, F_g, F_h)
    dBZ = dBZfdE(n, e, F_g, F_h)

    dB = 1 / (2 * sqrt(bx ** 2 + by ** 2 + bz ** 2)) * (2 * bx * dBX + 2 * by * dBY + 2 * bz * dBZ)
    return dB
#################################


##################################
#     gradients
##################################
def BXgradient(n:float, e:float, F_g:list, F_h:list) -> tuple:
    return (dBXfdN(n, e, F_g, F_h), dBXfdE(n, e, F_g, F_h))

def BYgradient(n:float, e:float, F_g:list, F_h:list) -> tuple:
    return (dBYfdN(n, e, F_g, F_h), dBYfdE(n, e, F_g, F_h))


def BZgradient(n:float, e:float, F_g:list, F_h:list) -> tuple:
    return (dBZfdN(n, e, F_g, F_h), dBZfdE(n, e, F_g, F_h))

def Bgradient(n, e, F_g, F_h):
    return (dBfdN(n, e, F_g, F_h), dBfdE(n, e, F_g, F_h))

########################################
######################################

initCache()
print('cache loaded')
