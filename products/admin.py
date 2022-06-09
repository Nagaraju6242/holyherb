from django.contrib import admin
from .models import Product,Quantity_Price,ProductImage,Review,ProductSku
from django.utils.html import format_html

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product" , "rating" , "user" , "timestamp"]

class QuantityPriceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    ordering = ["quantity_type","quantity","price"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","flavour","category_tag"]
    ordering = ["-category","title","flavour"]
    search_fields = ["title","flavour","category"]
    readonly_fields = ["slug",]

    def category_tag(self,obj):
        color = "orange"
        if(obj.category == "facecare"):
            color = "green"
        if(obj.category == "bodycare"):
            color = "red"
        if(obj.category == "gifting"):
            color = "#8500ff"
        return format_html('<b style="color:{}">{}</b>',color,obj.category)

class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ['product__title','product__flavour','product__category'] 
    list_display = ["get_name","get_flavour","get_image","image","main_image" , "artistic"]
    list_filter = ("main_image","artistic",)

    def get_name(self,obj):
        return obj.product.title
    get_name.admin_order_field  = 'product'  
    get_name.short_description = 'Product' 


    def get_flavour(self,obj):
        return obj.product.flavour
    get_flavour.admin_order_field  = 'product'  
    get_flavour.short_description = 'Flavour' 

    def get_image(self,obj):
        return format_html("<img style='width:100px;height:100px;object-fit:cover;' src={} />",obj.image.url)
    get_image.short_description = 'Image'

admin.site.register(Product,ProductAdmin)
admin.site.register(Quantity_Price,QuantityPriceAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(ProductSku)