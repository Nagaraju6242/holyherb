from accounts.models import Wishlist
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product,Review
from carts.models import Cart
from customization.models import Option
from django.urls import reverse
from django.http import Http404
from analytics.signals import object_viewed_signal

def get_product(request,slug):
    object = get_object_or_404(Product,slug__iexact=slug)
    related_products = Product.objects.filter(category=object.category).order_by("?")[:3] 
    artistic = None
    main_image = None
    review = []
    images = {}  
    cart_number = 0 

    # Important
    # Do not use cart_obj directly any where else check existed is True before
    
    cart_obj,exsisted = Cart.objects.get_or_none(request)
    if exsisted:
        cart_number = len(cart_obj.items.all())
    view_signal_enable = Option.objects.filter(name="user_object_views")
    if(view_signal_enable.exists()):
        view_signal_enable = view_signal_enable.first().enable
    else:
        view_signal_enable = False
    try:
        artistic = object.images.filter(artistic=True)
        main_image = object.images.filter(main_image=True)
        review = [i <= object.avg_rating for i in range(1,6)]
    except:
        pass
    data = []
    try:
        li = list(object.description.split("\n"))
        for i in li:
            if ":" in i:
                temp = i.split(":")
                data.append([temp[0]," ".join(temp[1:])])
            else:
                data.append(["extra",i])
    except:
        pass
    wishlist_items = None
    if request.user.is_authenticated:
        wishlist,existed = Wishlist.objects.get_or_none(request)
        if existed:
            print("Wishlist",wishlist)
            wishlist_items = wishlist.products.all()
        else:
            wishlist_items = []
    
    if object.has_multiple_quantity_images:
        images["main_image"] = object.images.filter(main_image=True)
        images["artistic"] = object.images.filter(artistic=True)
        images["sub_main"] = []
        images["sub_left"] = []
        images["sub_right"] = []
        for i in object.quantity_price.all():
            try:
                images["sub_main"].append(object.images.filter(quantity=i).first())
            except:
                pass
        for i in object.quantity_price.all():
            try:
                images["sub_left"].append(object.images.filter(quantity=i)[1])
            except:
                pass
        for i in object.quantity_price.all():
            try:
                images["sub_right"].append(object.images.filter(quantity=i)[2])
            except:
                pass        

    context = {
        "object" : object,
        "artistic" : artistic,
        "main_image": main_image,
        "review" : review,
        "data" : data,
        "ratinglist" : [1,2,3,4,5],
        "wishlist_items" : wishlist_items,
        "related_products" : related_products,
        "images" : images,
        "cart_number" : cart_number,
     }

    if object and view_signal_enable:
        object_viewed_signal.send(object.__class__,instance=object,request=request)
    return render(request,"products/detail.html",context)


def search(request):
    try:
        q = request.GET.get('q' , None)
        lookups = Q(title__icontains=q) | Q(category__icontains=q) | Q(flavour__icontains=q) | Q(title__icontains=q.replace(" ","")) | Q(category__icontains=q.replace(" ","")) | Q(flavour__icontains=q.replace(" ",""))
        objects = Product.objects.filter(lookups).distinct()
        sort_order = request.GET.get("sort",None)
        if(sort_order in ["price-inc","price-dec","alpha-inc","alpha-dec","new-first","new-last","trending"]):
            if(sort_order == "price-inc"):
                objects = Product.objects.order_lth(objects)
            elif(sort_order == "price-dec"):
                objects = Product.objects.order_htl(objects)
            elif(sort_order == "alpha-inc"):
                objects = Product.objects.order_atz(objects,category=True)
            elif(sort_order == "alpha-dec"):
                objects = Product.objects.order_zta(objects,category=True)
            elif(sort_order == "new-first"):
                objects = Product.objects.order_nto(objects)
            elif(sort_order == "new-last"):
                objects = Product.objects.order_otn(objects)
            elif(sort_order == "trending"):
                objects = Product.objects.order_bytrending(objects)
        details = {
            "search"  : q,
            "category": "search",
            "base_url": request.path + "?q=" + q + "&",
        }
        context = {
            "details" :details,
            "objects" : objects,
            "category" : True,
            "no_nav" : True,
            "handpicked" : True,
            "sort" : sort_order,
        }
        return render(request,"products/category_view.html",context)
    except:
        return redirect("/")


