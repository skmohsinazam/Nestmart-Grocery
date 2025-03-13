from django.contrib import admin
from service.models import Navbar_item
from service.models import Category
from service.models import Product
from service.models import About_provide
from service.models import ContactUs,Profile,Cart,Order,OrderItem,Which_trend

admin.site.site_header = "Nestmart Admin Dashboard"
admin.site.site_title = "Nestmart Admin"
admin.site.index_title = "Welcome to Nestmart Admin Panel"

admin.site.register(Navbar_item)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(About_provide)
admin.site.register(ContactUs)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Which_trend)






# Register your models here.
