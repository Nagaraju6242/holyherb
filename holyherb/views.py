from django.shortcuts import render
from customization.models import Recipe,HomePageBanner,Handpicked,HomePageIngredientIndex,Herobanner,HowDoWeDoIt
from orders.models import Coupon

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    homepagebanner = None
    recipe = None
    ii_home = HomePageIngredientIndex.objects.all()
    hdwdi = HowDoWeDoIt.objects.all()
    if(hdwdi.exists()):
        hdwdi = hdwdi.first()
    if(HomePageBanner.objects.all().exists()):
        homepagebanner = HomePageBanner.objects.order_by("?").first()
    if(Recipe.objects.all().exists()):
        recipe = Recipe.objects.order_by("?").first()
    handpicked = Handpicked.objects.all()
    herobanners = Herobanner.objects.all()
    data = {
        "recipe" : recipe,
        "homepagebanner" : homepagebanner,
        "handpicked" : handpicked,
        "ii_home":ii_home,
        "herobanners":herobanners,
        "hdwdi" : hdwdi,
    }
    response = render(request,'home.html',data)
    offerBannerDismissed = request.COOKIES.get('offerBannerDismissed',None)
    if(not offerBannerDismissed and homepagebanner):
        response.set_cookie("offerBannerDismissed","false",max_age=3600 * 24 * 10)
    return response

def coupons(request):
    coupons = Coupon.objects.all()
    return render(request,'coupons.html',{"coupons":coupons})

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def offline(request):
    return render(request,"offline.html")
