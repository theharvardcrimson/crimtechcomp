from django.shortcuts import render


A = ord('A')
a = ord('a')
# Create your views here.
def decrypt(msg, k): #<-- this is just a function
    ciph = ""
    count = 0
    for c in msg:
        if count == len(k):
            count = 0
            # reverse key
            k = k[:: -1]

        # Check to see if char is alphabetic
        if c.isalpha():
            # Preserve case
            if c.isupper():
                # Convert ASCII to alphabetical index, add key, turn back to ASCII
                ciph += chr((ord(c) - ord(k[count]) - 1) + A)
            else:
                ciph += chr((ord(c) - ord(k[count]) - 1) + a)
        else:
            ciph += c
        count += 1

    return ciph


def decode_view(request): #<-- this is a view
  if request.method == 'POST':
    context = {'decode': None}

    msg, k = request.POST['msg'], request.POST['key']
    fun = request.POST['function']

    context['decode'] = decode(msg, k)

    return render(request, 'decode.html', context=context)

  else:
    return render(request, 'decode.html')
