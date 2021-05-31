from allauth.account.forms import SignupForm, LoginForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'name', 'phno')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        # Call the init of the parent class
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(required=True)
        self.fields['phno'] = PhoneNumberField(required=True)
        self.fields['address'] = forms.CharField(required=True)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['phno'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    # # Put in custom signup logic
    # def custom_signup(self, request, user):
    #     # Set the user's type from the form reponse
    #     user.email = self.cleaned_data["email"]
    #     user.name = self.cleaned_data["name"]
    #     user.phno = self.cleaned_data["phno"]
    #     user.password = self.cleaned_data["password1"]
    #     # user.save()
    #     user = super(CustomSignupForm, self).save(request)
    #     return user

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.

        user = super(CustomSignupForm, self).save(request)
        phno = self.cleaned_data['phno']
        name = self.cleaned_data['name']
        user.phno = phno
        user.name = name
        user.save()
        # Add your own processing here.

        # You must return the original result.
        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['remember'].widget.attrs['class'] = 'form-check-input'

    def login(self, *args, **kwargs):
        return super(CustomLoginForm, self).login(*args, **kwargs)


class EditProfileForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    experience = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-select"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    phno = PhoneNumberField(widget=forms.TextInput(attrs={"class": "form-control"}))


class ContactForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.CharField(required=True)
    message = forms.CharField(required=True)


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.CharField(widget=forms.TextInput(attrs={"class": "form-select"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-select"}))
    time_preference = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-select"}))


class ProfessionalSignupForm(forms.Form):
    experience = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    category = forms.CharField(widget=forms.TextInput(attrs={"class": "form-select"}))


class ProfileCreationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phno = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))


class SubmitServiceRequestForm(forms.Form):
    task_id = forms.CharField(required=True)


class AssignServiceRequestForm(forms.Form):
    request_id = forms.CharField(required=True)
    employee_id = forms.CharField(required=True)
