from django.shortcuts import render


def home(request):
    context = {
        'name': "Yusuf"
    }
    return render(request, "backend/home.html", context=context)