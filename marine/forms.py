from django import forms

from .models import EntryData

import datetime



class EntryDataForm(forms.ModelForm):
    class Meta:
        model = EntryData
        fields = [
            'name_yacht',
            'registration_number',
            'home_port',
            'yacht_length',
            'yacht_width',
            'yacht_type',
            'owner_details_name',
            'owner_details_address',
            'commissioning_body_name',
            'commissioning_body_address',
            'commissioning_body_tel',
            'commissioning_body_email',
            'commissioning_body_nip',
            'parking_period_from',
            'parking_period_to',
            'correspondence_address',
            'chip_card'
        ]
        # W ten sposób dodajemy widgety aby ładnie dorobić potem frontend
        widgets = {
            'name_yacht': forms.TextInput(attrs={'class': 'name_yacht', 'placeholder': 'np. Sunrisse'}),
            'parking_period_from': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),
            'parking_period_to': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today()}),

        }


"""
Usuń możliwość wybrania niemożliwego okresu od przyszłości do przeszłości!
"""