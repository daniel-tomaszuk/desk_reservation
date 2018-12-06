
from django import forms
from django.forms import SelectDateWidget


class DateForm(forms.Form):
    date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )
