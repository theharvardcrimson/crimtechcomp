from django.shortcuts import render

ALPHA = 26
LOWA = 97
CAPA = 65

def ascii_to_alpha(a):
    if (a.isupper()):
        return ord(a) - CAPA
    else:
        return ord(a) - LOWA

def encode(msg, k):
	encoded = ""
	keyi = 0
	inc = True
	for c in msg:
		if c.isalpha():
			encoded += chr((ascii_to_alpha(c) + ascii_to_alpha(k[keyi])) % ALPHA + LOWA)
		else:
			encoded += c
		if inc == True:
			keyi += 1
		else:
			keyi -= 1
		if keyi == len(k):
			keyi -= 1
			inc = False
		elif keyi < 0:
			keyi += 1
			inc = True
	return (encoded)

def encode_view(request): #<-- this is a view
  if request.method == 'POST':
    context = {'key': None, 'msg': None, 'result': None}

    key, msg = request.POST['key'], request.POST['msg']

    context['key'] = key
    context['msg'] = msg
    context['result'] = encode(msg, key)

    return render(request, 'result.html', context=context)

  else:
    return render(request, 'encode.html')

# # Create your views here.
# def encode_view(request):
# 	if request.method == 'POST':
# 		key, msg = request.POST['key'], request.POST['msg']
# 		context = {'key': key, 'msg': msg, 'result': none}
# 		context['result'] = encode(msg, key)
		
# 		return render(request, 'encode.html', context=context)
#     else:
#     	return render(request, 'encode.html')