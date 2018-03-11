from django.shortcuts import render

def encode (msg, k) :
    newstr = ""
    for i, c in enumerate(msg):
        try:
           val = int(c)
        except ValueError:
            if ((i // len(k)) % 2 == 0):
                newstr + chr(ord(c) + ord(key[-(i % len(k))]))
            else:
                newstr + chr(ord(c) + ord(key[i % len(k)]))

# Create your views here.
def encode_view (req) :
  if 'msg' in req.POST and 'key' in req.POST:
      result = encode(request.POST['msg'], request.POST['key'])
      context = {
        'user_input': request.POST['msg'],
        'user_input2': request.POST['key'],
        'result': result
      }
  return render(request, 'encode.html', context=context)
