from django import forms
from django.forms import ModelForm


class SearchForm(forms.Form):
    latitude = forms.FloatField(label='Latitude', min_value=-30, max_value=90)
    longitude = forms.FloatField(
        label='Longitude', min_value=-120, max_value=120)
