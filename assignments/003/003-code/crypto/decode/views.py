from django.shortcuts import render

# DECODE

def decode(msg, key):
	pass

# Create your views here.
def decode_view(request):
	if request.method == 'POST':
		# context = {''}

		return render(request, 'decode_result.html')
	else:
		return render(request, 'decode.html')