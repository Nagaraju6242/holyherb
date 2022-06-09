from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Wishlist,JoinOurCircle


from .forms import UserAdminCreationForm,UserAdminChangeForm

User  = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Personal info', {'fields': ('name','number')}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class JoinOurCircleAdmin(admin.ModelAdmin):
    readonly_fields = ['email']
    class Media:
        js = ("js/admin/joc.js",)

class WishlistAdmin(admin.ModelAdmin):
    readonly_fields = ["user","products",]

admin.site.register(User,UserAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(JoinOurCircle,JoinOurCircleAdmin)
# Removing the Group Model
admin.site.unregister(Group)


admin.site.site_header = 'Holyherb Administration'       # default: "Django Administration"
admin.site.index_title = 'Site administration'           # default: "Site administration"
admin.site.site_title = 'Holyherb site admin'            # default: "Django site admin"
