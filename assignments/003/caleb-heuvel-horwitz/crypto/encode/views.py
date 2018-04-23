from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
alphabet = "abcdefghijklmnopqrstuvwxzy"

def encode(msg, k): 
	output = ""
	counter = 0
	key = k
	for i in msg:
		key += k[::-1] + k
	for i in msg:
		if i.isdigit() == True:
			output += i
			counter += 1
		elif i.isalpha() == False:
			output += i
			counter +=1
		elif i.isalpha() == True:
			if msg.index(i) == 0:
				output += alphabet[alphabet.index(i)+alphabet.index(key[counter])+1]
				counter += 1
			else:
				if (alphabet.index(i)+alphabet.index(key[msg.index(i)])+1) > 25:
					output += alphabet[alphabet.index(i)+alphabet.index(key[msg.index(i)])-24]
					counter += 1
				else:
					output += alphabet[alphabet.index(i)+alphabet.index(key[msg.index(i)])+1]
					counter += 1



def encode_view(request): 
 	if 'message' in request.POST and 'key' in request.POST:
  		result = encode('message', 'key')
  		context = {
    		'user_input': request.POST['message'],
    		'user_input2': request.POST['key'],
    		'result': result
  		}
		return render(request, 'result.html', context=context)