from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'

    sort = request.GET.get('sort', None)
    if sort == 'name':
        phones = Phone.objects.all().order_by('name')
    elif sort == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif sort == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all()
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(phones, 3)
    page = paginator.get_page(page_number)
    context = {
        'page': page,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
