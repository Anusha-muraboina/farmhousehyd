from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Booking


@shared_task
def send_booking_reminders():

    tomorrow = timezone.localdate() + timedelta(days=1)

    bookings = Booking.objects.filter(check_in=tomorrow)

    print(f"Total bookings found: {bookings.count()}")

    for booking in bookings:

        email = booking.guest_email

        print(f"Sending reminder to: {email}")

        subject = "Farmhouse Booking Reminder"

        html_content = render_to_string(
            "emails/booking_reminder.html",
            {
                "booking": booking
            }
        )

        msg = EmailMultiAlternatives(
            subject,
            "Your farmhouse booking is tomorrow.",
            None,
            [email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print(f"Reminder sent successfully to: {email}")