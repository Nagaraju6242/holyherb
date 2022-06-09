from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
from django.urls import path,include
from . import views
from products import views as product_views
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
# from carts.views import cart_detail_api_view
from accounts.views import get_wishlist_api,remove_item_from_wishlist_api,move_to_cart_api,join_our_circle,toggle_to_wishlist_api,get_cart_wishlist_api,orders_home,update_profile_api,download_file
from orders.views import shipping_method_reuse,remove_shipping,add_coupon_api,remove_coupon_api,remove_payment
from customization.views import privacy_policy,terms_and_conditions,faq


urlpatterns = [
    path('admin/accounts/joinourcircle/download',download_file),
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('allauth/', include('allauth.urls')),
    path('coupons/',views.coupons,name='coupons'),
    path('accounts/',include("accounts.urls")),
    path('products/',include("products.urls")),
    path('category/<str:category>/',product_views.get_category,name="get_category"),
    path('category/<str:category>/<str:product>/',product_views.get_category_product,name="get_category_product"),
    path('search/',product_views.search,name='search'),
    path('api/shippingmethod/',shipping_method_reuse),
    path('api/length/',get_cart_wishlist_api,name="get_cart_wishlist_api"),
    path('api/joincircle/',join_our_circle),
    path('api/wishlist/',get_wishlist_api,name="api-wishlist"),
    path('api/wishlist/move/',move_to_cart_api),
    path('api/wishlist/remove/',remove_item_from_wishlist_api,name="api-wishlist-remove"),
    path('api/wishlist/add/',toggle_to_wishlist_api,name="toggle-wishlist-api"),
    path('api/removeshipping/',remove_shipping),
    path('api/removepayment/',remove_payment),
    path('api/updateprofile/',update_profile_api,name="update-profile"),
    path('api/coupon/',add_coupon_api,name="coupon"),
    path('api/couponremove/',remove_coupon_api,name="coupon-remove"),
    path('api/writereview/',product_views.write_review,name="write-review"),
    path('api/reportinappropriate/',product_views.review_inappropriate),
    path('cart/',include("carts.urls")),
    path('checkout/address/create/',checkout_address_create_view,name="checkout_address_create"),
    path('checkout/address/reuse/',checkout_address_reuse_view,name="checkout_address_reuse"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('orders/',orders_home,name="orders_home"),
    path('ingredients/',include("ingredientindex.urls")),
    path('privacypolicy/',privacy_policy,name="privacy_policy"),
    path('termsandconditions/',terms_and_conditions,name="termsandconditions"),
    path('faq',faq,name="faq"),
    path('offline/',views.offline),
    path("robots.txt/",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    # path('sw.js/',(TemplateView.as_view(template_name="service-worker.js",
    #             content_type='application/javascript',
    #             )), name='service-worker.js'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)