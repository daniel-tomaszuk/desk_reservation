import datetime

from django import forms


class DateForm(forms.Form):
    date = forms.DateField(initial=datetime.date.today)
