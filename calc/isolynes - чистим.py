# -*- coding: utf-8 -

from math import *
from numpy import dot, arange, inf
import json
from BXfunctions import BXf, BZf, BYf, Bf, BXgradient, BYgradient, BZgradient, Bgradient, getActualMatrixes 



class myGeom:
    n = float
    e = float

    def __init__(self, n:float=0, e:float=0):
        self.n = float(n)
        self.e = float(e)

    def correct(n:float, e:float) -> tuple:
        if e > 180:
            e-=360
        if e < -180:
            e+=360
        if n > 90:
            n = 90 - (n - 90)
            e*=-1
        if n < -90:
            n = -90 + (-90 - n)
            e*=-1
        return (n, e)

    def isCorrectPoint(self) -> bool:
        return abs(self.n) <= 90 and abs(self.e) <= 180


    def __add__(self, other):
        n = self.n + other.n
        e = self.e + other.e

        (n, e) = myGeom.correct(n, e)
        res = myGeom(n, e)
        return  res

    def __mul__(self, other:float):
        return myGeom(self.n * other, self.e * other)

    def length(self) -> float:
        return sqrt(self.n ** 2 + self.e ** 2)

    def __str__(self) -> str:
        return json.dumps({'n':self.n, 'e':self.e})

    def range(self, other) -> float:
        dn = abs(self.n - other.n)
        de = abs(self.e - other.e)
        de = min(de, abs(de - 360))

        return sqrt((dn) ** 2 + (de) ** 2)

    def range(self, n:float, e:float) -> float:
        dn = abs(self.n - n)
        de = abs(self.e - e)
        de = min(de, abs(de - 360))

        return sqrt((dn) ** 2 + (de) ** 2)


def getMinMaxCoords(n_range, e_range, f:"BX, BY, BZ", F_g, F_h)->tuple:
    maxVal = -inf
    minPoint = myGeom()
    maxPoint = myGeom()
    minVal = inf

    for n in n_range:
        tmp = {}
        for e in e_range:
            val = f(n, e, F_g, F_h)
            if val > maxVal:
                maxVal = val
                maxPoint = myGeom(n, e)

            if val < minVal:
                minVal = val
                minPoint = myGeom(n, e)
    return (minPoint, maxPoint)


def binSearch(low:myGeom, high:myGeom, target:int, eps:float, f:"BX, BY, BZ", F_g, F_h):
    """
    low - точка, в которой зн-е Bx меньше искомого
    high - точка, в которой зн-е Bx больше искомого
    targetBX - искомое зн-е  
    """                   

    eps2 = 1e-3
    while abs(low.n - high.n) > eps2 or abs(low.e - high.e) > eps2:
        mid = myGeom((low.n + high.n) / 2, (low.e + high.e) / 2)   

        val = f(mid.n, mid.e, F_g, F_h) 
        if abs(val - target) < eps : #нашли
            break  

        if val > target:
            high = mid
        else:
            low = mid

    return mid

def binSearch2(low:dict, high:dict, target:int, eps:float, f:"BX, BY, BZ", F_g, F_h):
    """
    low - точка, в которой зн-е Bx меньше искомого
    high - точка, в которой зн-е Bx больше искомого
    targetBX - искомое зн-е  
    """                   
    eps2 = 1e-3
    print(low)
    print(hish)
    while abs(low['x'] - high['x']) > eps2 or abs(low['y'] - high['y']) > eps2:
        midP = mid(low, high) 

        val = f(midP['x'], midP['y'], F_g, F_h) 
        if abs(val - target) < eps : #нашли
            break  

        if val > target:
            high = mid
        else:
            low = mid

    return mid


def nearestWithValue(point:myGeom, target:int, eps:float, dist:float, f:"BX, BY, BZ", gradF:"gradBX, gradBY, gradBZ", F_g, F_h):
    grad = myGeom()
    (grad.n, grad.e) = gradF(point.n, point.e, F_g, F_h)
    val = f(point.n, point.e, F_g, F_h)
    step = 0.1 / grad.length()
    if(val > target):
        npoint = point + grad * (-step)
        while f(npoint.n, npoint.e, F_g, F_h) > target:
            npoint+=grad * (-step)
            if abs(npoint.n) > 88.5:
                return False
        npoint2 = binSearch(npoint, point, target, eps, f, F_g, F_h)
    else:
        npoint = point + grad * step
        while f(npoint.n, npoint.e, F_g, F_h) < target:
            npoint+=grad * (-step)
            if abs(npoint.n) > 88.5:
                return False
        npoint2 = binSearch(point, npoint, target, eps, f, F_g, F_h)
   # val = f(npoint2.n, npoint2.e, F_g, F_h)
    return npoint2

