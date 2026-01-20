from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# def contact(request):
#     return HttpResponse("This is the Contact Page")


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .forms import ContactForm
from .models import ContactInfo


def contact(request):

    contact_info = ContactInfo.objects.filter(is_active=True).first()

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save()

            # ================= ADMIN EMAIL =================
            admin_html = render_to_string(
                "emails/contact_admin.html",
                {"contact": contact}
            )

            admin_email = EmailMultiAlternatives(
                subject="New Contact Message",
                body="New contact received",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
            )
            admin_email.attach_alternative(admin_html, "text/html")
            admin_email.send(fail_silently=True)

            messages.success(request, "Your message has been sent successfully.")
            return redirect("contact")

    else:
        form = ContactForm()

    return render(request, "contact.html", {
        "form": form,
        "contact_info": contact_info
    })
