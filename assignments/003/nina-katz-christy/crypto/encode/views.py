from django.shortcuts import render

def encode(msg, k):
	return ""

# Create your views here.
def encode_view(request):
    return render(request, 'encode.html')