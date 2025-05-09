from django.shortcuts import render
from datetime import datetime

def home(request):
    today = datetime.now().strftime('%H:%M:%S, %B %d, %Y')
    return render(request, 'home.html', {'today': today})