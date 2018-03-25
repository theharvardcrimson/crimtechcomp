from django.shortcuts import render

# from models import *

# ENCODE

def encode(msg, key):
	msg = list(msg)

	for i in range(0, len(msg)):
		if i > 0 and i % len(key) == 0:
			key =  key[::-1]

		k = key[i % len(key)]

		kVal = ord(k) - 65 if k.isupper() else ord(k) - 97

		if msg[i].isalpha():
			if msg[i].isupper():
				base = 65
			else:
				base = 97

			msg[i] = chr(base + (ord(msg[i]) + kVal - base) % 26)

	return ''.join(msg) 


def encode_view(request):
	if request.method == 'POST':
		if 'msg' in request.POST and 'key' in request.POST:
			msg = request.POST['msg']
			key = request.POST['key']

			# encoded = Encoded_Message(key=key, plaintext=msg, ciphertext=crypto)
			# encoded.save()
			context = {'message': msg, 'key': key, 'ciphertext': encode(msg, key)}
		else:
			context = {'message': "", 'key': "", 'ciphertext': ""}

		return render(request, 'encode_result.html', context=context)
	else:
		return render(request, 'encode.html')
