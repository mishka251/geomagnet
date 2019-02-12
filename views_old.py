from django.shortcuts import render
from django.http import HttpResponse
from calculator import *
#import calc2 
# Create your views here.
def index(request):
	return render(request,
	'main.html')
	
def calc(request):
	lat = float(request.GET['lat'])
	lng = float( request.GET['lng'])
	alt = float(request.GET['alt'])
	data = float(request.GET['data'])
	h = float(request.GET['h'])

	proto_f = calculate(lat, lng, alt, data, h)
	jsonStringBx = json.dumps(proto_f)
	return 	HttpResponse(jsonStringBx)