from django.contrib import admin
from .models import ObjectViewed,OrderedQuantity,Pixel
# Register your models here.

class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = ['user' , 'content_object' , 'timestamp' ] 
    readonly_fields = ['user','content_object' ,'content_type', 'timestamp' ,'object_id','ip_address']

class OrderedQuantityAdmin(admin.ModelAdmin):
    list_display = ['product','ordered_quantity']
    readonly_fields = ['product','ordered_quantity']

class PixelAdmin(admin.ModelAdmin):
    readonly_fields = ["name"]
    list_display = ["name","pixel_id"]

admin.site.register(ObjectViewed,ObjectViewedAdmin)
admin.site.register(OrderedQuantity,OrderedQuantityAdmin)
admin.site.register(Pixel,PixelAdmin)