from django.shortcuts import render
from django.http import Http404
from .models import Ingredient
from accounts.models import Wishlist
from products.models import Product

# Create your views here.
def ingredientindexhome(request):
    letters = "abcdefghijklmnopqrstuvwxyz"
    data = {}
    for letter in letters:
        data[letter] = Ingredient.objects.filter(letter__iexact=letter)
    return render(request,"ii_home.html",{"letters":letters,"data":data})

def get_ingredient(request,ingredient):
    ingredient = Ingredient.objects.filter(name__iexact=ingredient)
    if(ingredient.exists()):
        ingredient = ingredient.first()
    else:
        raise Http404
    sort_order = request.GET.get("sort",None)
    products = []
    wishlist_items = []
    if(request.user.is_authenticated):
        wishlist,created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = wishlist.products.all()
    if(ingredient):
        products = ingredient.products.all()
        if(sort_order in ["price-inc","price-dec","alpha-inc","alpha-dec","new-first","new-last"]):
            if(sort_order == "price-inc"):
                products = Product.objects.order_lth(products)
            elif(sort_order == "price-dec"):
                products = Product.objects.order_htl(products)
            elif(sort_order == "alpha-inc"):
                products = Product.objects.order_atz(products)
            elif(sort_order == "alpha-dec"):
                products = Product.objects.order_zta(products)
            elif(sort_order == "new-first"):
                products = Product.objects.order_nto(products)
            elif(sort_order == "new-last"):
                products = Product.objects.order_otn(products)
    details = {
        "ingredient" : ingredient,
        "products" : products,
        "wishlist_items" : wishlist_items,
        "sort" : sort_order
    }
    return render(request,"ii_view.html",details)