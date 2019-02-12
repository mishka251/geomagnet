from math import pi
from datetime import *
import json
from math import *
import numpy

class params:
    """
    Класс для параметров из гет запроса и вычислеямых на их основеи некоторые константы

    получаемые в ГЕТ:
    nort - широта
    eas - долгота
    al - высота
    year - текущий год
    ut - ???

    вычислеямые:
    lamda  ??
    fi      ??
    quitfi_sh широта в сферических координатах
    teta   - полярный угол
    r  -  поправка на геоид (полярное сжатие Земли)

    константы:
    N  - кол-во строк в матрицах(длина апроксимируещего ряда (максимальная степень сферических
                           #гармоник))
    n_p   - концентрация протонов в солнечном ветре [м^-3]
    v     - скорость солнечного ветра
    """
    north = 0# = _GET['lat'];
    east = 0 #= _GET['lng'];
    alt = 0#= _GET['alt'];
    year = 0#= _GET['data'];
    UT = 0

    lamda = 0#= east * (pi() / 180);
    fi = 0#= north * (pi() / 180);
    quitfi_sh = 0 #//широта в сферических координатах
    teta = 0 # //ѕол¤рный угол
    r = 0#//поправка на геоид (пол¤рное сжатие «емли)
    
    N = 0
    n_p = 3800000
    v = 415100


    def initInput(nort, eas, al, yea, ut):
        """
        инициализация переменных(из ГЕТ и на их основе)
        nort - широта
        eas - долгота
        al - высота
        year - текущий год
        ut - ???
        """
        params.north = nort
        params.east = eas
        params.alt = al
        params.year = yea
        params.UT = ut

        params.lamda = params.east * (pi / 180)
        params.fi = params.north * (pi / 180)
        params.fi_sh = atan(((pow(b, 2) + params.alt * sqrt(pow(a, 2) * pow((cos(params.fi)), 2) + pow(b, 2) * pow((sin(params.fi)), 2))) / (pow(a, 2) + params.alt * sqrt(pow(a, 2) * pow(cos(params.fi), 2) + pow(b, 2) * pow((sin(params.fi)), 2)))) * tan(params.fi))
        params.teta = (pi / 2) - params.fi_sh 
        params.r = sqrt(pow(params.alt, 2) + 2 * params.alt * sqrt(pow(a, 2) * pow((cos(params.fi)), 2) + pow(b, 2) * pow((sin(params.fi)), 2)) + ((pow(a, 4) * pow((cos(params.fi)), 2) + pow(b, 4) * pow((sin(params.fi)), 2)) / (pow(a, 2) * pow((cos(params.fi)), 2) + pow(b, 2) * pow((sin(params.fi)), 2))))


#//константы земли
R = 6371.032   #//Средний радиус Земли, [км]
a = 6378.245 #//Большач полуось земного элепсоида вращения, [км] // Ёллипсоид Красовского
b = 6356.863019 #//Малая полуось Земного элипсоида вращения, [км] // Ёллипсоид Красовского

Age = 2015.0    #//Эпоха
#//***матрицы сферических гармонических коэффициентов (дл¤ эпохи 2015г.)
IGRF_g = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-29438.5, -1501.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-2445.3, 3012.5, 1676.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1351.1, -2352.3, 1225.6, 581.9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [907.2, 813.7, 120.3, -335.0, 70.3, 0, 0, 0, 0, 0, 0, 0, 0],
    [-232.6, 360.1, 192.4, -141.0, -157.4, 4.3, 0, 0, 0, 0, 0, 0, 0],
    [69.5, 67.4, 72.8, -129.8, -29.0, 13.2, -70.9, 0, 0, 0, 0, 0, 0],
    [81.6, -76.1, -6.8, 51.9, 15.0, 9.3, -2.8, 6.7, 0, 0, 0, 0, 0],
    [24.0, 8.6, -16.9, -3.2, -20.6, 13.3, 11.7, -16.0, -2.0, 0, 0, 0, 0],
    [5.4, 8.8, 3.1, -3.1, 0.6, -13.3, -0.1, 8.7, -9.1, -10.5, 0, 0, 0],
    [-1.9, -6.5, 0.2, 0.6, -0.6, 1.7, -0.7, 2.1, 2.3, -1.8, -3.6, 0, 0],
    [3.1, -1.5, -2.3, 2.1, -0.9, 0.6, -0.7, 0.2, 1.7, -0.2, 0.4, 3.5, 0],
    [-2.0, -0.3, 0.4, 1.3, -0.9, 0.9, 0.1, 0.5, -0.4, -0.4, 0.2, -0.9, 0]]

