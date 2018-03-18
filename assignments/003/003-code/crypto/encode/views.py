from django.shortcuts import render

# ENCODE

def encode(msg, key):
	pass

def encode_view(request):
	if request.method == 'POST':
		return render(request, 'encode_result.html')
	else:
		return render(request, 'encode.html')
