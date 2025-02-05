from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='main'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('product/<str:color>/<str:model>/', get_product_by_color, name='by_color'),
    path('to_favorite/<slug:slug>/', save_favorite_product, name='to_favorite'),
    path('favorites/', FavoriteListView.as_view(), name='favorite'),
    path('authentication/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('registration/', register_view, name='register'),
    path('my_cart/', my_cart, name='my_cart'),
    path('to_cart/<slug:product_slug>/<str:action>/', to_cart_view, name='to_cart'),
    path('delete_product/<int:pk>/<int:order>/', delete_order_product_view, name='delete_product'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
    path('profile/', profile_view, name='profile'),
    path('my_orders/', customer_orders_view, name='my_orders'),
    path('send_mail/', send_mail_views, name='send_mail'),
    path('about/', about_view, name='about'),
    path('contact_with_us/', offer_user_view, name='offer')
]