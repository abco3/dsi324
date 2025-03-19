from django.shortcuts import render

def index(request):
    """
    A simple view to render the index page.
    """
    return render(request, 'index.html')