from django.contrib import admin
from django.utils.html import format_html
from .models import Recipe,HomePageBanner,Handpicked,Miscellaneous,Option,HomePageIngredientIndex,Herobanner,HowDoWeDoIt

from .models import ShiprocketCredentials,Font
# Register your models here.

class ShiprocketCredentialsAdmin(admin.ModelAdmin):
    list_display = ["id","created_at",]
    readonly_fields = ["token"]

class MiscellaneousAdmin(admin.ModelAdmin):
    fields = ["title","description",]

class OptionAdmin(admin.ModelAdmin):
    list_display = ["title","enable"]
    readonly_fields = ["title","description"]
    fields = ["title","description","enable"]

class HerobannerAdmin(admin.ModelAdmin):
    list_display = ["main_heading","get_image","order"]

    def get_image(self,obj):
        return format_html("<img src={0} alt={1} style='height:100px;'/>".format(obj.image.url,obj.main_heading))

class IngredientAdmin(admin.ModelAdmin):
    list_display = ["letter","name","slide_order"]
    list_display_links = ["letter","name","slide_order"]

admin.site.register(Recipe)
admin.site.register(HomePageBanner)
admin.site.register(Handpicked)
admin.site.register(Miscellaneous,MiscellaneousAdmin)
admin.site.register(HomePageIngredientIndex,IngredientAdmin)
admin.site.register(Option,OptionAdmin)
admin.site.register(Herobanner,HerobannerAdmin)
# admin.site.register(ShiprocketCredentials,ShiprocketCredentialsAdmin)
# admin.site.register(Font)
admin.site.register(HowDoWeDoIt)