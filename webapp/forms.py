from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Employer


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'name', 'phno')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class EmployerSignupForm(SignupForm):
    experience = forms.IntegerField(required=True)

    def save(self, request):
        user = super(EmployerSignupForm, self).save(request)
        employer = Employer(
            email=user,
            experience=self.cleaned_data.get('experience')

        )
        employer.save()
        return employer.email


class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.CharField(required=True)
    message = forms.CharField(required=True)
