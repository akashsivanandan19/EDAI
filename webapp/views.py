from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import DetailView

from webapp.forms import ContactForm, EditProfileForm, CheckoutForm, ProfessionalSignupForm, ProfileCreationForm, \
    SubmitServiceRequestForm, AssignServiceRequestForm, TaskUpdateForm
from webapp.models import Contact, Task, CustomUser, Employee, ServiceRequest


def landing_view(request):
    context = None
    if check_employee(request):
        employee = Employee.objects.get(email=CustomUser.objects.get(email=request.user.email))
        context = {
            'employee': employee
        }
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
    return render(request, "index.html", context)


@login_required
def customer_dashboard_view(request):
    user = CustomUser.objects.get(email=request.user.email)
    tasks = Task.objects.filter(employer=user)
    employees = Employee.objects.all()
    # employees = Employee.objects.filter()

    context = {
        'tasks': tasks,
        'user': user,
        'employees': employees
    }

    return render(request, "dashboard.html", context)


def employee_dashboard_view(request):
    if request.method == 'POST':
        form = SubmitServiceRequestForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['task_id']
            task = Task.objects.get(id=task_id)
            service_request = ServiceRequest()
            service_request.task = task
            service_request.request_placed_employee = Employee.objects.get(
                email=CustomUser.objects.get(email=request.user.email))
            service_request.save()
        else:
            print(form.errors)

    user = CustomUser.objects.get(email=request.user.email)
    employee = Employee.objects.get(email=user)
    tasks = Task.objects.filter(category=employee.category)
    context = {
        'employee': employee,
        'user': user,
        'tasks': tasks
    }
    return render(request, "staff_dashboard.html", context)


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
        employee_object = Employee.objects.get(email=user_object)
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
            experience = form.cleaned_data['experience']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            user = CustomUser.objects.get(email=request.user.email)
            employee = Employee.objects.get(email=user)

            user.name = name
            user.email = email
            user.phno = phno

            user.address = address
            user.city = city

            employee.experience = experience

            employee.save(update_fields=['experience'])
            user.save()
            print(form.errors)

            obj, created = CustomUser.objects.update_or_create(
                name=name, email=email, phno=phno,
            )
            obj.save()
            return redirect('/success')

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
    context = None
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user.email)
        context = {
            'user': user
        }
        if check_employee(request):
            employee = Employee.objects.get(email=user)
            context['employee'] = employee
    return render(request, 'success.html', context)


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


def check_employee(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user.email)
        try:
            employee_object = Employee.objects.filter(email=user)
            if employee_object:
                return True
            else:
                return False


        except:
            pass


def request_view(request):
    user = CustomUser.objects.get(email=request.user.email)
    employee = Employee.objects.get(email=user)
    tasks = Task.objects.filter(category=employee.category)
    requests = ServiceRequest.objects.filter(request_placed_employee=employee)
    context = {
        'tasks': tasks,
        'employee': employee,
        'requests': requests,
    }
    return render(request, 'request_viewing.html', context)


@login_required
def request_assignment_view(request):
    user = CustomUser.objects.all()
    employee = Employee.objects.all()
    requests = ServiceRequest.objects.all()
    context = {
        'requests': requests,
        'user_item': user,
        'employee': employee
    }
    if request.method == 'POST':
        form = AssignServiceRequestForm(request.POST)
        if form.is_valid():
            employee_who_requested = form.cleaned_data['employee_id']
            request_id = form.cleaned_data['request_id']
            task = get_object_or_404(Task, pk=request_id)
            task.employee = employee_who_requested
            task.status = 'A'
            task.save()
            return redirect('/success')

    return render(request, 'request_assignment.html', context)


@login_required
def employee_task_view(request):
    user = CustomUser.objects.get(email=request.user)
    # task = get_object_or_404(Task, employee=request.user.email)
    task = Task.objects.filter(employee=request.user.email)
    context = {
        'user': user,
        'tasks': task,
    }
    if check_employee(request):
        employee = Employee.objects.get(email=user)
        context['employee'] = employee
    else:
        pass
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['task_id']
            task_status = form.cleaned_data['task_status']
            task_obj = get_object_or_404(Task, pk=task_id)
            task_obj.status = task_status
            task_obj.save()
            return redirect('/success')
        else:
            print(form.errors)
    return render(request, 'employee_tasks.html', context)
