from allauth.account.views import SignupView
from django.shortcuts import render

from allauth.account.views import LoginView

# Create your views here.
from webapp.forms import ContactForm, CustomSignupForm, EditProfileForm
from webapp.models import Contact, Task, CustomUser, Employer


def landing_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.__dict__)
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            name = form.cleaned_data['name']
            contact = Contact(
                email=email,
                name=name,
                message=message,
            )
            contact.save()
    return render(request, "index.html")


def customer_dashboard_view(request):
    return render(request, "dashboard.html")


def employee_dashboard_view(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, "dashboard.html", context)


def test_view(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, "contact.html", context)


def city_view(request, city):
    tasks = Task.objects.filter(city=city)
    context = {
        'tasks': tasks
    }
    return render(request, "cities.html", context)


def profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phno = form.cleaned_data['phno']
            address = form.cleaned_data['address']
            user = CustomUser.objects.get(email=request.user)
            employer = Employer(email=user, address=address)
            user.name = name
            user.email = email
            user.phno = phno
            user.save()
            employer.save()
            print(form.__dict__)

        else:
            print(form.errors)
            # print(form.__dict__)

    return render(request, "profile.html")