def func(p:tuple, f, F_g, F_h):
    return ((p[0], p[1]) , f(p[0], p[1], F_g, F_h))

def getAllPoints(n_range, e_range, f, F_g, F_h):
    """
    Возвращает словарь dict[(n, e)] = Bx(n, e)
    """    
    res = {}
    points = [(n, e) for n in n_range for e in e_range]

    res1 = map(lambda p: func(p, f, F_g, F_h), points)
    for p in res1:
        res[p[0]] = p[1]

    return res



def findNextPoints(n:float, e:float,  n_max:float, e_max:float, step:float):
    """
    Возвращает массив
    nearest[i] = (n, e)
    """
    nearestPoints = []
    if n + step <= n_max:
        nearestPoints.append((n + step, e))
    if e + step <= e_max:
        nearestPoints.append((n, e + step))
    if n + step <= n_max and e + step <= e_max:
        nearestPoints.append((n + step, e + step))
    return nearestPoints

def findValsinNearest(n:float, e:float, nearestPoints:list, isolineStep:int, ValsInPoints:dict, f, F_g, F_h):
    """
    Поиск значений Bx между соседями
    Возвращает словарь {myGeom(n, e): bx(n, e)}
    """
    val = ValsInPoints[(n, e)]
    res = {}
    if(val == int(val) and int(val) % isolineStep == 0):
        res[myGeom(n, e)] = val
    #print(Bx1)
    for nearest in nearestPoints:
        val1 = ValsInPoints[nearest]
        

        if val // isolineStep == val1 // isolineStep:
            continue
       # print(nearest, bx)
        count = int(abs(val - val1) // isolineStep) + 1
        if val > val1:
             maxVal = val
             minVal = val1
             minPoint = myGeom(nearest[0], nearest[1])
             maxPoint = myGeom(n, e)
        else:
             minVal = val
             maxVal = val1
             maxPoint = myGeom(nearest[0], nearest[1])
             minPoint = myGeom(n, e)

        val1 = maxVal - maxVal % isolineStep

        for i in range(count):             
            point = binSearch(minPoint, maxPoint, val1, 1e-2, f, F_g, F_h)
            res[point] = val1
            val1-=isolineStep
    #print(res)
    return res

def calculateIsolyne(point:myGeom, targetVal:float, prevLines:list, to:int, f, gradF, F_g, F_h):
    grad = myGeom()
    dist = 1.5#0.25#шаг поиска точек в градусах
    eps = 50#проверка значеиния от зн-я на изолинии
    points = [{'x':point.n, 'y':point.e}]
    while True:
        (grad.n, grad.e) = gradF(point.n, point.e, F_g, F_h) #градиент
        gradLen = grad.length()
        grad*=(dist / gradLen)

        norGrad = myGeom(grad.e, -grad.n)#нормальный в-р к градиенту заданной длины
        point+= norGrad * to#идем по нему

        pVal = f(point.n, point.e, F_g, F_h)
        
        if abs(pVal - targetVal) > eps: #если сильно отклонились от изолинии
           point = nearestWithValue(point, targetVal, 1e-2, dist, f, gradF, F_g, F_h)  
           if point == False or point.range(points[len(points)-1]['x'],points[len(points)-1]['y'])>7 :# если не нашли
               break
           pVal = f(point.n, point.e, F_g, F_h)

        if any([p for p in points if point.range(p['x'] ,p['y']) < 0.5]): #если повтор в этой линии
           points.append({'x':point.n, 'y':point.e})
           break   

        p = points[len(points) - 1]
        if point.range(p['x'] ,p['y']) > 7:#dist * 15:#если далеко от   #последней       
            break

        repeat = False  #повтор с предыдущими линиями
        for line in prevLines:
            if any([p1 for p1 in line if point.range(p1['x'], p1['y']) < 0.5]):
                repeat = True
                break
        if repeat:
            points.append({'x':point.n, 'y':point.e})
            break#изолиния уже есть

        points.append({'x':point.n, 'y':point.e})

        if abs(point.n) > 88.5:#если ушли за 85 параллель - выход
            break

    return points


#def savePoints(points, year):
#    f = open('points' + str(year) + '.txt', 'w')
#    for p in points:
#        f.write(str(p[0]) + ' ' + str(p[1]) + ' ' + str(points[p]) + '\n')
#    f.close()
    


def getIsolynes(year, f, gradF):
    [F_g, F_h] = getActualMatrixes(year)

    #calculator.initCache()
    print('loaded')
    #####################
    #params
    ###############
    n_min = -88
    n_max = 88
    step = 0.25

    e_min = -180
    e_max = 180
    #e_step = 15
    isolineStep = 500 
    allPoint = int(((n_max - n_min + 1) / step + 1) * ((e_max - e_min + 1) / step) + 1)

    now_perc = 0
    prev_perc = 0
    countPoint = 0

    n_range = arange(n_min, n_max + 1, step)
    e_range = arange(e_min, e_max + 1, step)

    BxInPoints = getAllPoints(n_range, e_range, f, F_g, F_h)
    #savePoints(BxInPoints, year)
    print('start points calculated')
    #print(BxInPoints)
    minB = int(round(min(BxInPoints.values())))
    maxB = int(round(max(BxInPoints.values())))

    minB = int(minB - int(minB) % isolineStep - isolineStep) #максимальное и минимальное с округлением
    maxB = int(maxB - int(maxB) % isolineStep + isolineStep)

    print(minB)
    print(maxB)
    vals = range(minB, maxB + 1, isolineStep)#значения по которым строим изолинии
    result = {}
   
    for Val in vals:
        result[Val] = []

    dist = 1.5
    print('calculate points')    


    for n in n_range:
        for e in e_range:

            countPoint+=1
            now_perc = countPoint / allPoint
            if(now_perc - prev_perc >= 0.01):
                print(str(now_perc * 100) + '%')
                prev_perc = now_perc

            Bx1 = BxInPoints[(n,e)]
            nearestPoints = findNextPoints(n, e, n_max,e_max, step)

            nearestVals = findValsinNearest(n, e, nearestPoints, isolineStep, BxInPoints, f, F_g, F_h)

            for point in nearestVals:
                Val = nearestVals[point]
                inIsolyne = False
                Isolynes = result[Val]
                for lyne in Isolynes:
                    for p in lyne:
                        if point.range(p['x'], p['y']) < dist:
                            inIsolyne = True
                            break
                    if inIsolyne:
                        break

                if inIsolyne:
                    continue
                isolyne1 = calculateIsolyne(point, Val,result[Val],  1, f, gradF, F_g, F_h)
                result[Val].append(isolyne1)
                isolyne2 = calculateIsolyne(point, Val, result[Val], -1, f, gradF, F_g, F_h)                 
                result[Val].append(isolyne2)

    return result

#def rangePoints(p1, p2):
#    dn = abs(p1['x'] - p2['x'])
#    de = abs(p1['y'] - p2['y'])
#    de = min(de, abs(de - 360))

#    return sqrt(dn * dn + de * de)


#def sortLynes(lynes):
#    for i in range(len(lynes)):
#        for j in range(i, len(lynes)):
#            if(len(lynes[j]) > len(lynes[i])):
#                tmp = lynes[i]
#                lynes[i] = lynes[j]
#                lynes[j] = tmp
#    return lynes

#def mid(p1, p2):
#    m1 = {'x':(p1['x'] + p2['x']) / 2, 'y':(p1['y'] + p2['y']) / 2}
#    m2 = {'x':(p1['x'] + p2['x']) / 2, 'y':(p1['y'] + p2['y']) / 2 + 180}
#    if m2['y'] > 180:
#        m2['y']-=360


#    if(rangePoints(p1,m1) < rangePoints(p1,m2)):
#        return m1
#    else:
#        return m2

#def listSplit(l, pos):
#    return (l[0:pos], l[pos:len(l)])


#def deleteIncorrect(lyne, Val, f, F_g, F_h):
#    res = [] 
#    eps = 500
#    maxD = 8


#    i = 0
#    while i < len(lyne) - 1:
#        p1 = lyne[i]
#        p2 = lyne[i + 1]
#        #midP = mid(p1, p2)

#        i+=1
#        #if (abs(f(midP['x'], midP['y'], F_g, F_h) - bxVal) > eps or rangePoints(p1, p2) > maxD):
#        if rangePoints(p1, p2)>maxD:
#            tmp = listSplit(lyne, i)
#            res.append(tmp[0])
#            lyne = tmp[1]
#            i = 0

#    if len(res) > 0:
#        return res
#    else:
#        return [lyne]


#def isSublyne(sublyne, lyne):
#    cnt = 0
#    dist = 1.5
#    for i in range(len(sublyne)):
#        if any([ p for p in lyne  if rangePoints(p, sublyne[i]) < dist]):
#            cnt+=1
#    if len(sublyne) - cnt < 3:
#        return True
#    else:
#        return False

#def addMissingLine(line, val, f, F_g, F_h):
#    p0 = line[0]
#    pn = line[len(line) - 1]
#    midP = mid(p0, pn)
#    eps = 250
#    dist = 3
#    if (abs(f(midP['x'], midP['y'], F_g, F_h) - val) < eps) and rangePoints(p0, midP) < dist and rangePoints(midP, pn) < dist:
#        line.append(midP)
#        line.append(p0)
#    return line


#def clearLynes3(lynesDict:dict, f, F_g, F_h):
#    for val in lynesDict:
#        nesLynes = []
#        for lyne in lynesDict[val]:
#            nesLynes+=deleteIncorrect(lyne, int(val), f,  F_g, F_h)
#        lynesDict[val] = nesLynes #list(filter(lambda l: len(l) > 2, nesLynes))
#    return lynesDict

#def clearLynes34(lynesDict:dict):  #3->4

#    for val in lynesDict:
#        nesLynes = lynesDict[val]
#        nesLynes = sortLynes(nesLynes)

#        subLynes = []

#        for i in range(len(nesLynes)):
#            for j in range(i + 1, len(nesLynes)):
#                if isSublyne(nesLynes[i], nesLynes[j]):
#                    subLynes.append(i)
#                    break
#        for i in subLynes[::-1]:
#            del nesLynes[i]#nesLynes.removeAt(i)

#        lynesDict[val] = nesLynes
#    return lynesDict

#def clearLynes45(lynes:dict, f, F_g:list, F_h:list):#(4)->(5)
#    for val in lynes:
#        nesLynes = []
#        for lyne in lynes[val]:
#            lyne = addMissingLine(lyne, int(val), f, F_g, F_h)
#            nesLynes.append(lyne)
#        lynes[val] = nesLynes

#    return lynes

#def clear(lynes:dict, f, F_g:list, F_h:list):
#    lynes = clearLynes3(lynes, f, F_g, F_h)
#    lynes = clearLynes45(lynes, f, F_g, F_h)
#    lynes = clearLynes34(lynes)
    
#    return lynes

        




def main():
    '''
    Создание изолиний, сохранение и чистка
    '''
    arr = [
           ('bx', BXf, BXgradient),
           ('by', BYf, BYgradient),
           ('bz', BZf, BZgradient),
           ('b', Bf, Bgradient)
           ]

    for year in range(2020, 2021, 1):
        [F_g, F_h] = getActualMatrixes(year)
        for (name, func, grad) in arr:
            res = getIsolynes(year, func, grad)

            print('saving ' + name)
            f = open(name + str(year) + '.txt', 'w')
            f.write(json.dumps(res))
            f.close()

            print(name + ' saved')
            #print('clearing ' + name)

            #res = clear(res, func, F_g, F_h)
            #print(name + str(year) + ' ready')
            #print('saving clear')

            #f = open('clear_' + name + str(year) + '.txt', 'w')
            #f.write(json.dumps(res))
            #f.close()

            #print(name + ' clear saved')
            print('end  ' + name + ' ' + str(year))

    return

if __name__ == "__main__":
    print('in iso')
    main()
