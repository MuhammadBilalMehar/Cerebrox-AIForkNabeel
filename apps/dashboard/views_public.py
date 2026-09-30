from django.shortcuts import render


def landing(request):
    # Courses are personal to each student (no global/shared subject list to show here).
    return render(request, 'public/landing.html')


def about(request):
    return render(request, 'public/about.html')
