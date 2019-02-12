# -*- coding: utf-8 -
from django.shortcuts import render
from django.http import HttpResponse
import json
from .calculator import calculate




def calc(request):
    north = float(request.GET['lat'])  # _GET['lat'] северная широта (южная со знаком "-")
    east = float(request.GET['lng'])   # _GET['lng'] восточная долгота (западная со знаком"-")
    alt = float(request.GET['alt'])    # _GET['alt'] высота над уровнем моря, км
    year = float(request.GET['data'])  # _GET['data'] текущая дата.(например 30 июня 2015 года запишется 2015.5)
    UT = float(request.GET['h'])       # _GET['h']
    proto_f = calculate(north, east, alt, year, UT)

    jsonStringBx = json.dumps(proto_f)
    return HttpResponse(jsonStringBx)
