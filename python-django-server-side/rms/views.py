from django.shortcuts import render
from django.http.response import HttpResponse


def zoozo(request):
    return HttpResponse('This message is encrypted and I know you are intelligent enough to decipher it 3A 2A  for you\n \n 4d792064656172204a6170616e657365204261636368612c0d0a5468697320746564647\n920697320666f7220796f752e2054686973207\n7696c6c2072656d696e6420796f75207468617420796f752073686f7\n56c6420736d696c652077686174657665722074686520736974756174696f6e2062652e0d0a596f757273206c6f76696e676c790d0a426162790d0a203a2a203a2a203a2a')
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def calorie_page(request):
    return render(request,'get_calorie.html')

def garima(request):
    return render(request,'garima.html')