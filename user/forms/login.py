from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    email = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Email"})
    )
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-loginForm"
        self.helper.form_class = "loginForms"
        self.helper.form_method = "post"
        # self.helper.form_action = "submit_survey"

        # self.helper.add_input(Submit("submit", "Submit"))

