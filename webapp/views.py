from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from webapp.forms import ContactForm, EditProfileForm, CheckoutForm, ProfessionalSignupForm, ProfileCreationForm
from webapp.models import Contact, Task, CustomUser, Employee


def landing_view(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user.email)
        if user.name is None:
            return redirect('/accounts/profile/create')
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
        else:
            print(form.errors)
    return render(request, "index.html")


def customer_dashboard_view(request):
    return render(request, "dashboard.html")


def employee_dashboard_view(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks
    }
    return render(request, "dashboard.html", context)


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

            user.name = name
            user.email = email
            user.phno = phno
            user.address = address
            user.save()
            print(form.errors)

            obj, created = CustomUser.objects.update_or_create(
                name=name, email=email, phno=phno,
            )
            obj.save()

        else:
            print(form.errors)

    return render(request, "profile.html", context)


@login_required
def appointment_booking_view(request, city, category):
    city = city
    category = category
    if CustomUser.objects.get(email=request.user):
        user = CustomUser.objects.get(email=request.user)
        context = {
            'city': city,
            'category': category,
            'employer': user
        }
    else:
        return redirect('/success')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            address = form.cleaned_data['address']
            category1 = form.cleaned_data['category']
            city = form.cleaned_data['city']
            time_preference = form.cleaned_data['time_preference']
            user = CustomUser.objects.get(email=request.user)
            description = form.cleaned_data['description']
            # employer = Employer(email=user, address=address)
            user = CustomUser.objects.get(email=user)
            if user:
                address = address
                category = category1
                time_preference = time_preference
                city = city
                description = description
                task = Task(
                    employer=user,
                    category=category,
                    address=address,
                    city=city,
                    description=description,
                    preference=time_preference
                    # TODO
                )
                task.save()
                return redirect('/success')
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


def success_view(request):
    return render(request, 'success.html')


@login_required
def profile_creation_view(request):
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            phno = form.cleaned_data['phno']
            phno = str(phno) + '91'
            user = CustomUser.objects.get(email=request.user.email)
            user.name = name
            user.phno = phno
            user.address = address
            user.save()
            return redirect('/success')
        else:
            print(form.errors)

    return render(request, 'account/profile_creation.html')

