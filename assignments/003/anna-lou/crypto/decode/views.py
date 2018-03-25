from django.shortcuts import render

# Create your views here.
def decode(msg, key):
  msgl = len(msg)
  keyl = len(key)
  res = ""
  counter = 0
  forward = True
  for i in range(msgl):
    msgc = ord(msg[i]) - (65 if msg[i].isupper() else 97)
    keyc = ord(key[counter]) - (64 if key[counter].isupper() else 96)
    res += chr((msgc - keyc) % 26 + 97) if msg[i].isalpha() else msg[i]
    counter += 1 if forward else -1
    if counter > keyl - 1:
      counter = keyl - 1
      forward = False
    elif counter < 0:
      counter = 0
      forward = True
  return res

def decode_view(request):
  if request.method == 'POST':
    context = {'result': None}

    context['msg'], context['k'] = request.POST['message'], request.POST['key']

    context['result'] = decode(context['msg'], context['k'])

    return render(request, '../../crypto/templates/result.html', context=context)

  else:
    return render(request, 'decode.html')
