from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    page_number = int(request.GET.get("page", 1))
    books = Book.objects.all()
    paginator = Paginator(books, 9)
    page = paginator.get_page(page_number)
    context = {
        'page': page,
    }
    return render(request, template, context)


def view_books_pub_date(request, pub_date: datetime):
    template = 'books/books_pub_date.html'
    page_number = int(request.GET.get("page", 1))
    books = Book.objects.all()
    paginator = Paginator(books, 9)
    page = paginator.get_page(page_number)
    context = {
        'page': page,
    }
    return render(request, template, context)