IGRF_h = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4796.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -2845.6, -642.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -115.3, 245.0, -538.3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 283.4, -188.6, 180.9, -329.5, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 47.4, 196.9, -119.4, 16.1, 100.1, 0, 0, 0, 0, 0, 0, 0],
    [0, -20.7, 33.2, 58.8, -66.5, 7.3, 62.5, 0, 0, 0, 0, 0, 0],
    [0, -54.1, -19.4, 5.6, 24.4, 3.3, -27.5, -2.3, 0, 0, 0, 0, 0],
    [0, 10.2, -18.1, 13.2, -14.6, 16.2, 5.7, -9.1, 2.2, 0, 0, 0, 0],
    [0, -21.6, 10.8, 11.7, -6.8, -6.9, 7.8, 1.0, -3.9, 8.5, 0, 0, 0],
    [0, 3.3, -0.3, 4.6, 4.4, -7.9, -0.6, -4.1, -2.8, -1.1, -8.7, 0, 0],
    [0, -0.1, 2.1, -0.7, -1.1, 0.7, -0.2, -2.1, -1.5, -2.5, -2.0, -2.3, 0],
    [0, -1.0, 0.5, 1.8, -2.2, 0.3, 0.7, -0.1, 0.3, 0.2, -0.9, -0.2, 0.7]]

SV_g = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [10.7, 17.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-8.6, -3.3, 2.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3.1, -6.2, -0.4, -10.4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-0.4, 0.8, -9.2, 4.0, -4.2, 0, 0, 0, 0, 0, 0, 0, 0],
    [-0.2, 0.1, -1.4, 0.0, 1.3, 3.8, 0, 0, 0, 0, 0, 0, 0],
    [-0.5, -0.2, -0.6, 2.4, -1.1, 0.3, 1.5, 0, 0, 0, 0, 0, 0],
    [0.2, -0.2, -0.4, 1.3, 0.2, -0.4, -0.9, 0.3, 0, 0, 0, 0, 0],
    [0.0, 0.1, -0.5, 0.5, -0.2, 0.4, 0.2, -0.4, 0.3, 0, 0, 0, 0],
    [0.0, -0.1, -0.1, 0.4, -0.5, -0.1, 0.1, 0.0, -0.2, -0.1, 0, 0, 0],
    [0.0, 0.0, -0.1, 0.3, -0.1, -0.1, -0.1, 0.0, -0.2, -0.1, -0.2, 0, 0],
    [0.0, 0.0, -0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1, -0.1, 0],
    [0.1, 0.0, 0.0, 0.1, -0.1, 0.0, 0.1, 0.0, 0, 0, 0, 0, 0]]

SV_h = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -26.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -27.1, -13.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8.4, -0.4, 2.3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -0.6, 5.3, 3.0, -5.3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0.4, 1.6, -1.1, 3.3, 0.1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0.0, -2.2, -0.7, 0.1, 1.0, 1.3, 0, 0, 0, 0, 0, 0],
    [0, 0.7, 0.5, -0.2, -0.1, -0.7, 0.1, 0.1, 0, 0, 0, 0, 0],
    [0, -0.3, 0.3, 0.3, 0.6, -0.1, -0.2, 0.3, 0.0, 0, 0, 0, 0],
    [0, -0.2, -0.1, -0.2, 0.1, 0.1, 0.0, -0.2, 0.4, 0.3, 0, 0, 0],
    [0, 0.1, -0.1, 0.0, 0.0, -0.2, 0.1, -0.1, -0.2, 0.1, -0.1, 0, 0],
    [0, 0, 0.1, 0.0, 0.1, 0.0, 0.0, 0.1, 0.0, -0.1, 0.0, -0.1, 0],
    [0, 0, 0, -0.1, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0]]


