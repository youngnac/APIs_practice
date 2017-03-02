from django.shortcuts import redirect, render


def index_view(request):

    return render(request, 'base/index.html')