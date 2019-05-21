from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request,
	'main.html')

def main2(request):
	return render(request,
	'main2.html')