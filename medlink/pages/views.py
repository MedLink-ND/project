from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.


def index(request):

    #try:
    #    return render(request, "index.html")
    #except Exception as e:
    #    print(e)
    #    print("error")

    return render(request, 'index.html')
