from django.shortcuts import render

# Create your views here.


def main_view(request, **kwargs):
    return render(
        request,
        'songbook/main.html',
        kwargs
    )
