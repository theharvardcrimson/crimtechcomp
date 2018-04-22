from django.shortcuts import render


def decode(ciphertext, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext]
    msg = ''
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        msg += chr(value + 65)
    return msg

# Create your views here.

def decode_view(request):
  if request.method == 'POST':
    context = {'result': None}

    key, message = request.POST['Key'], request.POST['Message']

    context['result'] = decode(message, key)

    return render(request, 'result.html', context=context)

  else:
    return render(request, 'decode.html')
