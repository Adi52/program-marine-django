from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from math import floor

from .models import ParkingPlace, EntryData
from .forms import EntryDataForm

from externals.apps import replace_non_ascii, zl_to_words
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
            place = form.save(commit=False)
            parking_place = ParkingPlace.objects.get(parking_place=parking_place_form)
            place.parking_place = parking_place
            place.save()
            return HttpResponseRedirect(reverse('marine:congrats'))

    context = {'form': form}
    return render(request, 'marine/new_book.html', context)


def congrats(request):
    return render(request, 'marine/congrats.html', {})


def create_and_download_declaration(request):
    """Strona po przesłaniu formularza oraz wygenerowanie deklaracji"""
    # Pobiera id miejsca postoju którego dotyczy deklaracja (w c_d nie można podać 'A-02' tylko id tego obiektu).
    id_parking_place = ParkingPlace.objects.get(parking_place=parking_place_form).id
    c_d = EntryData.objects.get(parking_place=id_parking_place)
    parking_place = str(c_d.parking_place)
    date = str(c_d.date)
    yacht = {'name': c_d.name_yacht, 'registration_number': c_d.registration_number, 'home_port': c_d.home_port,
             'length': c_d.yacht_length, 'width': c_d.yacht_width, 'ytype': c_d.yacht_type}
    fee = {'parking_fee': 8000, 'quarter_fee': 2000}

    fee_words = zl_to_words.say_int(floor(fee['parking_fee']))
    # str(x%1)[2:4]
    owner_details = {'name': c_d.owner_details_name, 'address': c_d.owner_details_address}
    parking_period = {'from': c_d.parking_period_from.strftime("%d.%m.%Y"),
                      'to': c_d.parking_period_to.strftime("%d.%m.%Y")}
    commissioning_body = {'name': c_d.commissioning_body_name, 'address': c_d.commissioning_body_address,
                          'tel': c_d.commissioning_body_tel, 'e-mail': c_d.commissioning_body_email,
                          'nip': c_d.commissioning_body_nip}
    # Domyślnie False, ponieważ większości jachtów nie dotyczy
    chip_card = c_d.chip_card
    document = Document('externals/apps/declarations/deklaracja.docx')
    create_declaration.create_declaration(document, parking_place, date, yacht, fee, owner_details, parking_period, commissioning_body, chip_card)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    filename = replace_non_ascii.removeAccents('Deklaracja_{}.docx'.format(yacht['name']))
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)
    document.save(response)
    return response



"""

Na jutro: 
- popraw rubrykę adres do korespondencji w declarations (dodatkowa zmienna) + tutaj if żeby się zgadzało 
- Dodaj i ustaw plik z obliczaniem opłaty (dokładnie!!!!)

BAARRRDZO DOBRA RRRROBOTA
"""

