from django import forms
from django.contrib.auth.models import User
from profiles.models import Project, Time
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        }
    ))

    first_name = forms.CharField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'First name',
        }
    ))

    last_name = forms.CharField(required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
        }
    ))

    password1 = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

    password2 = forms.CharField(required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
        }
    ))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

            return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = (
            'project',
        )

class TimeForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.SelectDateWidget(
        attrs={
            'class': 'form-control',
            'placeholder': 'Select a date',
        }
    ))
    class Meta:
        model = Time
        fields = (
        'duration',
        'date',
        'description'

        )
