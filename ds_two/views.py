from django.shortcuts import render , HttpResponse
import sys
import os



# Create your views here.
def index(request):#indextwo
    return render(request, 'index.html')            
        

def index2(r):    
    return render(r, 'index2.html')

def index3(r):    
    return render(r, 'index3.html')


def ds_two(r):    
    return render(r, 'ds_two.html')

def test(r):    
    return render(r, 'test.html')

def test2(r):    
    return render(r, 'test2.html')

