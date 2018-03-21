from django.shortcuts import render

# Create your views here.
def calculate(x, y): #<-- this is just a function
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
  else
    return None

def my_view_name(request): #<-- this is a view
  if request.method == 'POST':
    context = {'calculation': None}

    msg, k = request.POST['msg'], request.POST['k']

    context['calculation'] = calculate(msg, k)

    return render(request, 'calculated.html', context=context)

  else:
    return render(request, 'my_page_name.html')