from django.shortcuts import render

def decode(msg, key):
  x = ""
  key = key.upper()
  counter = 0
  for ch in msg:
    val = ord(key[counter]) - ord('A') + 1
    if ch.islower():
      x += chr((ord(ch) - val - ord('a')) % 26 + ord('a'))
    elif ch.isupper():
      x += chr((ord(ch) - val - ord('A')) % 26 + ord('A'))
    else:
      x += ch
    if counter == len(key) - 1:
      key = key[::-1]
      counter = 0
    else:
      counter += 1
  return x


def decode_view(request):
  if 'msg' in request.POST and 'key' in request.POST:
    msg = request.POST['msg']
    key = request.POST['key']
    context = {'message': msg, 'key': key, 'res': decode(msg, key)}
    return render(request, 'decoded.html', context=context)
  else:
    return render(request, 'decode.html')
    
