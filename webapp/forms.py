from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser, Employer


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'name', 'phno')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class EmployeeSignupForm(SignupForm):


    # def save(self, request):
    #     user = super(EmployerSignupForm, self).save(request)
    #     employer = Employer(
    #         email=user,
    #         experience=self.cleaned_data.get('experience')
    #
    #     )
    #     employer.save()
    #     return employer.email
    experience = forms.IntegerField(required=True, label=_("Experience"))
    name = forms.CharField(max_length=55, label=_("Name"))
    email = forms.CharField(max_length=55, label=_("Email"))
    phno = forms.CharField(max_length=12, label=_("Mobile"))

    class Meta:
        fields = ("name", "email", "phno", "email", "password"), "experience"

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(EmployeeSignupForm, self).save(request)

        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.phno = self.cleaned_data.get('phno')
        user.experience = self.cleaned_data.get("experience")
        user.save()

        # You must return the original result.
        return user


# class MyCustomLoginForm(LoginForm):
#
#     def login(self, *args, **kwargs):
#         # Add your own processing here.
#         super(MyCustomLoginForm, self).__init__(*args, **kwargs)
#         self.fields['login'].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget.attrs['class'] = 'form-control'
#         self.fields['remember'].widget.attrs['class'] = 'form-control'
#
#         # You must return the original result.
#         return super(MyCustomLoginForm, self).login(*args, **kwargs)

class CustomLoginForm(LoginForm):
    def __init__(self,*args,**kwargs):
        super(CustomLoginForm,self).__init__(*args,**kwargs)
        self.fields['login'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['remember'].widget.attrs['class'] = 'form-check-input'

    def login(self, *args, **kwargs):
        return super(CustomLoginForm, self).login(*args, **kwargs)


class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.CharField(required=True)
    message = forms.CharField(required=True)
