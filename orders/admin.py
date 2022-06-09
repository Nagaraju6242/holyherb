from django.contrib import admin
from .models import Order,ShippingMethod,Coupon
from django.urls import reverse
from django.contrib import messages
from django.utils.html import format_html
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["user","is_user","order_id","cart","coupon_code","coupon_discount","shipping_total","total","timestamp"]
    list_display = ["id","order_id","cart_link","status_color","total","shipping_method"]
    list_filter = ("status",)
    list_display_links = ("id","order_id",)

    def save_model(self, request, obj, form, change):
        if obj.shipment_id is None and obj.length is not None and obj.breadth is not None and obj.height is not None and obj.weight is not None:
            res = Order.objects.send_neworder(obj)
            if(res[0] == 200):
                if("shipment_id" in res[1].keys()):
                    obj.shipment_id = res[1]["shipment_id"]
                    super().save_model(request, obj, form, change)
            else:
                messages.add_message(request, messages.ERROR, res[1].get("message","Please check your Data Again"))
            return

    def status_color(self,order):
        if(order.status == "created"):
            text_color = "#2196f3"
        elif(order.status == "paid"):
            text_color = "green"
        elif(order.status == "shipped"):
            text_color = "purple"
        elif(order.status == "refunded"):
            text_color = "red"
        return format_html('<span style="color:%s;font-weight:700;text-transform:capitalize;">%s<span>' % (text_color,order.status))
    status_color.short_description = "Status"

    def cart_link(self,order):
        url = reverse("admin:carts_cart_change",args=[order.cart.id])
        link = '<a title="cart" target="_blank" href="%s">%s</a>' % (url, order.cart.id)
        return format_html(link)
    cart_link.short_description = "Cart"

class ShippingMethodAdmin(admin.ModelAdmin):
    readonly_fields = ('id','name')
    list_display = ("title","has_fixed_price")

class CouponAdmin(admin.ModelAdmin):
    list_display = ("coupon_code","title","expiry","percent_discount")

admin.site.register(Order,OrderAdmin)
admin.site.register(ShippingMethod,ShippingMethodAdmin)
admin.site.register(Coupon,CouponAdmin)