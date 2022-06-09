from django.urls import path
from .views import cart_update,cart_home,checkout_home,checkout_done_view,payment_error,update_quantity

urlpatterns = [
    path('',cart_home,name='cart_home'),
    path('update/',cart_update,name="cart_update"),
    path('checkout/',checkout_home,name="checkout"),
    # path('update-price/',update_cart_price,name="update_price"),
    path('update-quantity/',update_quantity,name="update_quantity"),
    path('success/',checkout_done_view),
    path('error/',payment_error,name="payment_error")
]