from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from allauth.account.views import LoginView, LogoutView

# Create your views here.
from webapp.forms import ContactForm, CustomSignupForm, EditProfileForm, CheckoutForm, ProfessionalSignupForm
from webapp.models import Contact, Task, CustomUser, Employer, Employee


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
    return render(request, "appointment_booking.html", context)


def city_view(request, city):
    tasks = Task.objects.filter(city=city)
    context = {
        'tasks': tasks,
        'city': city
    }
    return render(request, "cities.html", context)


def exists(obj):
    if obj:
        return True
    else:
        return False


def profile_view(request):
    context = {}
    print(request.user.email)
    user_object = CustomUser.objects.get(email=request.user.email)
    try:
        employer_object = Employer.objects.get(email=user_object)
        if employer_object:
            context = {
                '    type': 'employer',
                'employer': employer_object
            }
    except:
        pass

    try:
        employee_object = Employee.objects.filter(email=user_object)
        if employee_object:
            context = {
                'type': 'employee',
                'employee': employee_object
            }

    except:
        pass

    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phno = form.cleaned_data['phno']
            address = form.cleaned_data['address']
            user = CustomUser.objects.get(email=request.user)

            # if exists(user):
            #     pass

            employer = Employer.objects.filter(email=user)
            if employer:
                employer.update(address=address)

            else:
                employer_new = Employer(email=user, address=address)
                employer_new.save()

            user.name = name
            user.email = email
            user.phno = phno
            user.save()
            # print(form.__dict__)
            print(form.errors)

            obj, created = CustomUser.objects.update_or_create(
                name=name, email=email, phno=phno,
                # defaults={'first_name': 'Bob'},
            )
            obj.save()
            # return redirect('/profile/')

        else:
            print(form.errors)
            # print(form.__dict__)

    return render(request, "profile.html", context)


def appointment_booking_view(request, city, category):
    city = city
    category = category
    user = CustomUser.objects.get(email=request.user)
    employer = Employer.objects.get(email=user)
    context = {
        'city': city,
        'category': category,
        'employer': employer
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phno = form.cleaned_data['phno']
            address = form.cleaned_data['address']
            category1 = form.cleaned_data['category']
            city = form.cleaned_data['city']
            time_preference = form.cleaned_data['preference']
            user = CustomUser.objects.get(email=request.user)
            description = form.cleaned_data['description']
            # employer = Employer(email=user, address=address)
            employer = Employer.objects.get(email=user)
            if employer:
                address = address
                category = category1
                time_preference = time_preference
                city = city
                description = description
                task = Task(
                    employer=employer,
                    category=category,
                    time_prefence=time_preference
                    # TODO
                )
            print(form.__dict__)

        else:
            print(form.errors)

    return render(request, "appointment_booking.html", context)


@login_required
def professional_signup_view(request):
    if request.method == 'POST':
        form = ProfessionalSignupForm(request.POST)
        if form.is_valid():
            experience = form.cleaned_data['experience']
            category = form.cleaned_data['category']
            user = CustomUser.objects.get(email=request.user)
            employee = Employee(email=user, category=category, experience=experience)
            employee.save()
            return redirect('/')
            pass

        else:
            print(form.errors)

    return render(request, "account/professional_signup.html")
