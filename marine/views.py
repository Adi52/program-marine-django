from os import urandom
from binascii import hexlify

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.views import generic

from math import floor

from .models import ParkingPlace, EntryData
from .forms import EntryDataForm

from externals.apps import replace_non_ascii, zl_to_words, count_parking_fee
from externals.apps.declarations import create_declaration

from docx import Document


class IndexView(generic.ListView):
    template_name = 'marine/index.html'
    context_object_name = 'parking_places'

    def get_queryset(self):
        return ParkingPlace.objects.order_by('parking_place')


def new_book(request, parking_place_id):
    """Zarezerwuj miejsce postojowe"""
    parking_place = get_object_or_404(ParkingPlace, id=parking_place_id)
    if request.method != 'POST':
        form = EntryDataForm()

    else:
        form = EntryDataForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.parking_place = parking_place
            place.save()
            secret_key = hexlify(urandom(32)).decode()
            return HttpResponseRedirect(reverse('marine:congrats', args=[secret_key, parking_place_id]))

    context = {'form': form, 'parking_place_id': parking_place_id}
    return render(request, 'marine/new_book.html', context)


def congrats(request, secret_key, parking_place_id):
    return render(request, 'marine/congrats.html', {'parking_place_id': parking_place_id, 'secret_key': secret_key})


def create_and_download_declaration(request, secret_key, parking_place_id):
    """Strona po przesłaniu formularza oraz wygenerowanie deklaracji"""
    c_d = get_object_or_404(EntryData, parking_place=parking_place_id)
    parking_place = str(c_d.parking_place)
    date = str(c_d.date)
    yacht = {'name': c_d.name_yacht, 'registration_number': c_d.registration_number, 'home_port': c_d.home_port,
             'length': c_d.yacht_length, 'width': c_d.yacht_width, 'ytype': c_d.yacht_type}
    fee = {
        'parking_fee': count_parking_fee.count_parking_fee(c_d.parking_period_from, c_d.parking_period_to, yacht),
        'quarter_fee': 0}
    if fee['parking_fee'] % 1 == 0:
        fee_words = '{} złotych.'.format(zl_to_words.change_to_words(floor(fee['parking_fee'])))
    else:
        fee_words = '{} złotych {}/100 groszy'.format(zl_to_words.change_to_words(floor(fee['parking_fee'])),
                                                      str(round(fee['parking_fee'] % 1, 2))[2:])
    owner_details = {'name': c_d.owner_details_name, 'address': c_d.owner_details_address}
    parking_period = {'from': c_d.parking_period_from.strftime("%d.%m.%Y"),
                      'to': c_d.parking_period_to.strftime("%d.%m.%Y")}

    commissioning_body = {'name': c_d.commissioning_body_name, 'address': c_d.commissioning_body_address,
                          'tel': c_d.commissioning_body_tel, 'e-mail': c_d.commissioning_body_email,
                          'nip': c_d.commissioning_body_nip}
    # Domyślnie False, ponieważ większości jachtów nie dotyczy
    chip_card = c_d.chip_card
    document = Document('externals/apps/declarations/deklaracja.docx')
    create_declaration.create_declaration_resident(document, parking_place, date, yacht, fee, fee_words, owner_details,
                                          parking_period, commissioning_body, chip_card)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    filename = replace_non_ascii.removeAccents('Deklaracja_{}.docx'.format(yacht['name']))
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)
    document.save(response)
    return response
