from django import forms

from .models import EntryData


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
        ]
        # W ten sposób dodajemy widgety aby ładnie dorobić potem frontend
        widgets = {'name_yacht': forms.TextInput(attrs={'class': 'name_yacht', 'placeholder': 'np. Sunrisse'})}