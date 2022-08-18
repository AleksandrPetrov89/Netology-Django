from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


with open(BUS_STATION_CSV, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    station_list = []
    # Для экономии ресурсов использую только необходимые данные
    for line in reader:
        station_list.append({"Name": line["Name"], "Street": line["Street"],
                             "District": line["District"]})
    # station_list = list(reader)


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    # context = {
    #     'bus_stations': ...,
    #     'page': ...,
    # }

    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(station_list, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page,
    }

    return render(request, 'stations/index.html', context)
