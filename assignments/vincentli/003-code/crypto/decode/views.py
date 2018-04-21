from django.shortcuts import render

# Create your views here.
def decode(request):
    if request.method == "POST":
        key = str(request.POST["key"]).lower()
        text = str(request.POST["text"]).lower()

        # Encrypting function
        keyIndex = 0
        forward = True
        encoded = []
        context = {}
        for i in range(len(text)):
            if ord(text[i]) >= ord('a') and ord(text[i]) <= ord('z'):
                t = ord(text[i]) - ord('a')
                k = 0
                if ord(key[keyIndex]) >= ord('a') and ord(key[keyIndex]) <= ord('z'):
                    k = ord(key[keyIndex]) - ord('a') + 1
                elif ord(key[keyIndex]) >= ord('0') and ord(key[keyIndex]) <= ord('9'):
                    k = ord(key[keyIndex]) - ord('0') + 10
                encoded.append(chr((t - k) % 26 + ord('a')))
            else:
                encoded.append(text[i])

            if forward:
                keyIndex += 1
            else:
                keyIndex -= 1
            if keyIndex >= len(key):
                forward = False
                keyIndex = len(key) - 1
            if keyIndex <= -1:
                forward = True
                keyIndex = 0


        context["encoded"] = ''.join(encoded)
        context["message"] = text
        context["key"] = key

        return render(request, "decoded.html", context=context)

    else:
        return render(request, "decode.html")
