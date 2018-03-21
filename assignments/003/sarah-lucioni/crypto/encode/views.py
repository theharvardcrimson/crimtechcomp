from django.shortcuts import render


A = ord('A')
a = ord('a')
# Create your views here.
def encrypt(msg, k): #<-- this is just a function
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
                ciph += chr((ord(c) - (2 * A) + ord(k[count]) + 1) % 26 + A)
            else:
                ciph += chr((ord(c) - (2 * a) + ord(k[count]) + 1) % 26 + a)
        else:
            ciph += c
        count += 1

    return ciph


def encode_view(request): #<-- this is a view
  #if request.method == 'POST':
    #context = {'encode': None}

    #msg, k = request.POST['msg'], request.POST['key']
    #fun = request.POST['function']

    #context['encode'] = encrypt(msg, k)

    #return render(request, 'encode.html', context=context)

  #else:
    return render(request, "encode.html")
