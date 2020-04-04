from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError

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


def new_book(request):
    """Zarezerwuj miejsce postojowe"""

    if request.method == 'GET':
        form = EntryDataForm()
        global parking_place_form
        parking_place_form = request.GET['parking_place']

    else:
        form = EntryDataForm(request.POST)
        if form.is_valid():
            try:
                place = form.save(commit=False)
                parking_place = get_object_or_404(ParkingPlace, parking_place=parking_place_form)
                place.parking_place = parking_place
                place.save()
                return HttpResponseRedirect(reverse('marine:congrats'))
            except (IntegrityError, NameError):
                raise Http404("Miejsce zostało już zajęte!")

    context = {'form': form}
    return render(request, 'marine/new_book.html', context)


def congrats(request):
    return render(request, 'marine/congrats.html', {})


def create_and_download_declaration(request):
    """Strona po przesłaniu formularza oraz wygenerowanie deklaracji"""
    # Pobiera id miejsca postoju którego dotyczy deklaracja (w c_d nie można podać 'A-02' tylko id tego obiektu).
    try:
        id_parking_place = ParkingPlace.objects.get(parking_place=parking_place_form).id
        c_d = EntryData.objects.get(parking_place=id_parking_place)
        parking_place = str(c_d.parking_place)
        date = str(c_d.date)
        yacht = {'name': c_d.name_yacht, 'registration_number': c_d.registration_number, 'home_port': c_d.home_port,
                 'length': c_d.yacht_length, 'width': c_d.yacht_width, 'ytype': c_d.yacht_type}
        fee = {'parking_fee': count_parking_fee.count_parking_fee(c_d.parking_period_from, c_d.parking_period_to, yacht),
               'quarter_fee': 2000}
        print(fee['parking_fee'])
        if fee['parking_fee'] % 1 == 0:
            fee_words = '{}'.format(zl_to_words.change_to_words(floor(fee['parking_fee'])))
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
        create_declaration.create_declaration(document, parking_place, date, yacht, fee, fee_words, owner_details,
                                              parking_period, commissioning_body, chip_card)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        filename = replace_non_ascii.removeAccents('Deklaracja_{}.docx'.format(yacht['name']))
        response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)
        document.save(response)
        return response
    #Tu trzeba będzie coś wymyślić ;c
    except (IntegrityError, NameError):
        raise Http404("Miejsce zostało już zajęte!")


"""

Na jutro: 
- popraw rubrykę adres do korespondencji w declarations (dodatkowa zmienna) + tutaj if żeby się zgadzało 
- Dodaj i ustaw plik z obliczaniem opłaty (dokładnie!!!!)

BAARRRDZO DOBRA RRRROBOTA
"""
