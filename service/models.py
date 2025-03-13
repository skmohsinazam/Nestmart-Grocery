from django.db import models
from django.db import connection
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Navbar_item(models.Model):
    title=models.CharField(max_length=255)
    url=models.URLField()
    
    def __str__(self):
        return self.title

class Category(models.Model):
    image=models.ImageField(upload_to='images/')
    title=models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)  

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Which_trend(models.Model):
    title=models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    pno = models.CharField(max_length=100)
    pname = models.CharField(max_length=255)
    pdescription = models.TextField(blank=True, null=True)
    pqt = models.IntegerField(default=0)
    pimg = models.ImageField(upload_to='product_images/') 
    pprice = models.DecimalField(max_digits=10, decimal_places=2)
    pdiscpri = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cate=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    which_trend=models.ForeignKey(Which_trend,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.pname

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.pdiscpri * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.pname} ({self.quantity})"

class About_provide(models.Model):
    title=models.CharField(max_length=150)
    img=models.ImageField(upload_to='about/')
    discri=models.TextField(blank=False,null=False)
    
    def __str__(self):
        return self.title

class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=128)  
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    address = models.TextField()
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.full_name

class ContactUs(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()
    
    def __str__(self):
        return self.full_name
def Trending():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Product")
        rows=cursor.fetchall()
        
    return rows
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    payment_method = models.CharField(
        max_length=20, choices=[('cod', 'Cash on Delivery'), ('online', 'Online Payment')]
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order}={self.quantity} x {self.product.pname}"
# Create your models here.
