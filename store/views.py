from django.shortcuts import render
from .models import Book


def index(request):
    return render(request, 'template.html')

def store(request):
    books=Book.objects.all()

    context={
        'books':books,
    }

    #This is a demonstration for session variables
    '''
    request.session['location']="unknown"
    if request.user.is_authenticated():
        request.session['location'] = "Earth"
    '''
    #Then if you want to include the variable in site, add it to context variables

    return render(request, 'base.html', context)

def book_details(request, book_id):
    context={
        'book':Book.objects.get(pk=book_id),
    }
    return render(request,'store/detail.html', context)