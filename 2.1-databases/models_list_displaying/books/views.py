from datetime import date

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import Book


def index(request):
    return redirect('books')


books = Book.objects.all().order_by("pub_date")
all_date = [book.pub_date for book in books]


def books_view(request):
    template = 'books/books_list.html'
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(books, 2)
    page = paginator.get_page(page_number)
    context = {
        'page': page,
    }
    return render(request, template, context)


def view_books_pub_date(request, pub_date: date):
    if pub_date not in all_date:
        return redirect('books')
    template = 'books/books_pub_date.html'
    page_number = int(request.GET.get("page", 1))
    books_pub_date = books.filter(pub_date=pub_date)
    date_before, date_after = None, None
    for book in books:
        if book.pub_date < pub_date:
            date_before = book.pub_date
        if book.pub_date > pub_date:
            date_after = book.pub_date
            break
    paginator = Paginator(books_pub_date, 2)
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'date_before': date_before,
        'date_after': date_after

    }
    return render(request, template, context)
