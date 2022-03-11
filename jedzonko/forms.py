import django.forms as forms
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.models import User


class LogForms(forms.Form):
    login = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


def validate_login(value):
    users = User.objects.filter(username=value)
    if len(users) > 0:
        raise ValidationError("Ten login jest już zajęty")


class AddUser(forms.Form):
    login = forms.CharField(label="Nazwa użytkownika", max_length=100, validators=[validate_login])
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)
    name = forms.CharField(label="Imię", max_length=100)
    surname = forms.CharField(label="Nazwisko", max_length=100)
    email = forms.EmailField(label="Adres email")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_repeat = cleaned_data['password_repeat']
        if password != password_repeat:
            raise ValidationError("Hasło nie jest takie samo")


class ResetPass(forms.Form):
    old_password = forms.CharField(label="Aktualne hasło", widget=forms.PasswordInput)
    password = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_repeat = cleaned_data['password_repeat']
        if password != password_repeat:
            raise ValidationError("Hasło nie jest takie samo")