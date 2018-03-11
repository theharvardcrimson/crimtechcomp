from django.shortcuts import render

# Create your views here.
def calculate(x, y, f): #<-- this is just a function
  f = f.strip().lower()
  if f == 'add':
    return x + y
  elif f == 'subtract':
    return x - y
  elif f == 'multiply':
    return x * y
  elif f == 'divide':
    return x / y
  elif f == 'power':
    return x ** y
  else:
    return None

def encode_view(request): #<-- this is a view
  if request.method == 'POST':
    context = {'calculation': None}

    x, y = request.POST['x'], request.POST['y']
    fun = request.POST['function']

    context['calculation'] = calculate(x, y, fun)

    return render(request, 'encode.html', context=context)

  else:
    return render(request, 'encode.html')