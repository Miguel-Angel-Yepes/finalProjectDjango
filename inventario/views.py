from django.shortcuts import render

# Crear la vista del home
def home(request):
    return render(request, 'home.html', {})  