class mats:
    """
    для хранения актуальных матриц, т.к. они меняются во время работы
    """
    F_IGRF_g = [0]
    F_IGRF_h = [0]

    def actualize(year, Age, N):
        """
        Актуализация матриц сферических гармонических коэффициентов
        параметры:
        year - текущий год
        Age - эпоха(прошлое актуальное время)
        N - размеры матриц
        """
        mats.F_IGRF_g = [0] * N
        mats.F_IGRF_h = [0] * N
        for i in range(N):
            mats.F_IGRF_g[i] = [0] * N
            mats.F_IGRF_h[i] = [0] * N
            for j in range(N):
                mats.F_IGRF_g[i][j] = IGRF_g[i][j] + (SV_g[i][j]) * (year - Age)
                mats.F_IGRF_h[i][j] = IGRF_h[i][j] + (SV_h[i][j]) * (year - Age)


def PI_odd(i):
     """Функция расчета произведения нечетных составляющих ряда сферических гармоник 
     """
     rez = 1
     for k in range(1, i + 1):
        rez1 = 2 * k - 1
        rez = rez * rez1
    
     return rez


def epsilon(i):
    """ Функция расчета нормировачного множителя """
    if (i < 1):
        eps = 1
    else:
        eps = 2
    return eps


def U(r, lamda, teta):
    """

    """
    N = params.N
    F_IGRF_g = mats.F_IGRF_g
    F_IGRF_h = mats.F_IGRF_h
    sum_n = 0#; // суммирование п,
    for n in range(1, N):# N - максимальная степень нормированных по Шмидту присоединенных функций
                         # Лежандра
                                                  
        sum_m = 0       
        for m in range(0, n + 1):# суммирование по m

            #питон не любит переносы, поэтому в одну строку
            half_REZ = R * (F_IGRF_g[n][m] * cos(m * lamda) + F_IGRF_h[n][m] * sin(m * lamda)) * pow((R / r), (n + 1)) * PI_odd(n) * sqrt(epsilon(m) / (factorial(n + m) * factorial(n - m))) * pow((sin(teta)), m) * (pow(cos(teta), (n - m)) - ((n - m) * (n - m - 1) / (2 * (2 * n - 1))) * pow((cos(teta)), (n - m - 2)) + ((n - m) * (n - m - 1) * (n - m - 2) * (n - m - 3) / (2 * 4 * (2 * n - 1) * (2 * n - 3))) * pow((cos(teta)), (n - m - 4)) - ((n - m) * (n - m - 1) * (n - m - 2) * (n - m - 3) * (n - m - 4) * (n - m - 5) / (2 * 4 * 6 * (2 * n - 1) * (2 * n - 3) * (2 * n - 5))) * pow((cos(teta)), (n - m - 6)) + ((n - m) * (n - m - 1) * (n - m - 2) * (n - m - 3) * (n - m - 4) * (n - m - 5) * (n - m - 6) * (n - m - 7) / (2 * 4 * 6 * 8 * (2 * n - 1) * (2 * n - 3) * (2 * n - 5) * (2 * n - 7))) * pow((cos(teta)), (n - m - 8)) - ((n - m) * (n - m - 1) * (n - m - 2) * (n - m - 3) * (n - m - 4) * (n - m - 5) * (n - m - 6) * (n - m - 7) * (n - m - 8) * (n - m - 9) / (2 * 4 * 6 * 8 * 10 * (2 * n - 1) * (2 * n - 3) * (2 * n - 5) * (2 * n - 7) * (2 * n - 9))) * pow((cos(teta)), (n - m - 10)) + ((n - m) * (n - m - 1) * (n - m - 2) * (n - m - 3) * (n - m - 4) * (n - m - 5) * (n - m - 6) * (n - m - 7) * (n - m - 8) * (n - m - 9) * (n - m - 10) * (n - m - 11) / (2 * 4 * 6 * 8 * 10 * 12 * (2 * n - 1) * (2 * n - 3) * (2 * n - 5) * (2 * n - 7) * (2 * n - 9) * (2 * n - 11))) * pow(cos(teta), (n - m - 12)))
            sum_m = sum_m + half_REZ
        
        sum_n = sum_n + sum_m
    
    potential = sum_n
    return potential


def dydx(x0, y):
    """
    производная от функции y(x) в точке x0
    """

#////********************ИСХОДНЫЕ ДАННЫЕ********************
#//***********Без необходимости менять не нужно***********
    h0 = 1                 #   // оптимальный шаг дискретизации (изначально не известен)
    h = 0                   #  // задаемся изначальным шагом дискретизации = 1 (пока он
                            #  равен нулю - издержки алгоритма, позже примет
                                     #  значение 1)
    e = 1 * pow(10, (-9))    #   // задаемся погрешностью округления с точностью до 9-го знака после
                             #   запятой (количество знаков после запятой
                                                      #   значения аргумента
                                                                               #   Y(X))
