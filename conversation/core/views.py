from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, my name is Arthur!")


