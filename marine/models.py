from django.db import models
import datetime
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.exceptions import ValidationError
from django.utils.html import format_html


class ParkingPlace(models.Model):
    parking_place = models.CharField('Miejsce postoju', max_length=5)
    occupied_to = models.DateField('Zajęte do', blank=True, null=True)
    name_yacht = models.CharField('Nazwa jachtu', max_length=50, null=True, blank=True)

    def place_free(self):
        if self.occupied_to:
            return self.occupied_to <= datetime.date.today()
        else:
            return True

    place_free.boolean = True
    place_free.short_description = 'STATUS'

    def check_it(self):
        if self.occupied_to and self.occupied_to <= datetime.date.today():
            return format_html('<color style="color: red">KONIEC REZERWACJI</span>')

    def __str__(self):
        if self.check_it:
            return self.parking_place


YACHT_TYPE_CHOICES = (
    ('żaglowy', 'ŻAGLOWY'),
    ('motorowy', 'MOTOROWY'),
)


class EntryData(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    parking_place = models.OneToOneField(ParkingPlace, on_delete=models.CASCADE, verbose_name='Miejsce postoju')
    date = models.DateField(auto_now_add=True)
    name_yacht = models.CharField(max_length=30, verbose_name='Nazwa jachtu')
    registration_number = models.CharField(max_length=30, verbose_name='Numer rejestracyjny')
    home_port = models.CharField(max_length=30, verbose_name='Port macierzysty')
    yacht_length = models.FloatField(verbose_name='Długość jachtu')
    yacht_width = models.FloatField(verbose_name='Szerokość jachtu')
    yacht_type = models.CharField(max_length=20, choices=YACHT_TYPE_CHOICES, default='typ', verbose_name='Typ jachtu')
    owner_details_name = models.CharField(max_length=30, verbose_name='Imie i nazwisko właściciela jednostki')
    owner_details_address = models.CharField(max_length=100, verbose_name='Adres właściciela jednostki')
    commissioning_body_name = models.CharField(max_length=100, verbose_name='Podmiot zlecający umowę')
    commissioning_body_address = models.CharField(max_length=100, verbose_name='Adres')
    commissioning_body_tel = models.CharField(max_length=30, verbose_name='Numer telefonu')
    commissioning_body_email = models.EmailField(max_length=30, verbose_name='E-mail')
    commissioning_body_nip = models.CharField(max_length=30, verbose_name='NIP')
    parking_period_from = models.DateField(null=True, verbose_name='Postój od')
    parking_period_to = models.DateField(null=True, verbose_name='Postój do')
    chip_card = models.BooleanField(default=False, verbose_name='Karta chipowa')
    email_confirm = models.BooleanField(default=False, verbose_name='Potwierdzony mail')

    def check_it(self):
        if self.parking_period_to <= datetime.date.today():
            return format_html('<color style="color: red">KONIEC REZERWACJI</span>')

    check_it.short_description = ''

    def clean(self):
        super().clean()
        date_from = self.parking_period_from
        date_to = self.parking_period_to
        if date_from > date_to:
            raise ValidationError('"Postój" do musi być później niż "Postój od"!')

    def save(self, *args, **kwargs):
        super(EntryData, self).save(*args, **kwargs)
        parking_place = self.parking_place
        parking_place.occupied_to = self.parking_period_to
        parking_place.name_yacht = self.name_yacht
        parking_place.save()

    def __str__(self):
        return '{} {}'.format(self.parking_place, self.name_yacht)

    @receiver(pre_delete)
    def mymodel_delete(sender, instance, **kwargs):
        d = ParkingPlace.objects.get(parking_place=instance.parking_place)
        d.name_yacht = None
        d.occupied_to = None
        d.save()