#//********************************************************

    while ((abs(h - h0)) > 0.000000001):
        h = h0

        X = [0] * 6
        Y = [0] * 6

        for i in range(len(X)):
            X[i] = x0 + i * h


        for i in range(len(Y)):
            Y[i] = y(X[i])

        deltaY1 = Y[1] - Y[0]
        deltaY2 = Y[2] - Y[1] - deltaY1
        deltaY3 = ((Y[3] - Y[2]) - (Y[2] - Y[1])) - deltaY2
        deltaY4 = (((Y[4] - Y[3]) - (Y[3] - Y[2])) - ((Y[2] - Y[1]) - (Y[1] - Y[0]))) - deltaY3
        deltaY5 = (((Y[5] - Y[4]) - (Y[4] - (Y[3]))) - ((Y[3] - Y[2]) - (Y[2] - Y[1]))) - deltaY4

        d2y = (1 / pow(h, 2)) * (deltaY2 - deltaY3 + (11 / 12) * deltaY4 - (5 / 6) * deltaY5)

        h0 = sqrt(4 * (abs((e * Y[0]) / (d2y))))
    
    h = h0
    dy = (1 / h) * (deltaY1 - (1 / 2) * deltaY2 + (1 / 3) * deltaY3)
    return dy


def dUdlamda(r, lamda0, teta):
    """
    функция расчета производной dU/dlamda
    в точке r, lamda0, teta
    """
    return dydx(lamda0, lambda x : U(r, x, teta))

def dUdteta(r, lamda,  teta0):
	"""
	функция расчета производной dU/dteta
	в точке r, lamda, teta0
	"""
	return dydx(teta0, lambda x : U(r,lamda, x))

def dUdr(r0, lamda, teta):
    """
    функция расчета производной dU/dr
    в точке r0, lamda, teta
    """
    return dydx(r0,  lambda x : U(x, lamda, teta))


def calculateGEO(north, east, alt, a, b):
    """
    перевод в геоцентрическую систему

    Входные параметры:
    north - широта
    alt - долгота
    alt - высота
    a - Большач полуось земного элепсоида вращения,
    b -  Малая полуось Земного элипсоида вращения

    Возвращает
    [xGEO, yGEO, zGEO] - координаты в геоцентрической системе
    """
    #//координаты в географической системе (GEO), переведенные в радианы
    latGEO = north * (pi / 180)
    longGEO = east * (pi / 180)
    altGEO = alt

    rE = sqrt(pow(altGEO, 2) + 2 * altGEO * sqrt(pow(a, 2) * pow(cos(latGEO), 2) + pow(b, 2) * pow(sin(latGEO), 2)) + (pow(a, 4) * pow(cos(latGEO), 2) + pow(b, 4) * pow(sin(latGEO), 2)) / (pow(a, 2) * pow(cos(latGEO), 2) + pow(b, 2) * pow(sin(latGEO), 2)))

    #//перевод в геоцентрическую систему
    xGEO = rE * cos(latGEO) * cos(longGEO)
    yGEO = rE * cos(latGEO) * sin(longGEO)
    zGEO = rE * sin(latGEO)

#//матрица координат GEO
    return [xGEO, yGEO, zGEO]



