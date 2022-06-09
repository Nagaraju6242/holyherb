from addresses.models import Address
from django.shortcuts import redirect, render
from .forms import AddressForm
from accounts.models import JoinOurCircle
from django.http import JsonResponse

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    subscribe = request.POST.get("newsletter",None)
    if subscribe:
        email = request.POST.get("email",None)
        if(email):
            qs = JoinOurCircle.objects.filter(email=email)
            if(not qs.exists()):
                JoinOurCircle.objects.create(email=email)

    if form.is_valid():
        number = form.cleaned_data.get("phone_number")
        pincode = form.cleaned_data.get("postal_code")
        print(number,pincode)
        try:
            pincode = int(pincode)
        except:
            return JsonResponse({
                "added" : False,
                "error" : "Invalid Pincode"
            })
        try:
            number = int(number)
        except:
            return JsonResponse({
                "added" : False,
                "error" : "Invalid Phone Number"
            })
        print(number,pincode)
        if(len(str(number)) == 10):
            if(len(str(pincode)) == 6):
                instance = form.save(commit=False)
                if request.user.is_authenticated:
                    instance.user = request.user
                instance.save()
                request.session["shipping_address_id"] = instance.id
            else:
                return JsonResponse({
                "added" : False,
                "error" : "Invalid Pincode"
            })
        else:
            return JsonResponse({
                "added" : False,
                "error" : "Invalid Phone Number"
            })
    return JsonResponse({
                "added" : True,
                "error" : ""
            })

def checkout_address_reuse_view(request):
    if request.method == "POST":
        shipping_address = request.POST.get('shipping_address',None)
        if shipping_address is not None:
            qs = Address.objects.filter(id=shipping_address,user=request.user)
            if qs.exists():
                request.session["shipping_address_id"] = shipping_address

    return redirect("checkout")
    
    
