from django.shortcuts import render

def base(request): #<-- this is a view
  return render(request, "base.html")
