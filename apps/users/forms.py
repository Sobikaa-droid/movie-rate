from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings

from .models import TunedUser


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = TunedUser
        fields = ["username", 'email', "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix

        self.fields['username'].help_text = 'Letters, numbers and @/./+/-/_ only.'
        self.fields['password1'].help_text = '8-20 characters, letters and numbers, no spaces.'
        self.fields['password2'].help_text = None

        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'{field.label}*'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = TunedUser
        fields = ["username", 'first_name', 'second_name', 'description', 'year_of_birth', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes ':' as label suffix

        self.fields['username'].help_text = 'Letters, numbers and @/./+/-/_ only.'

        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'{field.label}*'
