from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import ParkingPlace, EntryData
from .forms import EntryDataForm

from externals.apps import replace_non_ascii
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
    owner_details = {'name': c_d.owner_details_name, 'address': c_d.owner_details_address}
    parking_period = {'from': c_d.parking_period_from.strftime("%d.%m.%Y"),
                      'to': c_d.parking_period_to.strftime("%d.%m.%Y")}
    commissioning_body = {'name': c_d.commissioning_body_name, 'address': c_d.commissioning_body_address,
                          'tel': c_d.commissioning_body_tel, 'e-mail': c_d.commissioning_body_email,
                          'nip': c_d.commissioning_body_nip}
    # Domyślnie False, ponieważ większości jachtów nie dotyczy
    chip_card = c_d.chip_card
    media = False
    # Sprawdza czy jacht stoi na kei nieopomiarowanej (dodatkowa opłata za media).
    if 'D' in parking_place:
        media = True

    document = Document('externals/apps/create_declaration/deklaracja.docx')

    for paragraph in document.paragraphs:
        if 'Miejsce postojowe' in paragraph.text:
            paragraph.text = 'Miejsce postojowe {}                                                               ' \
                             '                                        ' \
                             'Data {}'.format(parking_place, date)

    document.add_paragraph('\n')
    document.add_paragraph('Nazwa jachtu: ', style='List Number').add_run(yacht['name']).bold = True
    document.add_paragraph('Nr rejestracyjny: ', style='List Number').add_run(
        yacht['registration_number']).bold = True
    document.add_paragraph('Port macierzysty: ', style='List Number').add_run(
        yacht['home_port']).bold = True
    document.add_paragraph('Dane jachtu: ', style='List Number')
    p = document.add_paragraph('            Długość: ')
    p.add_run(str(yacht['length'])).bold = True
    p.add_run(' m')
    p.add_run('             Szerokość: ')
    p.add_run(str(yacht['width'])).bold = True
    p.add_run(' m')
    document.add_paragraph('Typ jachtu: ', style='List Number').add_run(yacht['ytype']).bold = True
    document.add_paragraph('Dane właściciela* lub użytkownika jachtu*: ', style='List Number')
    document.add_paragraph('            - imię i nazwisko: ').add_run(owner_details['name']).bold = True
    document.add_paragraph('            - adres : ').add_run(owner_details['address']).bold = True
    document.add_paragraph('Dane armatora: ', style='List Number')
    document.add_paragraph('            - imię i nazwisko: ').add_run(owner_details['name']).bold = True
    document.add_paragraph('            - adres : ').add_run(owner_details['address']).bold = True
    document.add_paragraph('Podmiot zlecający, podpisujący umowę na postój jachtu: ', style='List Number')
    document.add_paragraph('            - nazwisko imię */ pełna nazwa klubu lub firmy: ').add_run(
        commissioning_body['name']).bold = True
    document.add_paragraph('            - adres: ').add_run(commissioning_body['address']).bold = True
    document.add_paragraph('            - tel: ').add_run(commissioning_body['tel']).bold = True
    document.add_paragraph('            - E-mail: ').add_run(commissioning_body['e-mail']).bold = True

    document.add_paragraph('            - NIP klubu/stowarzyszenia: ').add_run(
        commissioning_body['nip']).bold = True
    document.add_paragraph('Deklarowany okres i czas postoju: ', style='List Number')
    document.add_paragraph('            - od dnia: ').add_run(parking_period['from']).bold = True
    document.add_paragraph('            - do dnia: ').add_run(parking_period['to']).bold = True
    document.add_paragraph('')
    document.add_paragraph('Opłata za postój wynosi: ', style='List Number').add_run(
        str(fee['parking_fee'])).bold = True
    document.add_paragraph(
        'Czynsz płatny, zgodnie z wystawioną fakturą z góry, jednorazowo lub w czterech poniższych '
        'ratach za każdy kwartał do:')
    document.add_paragraph('      I. 15.05.2020, w kwocie: ').add_run(str(fee['quarter_fee'])).bold = True
    document.add_paragraph('     II. 15.08.2020, w kwocie: ').add_run(str(fee['quarter_fee'])).bold = True
    document.add_paragraph('    III. 15.11.2020, w kwocie: ').add_run(str(fee['quarter_fee'])).bold = True
    document.add_paragraph('    IV. 15.21.2020, w kwocie: ').add_run(str(fee['quarter_fee'])).bold = True
    document.add_paragraph('na rachunek Wynajmującego o nr  88 1030 1117 0000 0000 8899 5007.')
    document.add_paragraph('Adres do korespondencji: ', style='List Number').add_run(
        owner_details['address']).bold = True
    document.add_paragraph('Karta chipowa: ', style='List Number').add_run(chip_card).bold = True
    if media:
        p = document.add_paragraph('Dodatkowo zlecone usługi: ', style='List Number')
        p.add_run('184zł - miejsce postojowe na wodzie nieopomiarowane').bold = True
    document.add_paragraph('Miejsce postoju nr: ', style='List Number').add_run(parking_place).bold = True
    document.add_paragraph(
        '\nUprzejmie informujemy, że w trakcie postoju jachtu na przystani NCŻ AWFiS może zaistnieć '
        'konieczność zmiany miejsca lokalizacji postoju jachtu na inne zgodnie z ze wskazaniem '
        'upoważnionego pracownika przystani.\n\n'
        'Oświadczam, iż zapoznałem się z Regulaminem przystani Narodowego Centrum Żeglarstwa AWFiS '
        'Gdańsku, w tym zawarcia umowy na postój. W pełni go akceptuję co poświadczam własnoręcznym '
        'podpisem pod Deklaracją postoju. Oświadczam, iż w przypadku okresu postoju krótszego niż '
        'zadeklarowany (wynikający m.in. ze sprzedaży jachtu) mam świadomość, że stawka będzie '
        'rekalkulowana do krótszego okresu postoju, zgodnie z obowiązującym cennikiem.\n\n').paragraph_format.alignment = 3
    document.add_paragraph(".........................................................				 .........."
                           "...............................................").add_run(
        '   podpis pracownika NCŻ                                                                                 '
        '             podpis (imię, nazwisko)').italic = True

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    filename = replace_non_ascii.removeAccents('Deklaracja_{}.docx'.format(yacht['name']))
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)
    document.save(response)
    return response



"""
Na jutro: 
- popraw rubrykę adres do korespondencji w create_declaration (dodatkowa zmienna) + tutaj if żeby się zgadzało 
- Dodaj i ustaw plik z obliczaniem opłaty (dokładnie!!!!)

BAARRRDZO DOBRA RRRROBOTA
"""

