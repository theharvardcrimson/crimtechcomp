from django.shortcuts import render

# Create your views here.
def encode(request):
    return render(request, "encode.html")
