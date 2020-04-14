from django.contrib import admin

from .models import ParkingPlace, EntryData


def reset_occupied_to(modeladmin, request, queryset):
    queryset.update(occupied_to=None)
    queryset.update(name_yacht=None)


# Register your models here.
class ParkingPlaceAdmin(admin.ModelAdmin):
    list_display = ('parking_place', 'check_it', 'name_yacht', 'occupied_to', 'place_free')
    actions = [reset_occupied_to]


class EntryDataAdmin(admin.ModelAdmin):
    list_display = ('parking_place', 'check_it', 'name_yacht')


admin.site.register(ParkingPlace, ParkingPlaceAdmin)
admin.site.register(EntryData, EntryDataAdmin)

"""
Zrób wymóg potwierdzenia z maila, w przeciwnym wypadku rezerwacja jest usuwana.

Zrób testy!!

Zrób logowanie, może w przyszłości

Zrób apke do obliczania wysokości opłaty za postój


Frontend

"""
