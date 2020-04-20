from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import ParkingPlace, EntryData
from .forms import EntryDataForm

from program_marine_django.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from externals.apps import replace_non_ascii, count_parking_fee
from externals.apps.declarations import create_declaration

from slownie import slownie_zl100gr

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

            # Send email (booking confirmation)
            # -----------------------------------------

            subject = 'Dziękujemy za złożenie rezerwacji w naszej marinie!'
            context = {'name': place.owner_details_name, 'parking_place': parking_place,
                       'parking_period_from': place.parking_period_from.strftime("%d.%m.%Y"),
                       'parking_period_to': place.parking_period_from.strftime("%d.%m.%Y"),
                       'secret_key_email': place.secret_key_email,
                       }
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)

            recipient = place.commissioning_body_email
            send_mail(subject, plain_message, EMAIL_HOST_USER, [recipient], html_message=html_message)
            # -----------------------------------------

            secret_key = place.secret_key
            return HttpResponseRedirect(reverse('marine:congrats', args=[secret_key]))

    context = {'form': form, 'parking_place_id': parking_place_id}
    return render(request, 'marine/new_book.html', context)


def congrats(request, secret_key):
    return render(request, 'marine/congrats.html', {'secret_key': secret_key})


def create_and_download_declaration(request, secret_key):
    """Strona po przesłaniu formularza oraz wygenerowanie deklaracji"""
    entry_data = get_object_or_404(EntryData, secret_key=secret_key)
    parking_place = str(entry_data.parking_place)
    date = str(entry_data.date)
    yacht = {'name': entry_data.name_yacht, 'registration_number': entry_data.registration_number,
             'home_port': entry_data.home_port, 'length': entry_data.yacht_length, 'width': entry_data.yacht_width,
             'ytype': entry_data.yacht_type}
    fee = {'parking_fee': count_parking_fee.count_parking_fee(entry_data.parking_period_from,
                                                              entry_data.parking_period_to, yacht)}
    fee_words = slownie_zl100gr(fee['parking_fee'])
    owner_details = {'name': entry_data.owner_details_name, 'address': entry_data.owner_details_address}
    parking_period = {'from': entry_data.parking_period_from, 'to': entry_data.parking_period_to}

    commissioning_body = {'name': entry_data.commissioning_body_name, 'address': entry_data.commissioning_body_address,
                          'tel': entry_data.commissioning_body_tel, 'e-mail': entry_data.commissioning_body_email,
                          'nip': entry_data.commissioning_body_nip}
    chip_card = entry_data.chip_card
    document = Document('externals/apps/declarations/deklaracja.docx')
    create_declaration.create_declaration_resident(document, parking_place, date, yacht, fee, fee_words, owner_details,
                                                   parking_period, commissioning_body, chip_card)

    # Download file (declaration)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    filename = replace_non_ascii.removeAccents('Deklaracja_{}.docx'.format(yacht['name']))
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(filename)
    document.save(response)
    return response


def confirm_email(request, secret_key_email):
    entry_data = get_object_or_404(EntryData, secret_key_email=secret_key_email)
    entry_data.email_confirm = True
    entry_data.save()
    return render(request, 'marine/email_confirm.html', {})
