from allauth.account.views import SignupView
from django.shortcuts import render

from allauth.account.views import LoginView

# Create your views here.
from webapp.forms import ContactForm, EmployeeSignupForm
from webapp.models import Contact, Task


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


# def employer_signup(SignupView):
#     return render(request, "employer_signup.html")

class EmployeeSignupView(SignupView):
    template_name = "account/employer_signup.html"
    form_class = EmployeeSignupForm
    view_name = "employer_signup"


employee_signup = EmployeeSignupView.as_view()


# def login_test_view(request):
#     return render(request, "login_new.html")
#
#
# def signup_test_view(request):
#     return render(request, "signup_new.html")


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

