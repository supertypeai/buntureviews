from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )
    email = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Email"})
    )
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-registrationForm"
        self.helper.form_class = "registrationForm"
        self.helper.form_method = "post"
        # self.helper.form_show_errors = True
