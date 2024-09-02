from django.shortcuts import redirect, render
from .forms import ApplicationForm
from .models import Form
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.core.mail import send_mail

from pathlib import Path
# import environ
from decouple import config

# Initialize environment variables
# env = environ.Env()
# environ.Env.read_env()

def index(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)  # include request.FILES for file uploads
        if form.is_valid():
            # Create the Form object manually
            form_instance = Form(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                date=form.cleaned_data["date"],
                occupation=form.cleaned_data["occupation"],
                cv=form.cleaned_data["cv"]
            )
            form_instance.save()

            # Send confirmation email
            first_name = form.cleaned_data["first_name"]
            email = form.cleaned_data["email"]
            message_body = f"Your Application for Python Developer is Successfully Submitted. Thank you! \n{first_name}"
            email_message = EmailMessage("Confirmation of Application Submission", message_body, to=[email]) 
            email_message.send()

            messages.success(request, "Submission Success!")
        else:
            messages.error(request, "Submission Failed. Please correct the errors and try again.")
    else:
        form = ApplicationForm()

    return render(request, "index.html", {'form': form})


def about(request):
    return render(request, "about.html")



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                f"Contact Form Submission from {name}",
                message,
                email,
                # [env('EMAIL_HOST_USER'),], 
                [config('EMAIL_HOST_USER'),], 
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