def get_handpicked(request):
    sort_order = request.GET.get("sort",None)
    objects = Product.objects.filter(handpicked=True)
    if(sort_order in ["price-inc","price-dec","alpha-inc","alpha-dec","new-first","new-last","trending"]):
        if(sort_order == "price-inc"):
            objects = Product.objects.order_lth(objects)
        elif(sort_order == "price-dec"):
            objects = Product.objects.order_htl(objects)
        elif(sort_order == "alpha-inc"):
            objects = Product.objects.order_atz(objects,category=True)
        elif(sort_order == "alpha-dec"):
            objects = Product.objects.order_zta(objects,category=True)
        elif(sort_order == "new-first"):
            objects = Product.objects.order_nto(objects)
        elif(sort_order == "new-last"):
            objects = Product.objects.order_otn(objects)
        elif(sort_order == "trending"):
            objects = Product.objects.order_bytrending(objects)
    details = {
        "category": "Handpicked",
        "base_url": request.path + "?",
    }
    
    context = {
        "details" :details,
        "objects" : objects,
        "category" : True,
        "no_nav" : True,
        "handpicked" : True,
        "sort" : sort_order,
    }
    return render(request,"products/category_view.html",context)

def get_category(request,category):
    sort_order = request.GET.get("sort",None)
    if(category in ["haircare" , "facecare" , "bodycare" , "gifting"]):
        try:
            objects = Product.objects.filter(category=category)
            if(sort_order in ["price-inc","price-dec","alpha-inc","alpha-dec","new-first","new-last","trending"]):
                if(sort_order == "price-inc"):
                    objects = Product.objects.order_lth(objects)
                elif(sort_order == "price-dec"):
                    objects = Product.objects.order_htl(objects)
                elif(sort_order == "alpha-inc"):
                    objects = Product.objects.order_atz(objects,category=True)
                elif(sort_order == "alpha-dec"):
                    objects = Product.objects.order_zta(objects,category=True)
                elif(sort_order == "new-first"):
                    objects = Product.objects.order_nto(objects)
                elif(sort_order == "new-last"):
                    objects = Product.objects.order_otn(objects)
                elif(sort_order == "trending"):
                    objects = Product.objects.order_bytrending(objects)
            products = list(set([x.title for x in objects]))
            products.sort()
            details = {
                "category" : category,
                "products" : products,
                "base_url": request.path + "?",
            }
            context = {
                "details" : details,
                "objects" : objects,
                "category" : True,
                "sort" : sort_order,
            }
            return render(request,"products/category_view.html",context)
        except:
            raise  Http404
    raise  Http404

def get_category_product(request,category,product):
    sort_order = request.GET.get("sort",None)
    wishlist_items = []
    if(request.user.is_authenticated):
        wishlist,created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = wishlist.products.all()
    try:
        if(category in ["haircare" , "facecare" , "bodycare" , "gifting"]):
            product = product.replace("-"," ")
            products = list(set([x.title.lower() for x in Product.objects.filter(category__icontains=category)]))
            if(product.lower() in products):
                objects = Product.objects.filter(category__icontains=category,title__icontains=product)
                if(sort_order in ["price-inc","price-dec","alpha-inc","alpha-dec","new-first","new-last"]):
                    if(sort_order == "price-inc"):
                        objects = Product.objects.order_lth(objects)
                    elif(sort_order == "price-dec"):
                        objects = Product.objects.order_htl(objects)
                    elif(sort_order == "alpha-inc"):
                        objects = Product.objects.order_atz(objects)
                    elif(sort_order == "alpha-dec"):
                        objects = Product.objects.order_zta(objects)
                    elif(sort_order == "new-first"):
                        objects = Product.objects.order_nto(objects)
                    elif(sort_order == "new-last"):
                        objects = Product.objects.order_otn(objects)
                details = {
                    "category" : category,
                    "product" : product,
                    "products" : products,
                    "base_url": request.path + "?",
                }
                context = {
                    "details" : details,
                    "objects" : objects,
                    "wishlist_items" : wishlist_items,
                    "category" : False,
                    "sort" : sort_order,
                }
                return render(request,"products/category_view.html",context)
    except:
        raise  Http404
    raise  Http404

def write_review(request):
    if request.user.is_authenticated and request.method == "POST":
        product = None
        product_id = request.POST.get("product_id",None)
        if(product_id):
            products = Product.objects.filter(id=product_id)
            if(products.exists()):
                product = products.first()
        rating = request.POST.get("rating",None)
        number = request.POST.get("number",None)
        description = request.POST.get("description",None)
        if(rating):
            try:
                rating = int(rating)
                x = int(number)
                rating = sorted((1, rating, 5))[1]
            except:
                return redirect("home")
            if description != "" and number != "":
                user = request.user
                if(product and rating and description and number and user):
                    Review.objects.create(product=product,rating=rating,description=description,user=user,number=number)
                    return redirect(reverse("detail",args=[product.slug]))
                else:
                    return redirect("home")
    return redirect("home")


def review_inappropriate(request):
    if request.user.is_authenticated and request.method == "POST":
        id = request.POST.get("id",None)
        if(id):
            review = Review.objects.filter(id=id)
            if(review.exists()):
                review = review.first()
                review.inappropriate = True
                review.save()
                return JsonResponse({"success" : True})
    return JsonResponse({"success" : False})