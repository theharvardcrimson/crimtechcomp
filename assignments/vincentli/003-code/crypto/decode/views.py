from django.shortcuts import render

# Create your views here.
def decode(request):
    return render(request, "decode.html")