def coords(UT, n_p, v, Ynum, teta, lamda, alt):
    """
    входные  
    n_p - концентрация протонов в солнечном ветре [м^-3]
    Ynum - порядковый номер дня в году [1..365]  
    v - скорость солнечного ветра    
    teta, lamda, alt - географические координаты

    возвращает X, Y, Z - Солнечно-магнитосферные координаты в единицах [R - радиус Земли]

    промежуточные

    psi - угол наклона геомагнитного диполя к плоскости ортогональной линии  Земля-Солнце, [град]
    B2 - вектор индукции магнитного поля магнитосферных токов, вычисляемый солнечно-магнитосферной системе координат
    n_alpha - концентрация альфа-частиц в солнечном ветре [м^-3]
    n_m - концентрация малых ионных компонентов [м^-3]
    """

    n_alpha = 0.06 * n_p #// Расчет концентрации альфа-частиц в солнечном ветре [м^-3]
    n_m = 0.001 * n_p   # // Расчет концентрации малых ионных компонентов [м^-3]

    #//---Перевод вектора индукции магнитного поля из географическй системы
    #координат в солнечно-магнитосферную---
    alpha1 = (pi / 180) * 11.43 #// угол между осью вращения Земли и осью геомагнитного диполя
    alpha2 = (pi / 180) * 23.5  #// угол наклона плоскости экватора к плоскости эклиптики
    U0 = 12 #//часов
    K = 15 #// градусов/час

    # угол между линией Земля-Солнце и проекцией оси вращения Земли на
    # плоскость эклиптики, [град]
    fi_SE = (pi / 180) * (360 * (172 - Ynum) / 365)

    #// угол между плоскостью полуночного мередиана и мередианальной
    #плоскостью, содержащей северный магнитный полюс
    fi_m = (pi / 180) * (K * UT - 69) 
 
    beta0 = asin(sin(alpha2) * cos(fi_SE)) #// Склонение Солнца

   # угол наклона геомагниного диполя к плоскости ортогональной линии
   # Земля-Солнце
    psi = asin(-sin(beta0) * cos(alpha1) + cos(beta0) * sin(alpha1) * cos(fi_m)) 

    beta1 = (K * (UT - U0)) * pi / 180 #// западная долгота полуденного мередиана

     #//угол между полуденным географическим меридианом и плоскостью y = 0 в
     #солнечно магнитосферных координатах
    beta2 = acos((cos(alpha1) + sin(beta0) * sin(psi)) / cos(psi) * cos(beta0))
    
    #// Матрица поворота к солнечно-магнитосферным координатам
    T_array = [[cos(beta1) * cos(beta0), (-1) * sin(beta1) * cos(beta0), sin(beta0)],
        [sin(beta1) * cos(beta2) - cos(beta1) * sin(beta0) * sin(beta2), cos(beta1) * cos(beta2) + sin(beta1) * sin(beta0) * sin(beta2), cos(beta0) * sin(beta2)],  
        [(-1) * sin(beta1) * sin(beta2) - cos(beta1) * sin(beta0) * cos(beta2), (-1) * cos(beta1) * sin(beta2) + sin(beta1) * sin(beta0) * cos(beta2), cos(beta0) * cos(beta2)]]

    # // Матрица перевода из сферических в декартовы координаты
    S_array = [[sin(teta) * cos(lamda), cos(teta) * cos(lamda), (-1) * sin(lamda)],
        [sin(teta) * sin(lamda), cos(teta) * sin(lamda), cos(lamda)],                   
        [cos(teta), (-1) * sin(teta), 0]]


    Q_array = numpy.dot(T_array, S_array)#T*S

    spherCoord = [alt, teta, lamda]

    return numpy.dot(Q_array, spherCoord) #[X, Y, Z] = Q*spherCoord
    

def days_z(year, month, day):
    """
    Номер дня от начала года
    вход year - год, month - номер месяца, day - номер день в месяце
    """
    #               ян фе ма ап ма ию ию ав се ок но де
    day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0:
        day_in_month[1]+=1 #високосный год

    sum = 0
    for i in range(month - 1):
        sum+=day_in_month[i]
    sum+=day
    return sum

def rotate(year, Age, lamda, GEO):
    """
    Расчет MAG
    принимает 
    year - текущий год
    Age - начальная эпоха
    lamda  - угол ??
    GEO   - ??
    """
    #//Сферические гармонические коэффициенты для эпохи 2015-2020
    h11_igrf = 4797.1;
    g11_igrf = -1501;
    g10_igrf = -29442;

    g10_sv = 10.3;
    g11_sv = 18.1;
    h11_sv = -22.6;

    h11 = h11_igrf + h11_sv * (year - Age)
    g11 = g11_igrf + g11_sv * (year - Age)
    g10 = g10_igrf + g10_sv * (year - Age)
#//расчет углов поворота
    
#//угол поворотота вокруг оси Y
    lamda = atan(h11 / g11)
    n1 = (pi / 2)
    n2 = (g11 * cos(lamda) + h11 * sin(lamda))
    n3 = asin(n2 / (g10))
    fi = (n1 - n3) - (pi / 2)


  
    t5Y = [#//Поворотные матрицы 3x3
        [cos(fi), 0, sin(fi)],
        [0, 1, 0],
        [-sin(fi), 0, cos(fi)]]

    t5Z = [[cos(lamda), sin(lamda), 0],
        [-sin(lamda), cos(lamda), 0],
        [0, 0, 1]]

