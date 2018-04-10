from django.shortcuts import render

def decode (msg, k):
    newstr = ""
    for i, c in enumerate(msg):
        try:
            val = int(c)
            newstr += str(val)
        except ValueError:
            if ((i // len(k)) % 2 == 0):
                adjusted = (ord(c) - (ord(k[i % len(k)])) + 96)
                if adjusted < 97:
                    newstr += chr(122 + ((ord(c) - (ord(k[i % len(k)])))))
                else:
                    newstr += chr((ord(c) - (ord(k[i % len(k)])) + 96))
            else:
                adjusted = ord(c) - (ord(k[-(i % len(k)) - 1])) - 96
                if adjusted < 97:
                    newstr += chr(122 + (ord(c) - (ord(k[-(i % len(k)) - 1]))))
                else:
                    newstr += chr((ord(c) - (ord(k[-(i % len(k)) - 1])) + 96))
    return newstr

# Create your views here.
def decode_view (request):
    if 'msg' in request.POST and 'key' in request.POST:
        result = decode(request.POST['msg'], request.POST['key'])
        context = {
            'user_input': request.POST['msg'],
            'user_input2': request.POST['key'],
            'result': result
        }
        return render(request, 'result.html', context=context)
    else:
        return render(request, 'decode.html')
