from django.shortcuts import render

def decode (msg, k):
    newstr = ""
    for i, c in enumerate(msg):
        try:
            val = int(c)
        except ValueError:
            if ((i // len(k)) % 2 == 0):
                newstr + chr(ord(c) - ord(key[-(i % len(k))]))
            else:
                newstr + chr(ord(c) - ord(key[i % len(k)]))

# Create your views here.
def decode_view (req):
    if 'msg' in req.POST and 'key' in req.POST:
        result = decode(request.POST['msg'], request.POST['key'])
        context = {
            'user_input': request.POST['msg'],
            'user_input2': request.POST['key'],
            'result': result
        }
    return render(request, 'decode.html', context=context)
