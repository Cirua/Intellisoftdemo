from django.shortcuts import render

def index(request):
    context = {
        "home_page":"Home page 123",
        "user_name":"Damian"
    }
    
    return render(request, "index.html", context)