#//Умножение матриц: t5 = t5Y*t5Z
    t5 = numpy.dot(t5Y, t5Z)

#//Умножение матриц: MAG = t5*tGEO
    return  numpy.dot(t5, GEO)  #MAG

def calculate(lat, lng, alt, data, h):
	params.N = len(IGRF_g) #- 1#// длина апроксимируещего ряда (максимальная степень сферических
                           #гармоник)
	params.initInput(lat, lng, alt, data, h)
	mats.actualize(params.year, Age, params.N)

	Uv = U(params.r, params.lamda, params.teta)

	datenow = date.today()
	Ynum = days_z(datenow.year, datenow.month, datenow.day)  ##date("z") + 1;

	[X_, Y_, Z_] = coords(params.UT, params.n_p, params.v, Ynum, params.teta, params.lamda, params.alt)

	GEO = calculateGEO(params.north, params.east, params.alt, a, b)

	MAG = rotate(params.year, Age, params.lamda, GEO)
        #//составляющие вектора индукции геомагнитного поля внутриземных
        #источников
	BX = (1 / params.r) * dUdteta(params.r, params.lamda, params.teta)
	

	BY = 0
	if params.teta!=0:
		BY=(-1 / (params.r * sin(params.teta))) * dUdlamda(params.r, params.lamda, params.teta)
	BZ = dUdr(params.r, params.lamda, params.teta)

    #// прямоугольные составляющи вектора индукции в точке с координатами fi,
    #lamda,r, [нТл]
	Bx = BX * cos(params.fi - params.fi_sh) + BZ * sin(params.fi - params.fi_sh)
	By = BY
	Bz = BZ * cos(params.fi - params.fi_sh) - BX * sin(params.fi - params.fi_sh)

    #// полный вектор геомагнитного поля анутриземных исочников, [нТл]
	B = sqrt(pow(Bx, 2) + pow(By, 2) + pow(Bz, 2))

	#//Магнитное склонение, [град]
	D = (180 / pi) * atan(By / Bx)
	#/Магнитное наклонение, [град]
	I = (180 / pi) * asin(Bz / B)

	#// Широта северного магнитного полюса
	FI = (180 / pi) * atan(IGRF_g[1][0] / sqrt(pow(IGRF_g[1][1], 2) + pow(IGRF_h[1][1], 2)))

	#//Долгота северного магнитного полюса
	LAMDA = (180 / pi) * atan(IGRF_h[1][1] / IGRF_g[1][1])

	#// Магнитный момент геомагнитного диполя
	M = pow(params.r, 3) * sqrt(pow(IGRF_g[1][0], 2) + pow(IGRF_g[1][1], 2) + pow(IGRF_h[1][1], 2))

    #//пересчет в град
	latMAG = atan((MAG[2]) / (sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))) * (180 / pi)
	if (MAG[1] > 0):
		longMAG = acos((MAG[0]) / (sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))) * (180 / pi)
	else:
		longMAG = 360 - (acos((MAG[0]) / (sqrt(pow(MAG[0], 2) + pow(MAG[1], 2)))) * (180 / pi))
   


	proto_f = [params.teta,
	params.lamda,
	params.N,
	Uv,
	Bx,
	By,
	Bz,
	B,
	D,
	I,
	FI,
	LAMDA,
	M,
	latMAG,
	longMAG,
	sqrt(pow(MAG[0], 2) + pow(MAG[1], 2) + pow(MAG[2], 2))]
	return  proto_f


def main():
    #date_default_timezone_set("UTC");
    #//header('Content-Type: text/xml');
   	
    

    #####################################
    ##TEST PARAMS lat=54.7364&lng=55.9631&data=2018.80&alt=0.167&h=14
    lat = 54.7364
    lng = 55.9631
    data = 2018.80
    alt = 0.167
    h = 16
    
     ##################################



    proto_f = calculate(lat, lng, alt, data, h)

    print("=======")

    for i in range(len(proto_f)):
        print(proto_f[i])

    print("=======")

   
    jsonStringBx = json.dumps(proto_f)  #jsonStringBx = json_encode(proto_f);
    print(jsonStringBx)


if __name__ == '__main__':
    main()
