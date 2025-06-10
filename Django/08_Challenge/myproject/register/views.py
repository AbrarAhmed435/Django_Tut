from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.

def register_home(request):
    return render(request,'register_home.html')

#Hello