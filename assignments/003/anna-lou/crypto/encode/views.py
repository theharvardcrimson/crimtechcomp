from django.shortcuts import render

# Create your views here.
def encode(msg, key):
  msgl = len(msg)
  keyl = len(key)
  res = ""
  counter = 0
  forward = True
  for i in range(msgl):
    msgc = ord(msg[i]) - 97
    keyc = ord(key[counter]) - 96
    res += chr((msgc + keyc) % 26 + 97) if 0 <= msgc <= 26 else msg[i]
    counter += 1 if forward else -1
    if counter > keyl - 1:
      counter = keyl - 1
      forward = False
    elif counter < 0:
      counter = 0
      forward = True
  return res

def encode_view(request):
  if request.method == 'POST':
    context = {'result': None}

    msg, k = request.POST['message'], request.POST['key']

    context['result'] = encode(msg, k)
    print("\n\n\n" + context['result'])
    context['test'] = 'testtest'

    return render(request, '../../crypto/templates/result.html', context=context)

  else:
    return render(request, 'encode.html')
