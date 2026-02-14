from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def cms(request):
    return HttpResponse("This is the cms Page")



from django.shortcuts import render


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def terms_conditions(request):
    return render(request, "pages/terms_condition.html")


def refund_policy(request):
    return render(request, "pages/refund_policy.html")
