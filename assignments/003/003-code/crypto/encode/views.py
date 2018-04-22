from django.shortcuts import render


def encode(msg, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    msg_int = [ord(i) for i in msg]
    ciphertext = ''
    for i in range(len(msg_int)):
        value = (msg_int[i] + key_as_int[i % key_length]) % 26
        ciphertext += chr(value + 65)
    return ciphertext

# Create your views here.

def encode_view(request):
  if request.method == 'POST':
    context = {'result': None}

    key, message = request.POST['Key'], request.POST['Message']

    context['result'] = encode(message, key)

    return render(request, 'result.html', context=context)

  else:
    return render(request, 'encode.html')
