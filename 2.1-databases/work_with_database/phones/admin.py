from django.contrib import admin

# Register your models here.
from .models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['id', 'name', 'price', 'image', 'release_date', 'lte_exists', 'slug']
    list_filter = ['id', 'name', 'price', 'release_date']
