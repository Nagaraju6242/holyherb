from django.contrib import admin
from .models import Cart,CartItem
# Register your models here.

class CartInline(admin.TabularInline):
    model = Cart.items.through

class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ["product","quantity","quantity_price","price"]
    list_display = ["id","product","quantity","qp","price"]
    list_display_links = ["id","product"]

    def qp(self,obj):
        if(obj.quantity_price.exists()):
            x = obj.quantity_price.first()
            return str(x.quantity) + x.quantity_type + " -- " + str(x.price)
        return "NA"


class CartAdmin(admin.ModelAdmin):
    readonly_fields = ["user","total","subtotal","updated","items"]
    search_fields = ["id"]
    list_display = ["id","user","total","updated"]
    list_display_links = ["id","user"]
    class Media:
        js = ("js/admin/cart.js",)
        css = {
            'all' : ("css/admin/cart.css",)
        }

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)