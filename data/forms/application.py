from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AddApplicationForm(forms.Form):
    app_id = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "App ID"})
    )
    country = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Country"})
    )

