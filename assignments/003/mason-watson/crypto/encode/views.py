from django.shortcuts import render

def encode (msg, k):
    newstr = ""
    for i, c in enumerate(msg):
        try:
           val = int(c)
           newstr += str(val)
        except ValueError:
            if ((i // len(k)) % 2 == 0):
                adjusted = (ord(c) + (ord(k[i % len(k)])) - 96)
                if adjusted >= 123:
                    newstr += chr((ord(c) + (ord(k[i % len(k)])) - 96) % 123 + 97)
                else:
                    newstr += chr((ord(c) + (ord(k[i % len(k)])) - 96))
            else:
                adjusted = ord(c) + (ord(k[-(i % len(k)) - 1])) - 96
                if adjusted >= 123:
                    newstr += chr((ord(c) + (ord(k[-(i % len(k)) - 1])) - 96) % 123 + 97)
                else:
                    newstr += chr((ord(c) + (ord(k[-(i % len(k)) - 1])) - 96))
    return newstr

# Create your views here.
def encode_view (request) :
  if 'msg' in request.POST and 'key' in request.POST:
      msg = request.POST['msg']
      key = request.POST['key']
      result = encode(msg, key)
      context = {
        'user_input': msg,
        'user_input2': key,
        'result': result
      }
      return render(request, 'result.html', context=context)
  else:
      return render(request, 'encode.html')
