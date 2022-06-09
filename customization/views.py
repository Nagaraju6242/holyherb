from django.shortcuts import render
from .models import Miscellaneous
import markdown

# Create your views here.
def privacy_policy(request):
    try:
        pp = Miscellaneous.objects.filter(name="privacy_policy").first()
    except:
        pp = None
    return render(request,"customization/privacy_policy.html",{"data":pp})

def terms_and_conditions(request):
    try:
        tandc = Miscellaneous.objects.filter(name="terms_and_conditions").first()
    except:
        tandc = None
    return render(request,"customization/privacy_policy.html",{"data":tandc})

def faq(request):
    md = markdown.Markdown()
    try:
        faq = Miscellaneous.objects.filter(name="FAQ").first()
        data = {
            "name" : faq.name,
            "title" : faq.title,
            "description" : md.convert(faq.description),
        }
    except:
        faq = None
        data = {}

    return render(request,"customization/privacy_policy.html",{"data" : data})