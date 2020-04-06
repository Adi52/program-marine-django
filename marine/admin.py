from django.contrib import admin

from .models import ParkingPlace, EntryData


def reset_occupied_to(modeladmin, request, queryset):
    queryset.update(occupied_to=None)
    queryset.update(name_yacht=None)


# Register your models here.
class ParkingPlaceAdmin(admin.ModelAdmin):
    list_display = ('parking_place', 'name_yacht', 'occupied_to', 'place_free')
    actions = [reset_occupied_to]


admin.site.register(ParkingPlace, ParkingPlaceAdmin)
admin.site.register(EntryData)



"""
Tu jest taki problem, że po wywołaniu funkcji reset_occupied_to zeruje ona objekt w ParkingPlace, powinna też usunąć 
powiązany obiekt w EntryData. Ponieważ po wyzerowaniu obiektu ParkingPlace na stronie głownej miejsce pokazuje jako 
wolne (i tak właśnie powinno działać), ale po złożeniu rezerwacji na miejscu "wolnym" występuje błąd ponieważ próbujemy
przypisać więcej niż jedną łódkę do jednego miejsca.


Dodaj drugą deklarację (nierezydencką)
zrób jakieś rozróżnianie między rezydentem a nie rezydentem. 


Zrób testy!!


Zrób wymóg potwierdzenia z maila, w przeciwnym wypadku rezerwacja jest usuwana.


Zrób logowanie, może w przyszłości


Zrób apke do obliczania wysokości opłaty za postój


Frontend

Po upłynięciu terminu postoju zrób podświetlenie danej pozycji w panelu admina, oraz zmianę na stronie głównej na 
napis w stylu "zajęte", czy "rezerwacja".
"""