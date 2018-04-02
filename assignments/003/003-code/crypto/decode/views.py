from django.shortcuts import render

# DECODE

def decode(crypto, key):
	crypto = list(crypto)

	for i in range(0, len(crypto)):
		if i > 0 and i % len(key) == 0:
			key =  key[::-1]

		k = key[i % len(key)]

		kVal = ord(k) - 65 if k.isupper() else ord(k) - 97

		if crypto[i].isalpha():
			if crypto[i].isupper():
				base = 65
			else:
				base = 97

			crypto[i] = chr(base + (ord(crypto[i]) - kVal - base) % 26)

	return ''.join(crypto)

# Create your views here.
def decode_view(request):
	if request.method == 'POST':
		if 'msg' in request.POST and 'key' in request.POST:
			msg = request.POST['msg']
			key = request.POST['key']

			# encoded = Encoded_Message(key=key, plaintext=msg, ciphertext=crypto)
			# encoded.save()
			context = {'message': msg, 'key': key, 'plaintext': decode(msg, key)}
		else:
			context = {'message': "", 'key': "", 'plaintext': ""}

		return render(request, 'decode_result.html', context=context)
	else:
		return render(request, 'decode.html')