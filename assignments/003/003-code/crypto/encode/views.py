from django.shortcuts import render

def encode(msg, k):
  ALPHABET_LENGTH = 26
  ORD_LOWER_A = ord('a')

  key_length = len(k)
  key_as_shift = [ord(i) - ORD_LOWER_A + 1 for i in k]
  ciphertext = ""

  for index, char in enumerate(msg):
    if char.isalpha():
      shift_index = (index % key_length) if ((index // key_length) % 2 == 0) else (-((index % key_length) + 1))
      ciphertext += chr(((ord(char) - ORD_LOWER_A + key_as_shift[shift_index]) % ALPHABET_LENGTH) + ORD_LOWER_A)
    else:
      ciphertext += char

  return ciphertext

def encode_view(request):
  if 'msg' in request.POST and 'key' in request.POST:
    result = encode(request.POST['msg'], request.POST['key'])
    context = {
      'user_input': request.POST['msg'],
      'user_input2': request.POST['key'],
      'result': result
    }
    return render(request, 'result.html', context=context)
  else:
    return render(request, 'encode.html')
