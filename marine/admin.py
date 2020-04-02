from django.contrib import admin

from .models import ParkingPlace, EntryData


def reset_occupied_to(modeladmin, request, queryset):
    queryset.update(occupied_to=None)


# Register your models here.
class ParkingPlaceAdmin(admin.ModelAdmin):
    list_display = ('parking_place', 'occupied_to', 'place_free')
    actions = [reset_occupied_to]


admin.site.register(ParkingPlace, ParkingPlaceAdmin)
admin.site.register(EntryData)
