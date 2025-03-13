from django.contrib import admin
from django.urls import path
from nestmart_grocery import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home/', views.home,name='home'),
    path('about/', views.aboutUs,name='about'),
    path('shop/', views.shop,name='shop'),
    path('login/', views.login_view,name='login'),
    path('register/', views.register,name='register'),
    path("contactus/", views.contactUs, name="contact"),
    path("contact_us/", views.contact_us, name="contact"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('catepage/<slug:slug>/', views.cate_shop, name='cate_shop'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:cart_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-checkout/', views.process_checkout, name='process_checkout'),
    path('order_confirmation/<int:order_id>', views.order_confirmation, name='order_confirmation'),
    path('search/', views.search_products, name='search_products'),
    path('order-history/', views.order_history, name='order_history')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
