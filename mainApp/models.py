from random import choices
from django.db import models

class Maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline2 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline3 = models.CharField(max_length=100,default=None,null=True,blank=True)
    pin = models.CharField(max_length=50,default=None,null=True,blank=True)
    city = models.CharField(max_length=50,default=None,null=True,blank=True)
    state = models.CharField(max_length=50,default=None,null=True,blank=True)
    pic = models.FileField(upload_to="images",default="noimage.jpg",null=True,blank=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    maincategory = models.ForeignKey(Maincategory,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    baseprice = models.IntegerField()
    discount = models.IntegerField()
    finalprice = models.IntegerField()
    size = models.CharField(max_length=150)
    description = models.TextField()
    stock = models.CharField(max_length=20,default="In Stock")
    pic1 = models.ImageField(upload_to="images",default="noimagep.jpg",null=True,blank=True)
    pic2 = models.ImageField(upload_to="images",default="noimagep.jpg",null=True,blank=True)
    pic3 = models.ImageField(upload_to="images",default="noimagep.jpg",null=True,blank=True)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline1 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline2 = models.CharField(max_length=100,default=None,null=True,blank=True)
    addressline3 = models.CharField(max_length=100,default=None,null=True,blank=True)
    pin = models.CharField(max_length=50,default=None,null=True,blank=True)
    city = models.CharField(max_length=50,default=None,null=True,blank=True)
    state = models.CharField(max_length=50,default=None,null=True,blank=True)
    pic = models.FileField(upload_to="images",default="noimage.jpg",null=True,blank=True)

    def __str__(self):
        return self.username

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

order = ((0,'Cancel'),(1,'Not Packed'),(2,'Packed'),(3,'Out for Delivery'),(4,'Delivered'))
payment = ((1,'Pending'),(2,'Done'))
class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    shipping = models.IntegerField()
    final = models.IntegerField()
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    mode = models.CharField(max_length=20,default="COD")
    orderstatus = models.IntegerField(choices=order,default=1)
    paymentstatus = models.IntegerField(choices=payment,default=1)
    rppid = models.CharField(max_length=100,default="",null=True,blank=True)
    rpoid = models.CharField(max_length=100,default="",null=True,blank=True)
    rpsid = models.CharField(max_length=100,default="",null=True,blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+" "+str(self.buyer)

class CheckoutProducts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    size = models.CharField(max_length=20)
    price = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    checkout = models.ForeignKey(Checkout,on_delete=models.CASCADE)
    pic = models.FileField(upload_to="images",default="noimage.jpg",null=True,blank=True)

    def __str__(self):
        return self.name


class Newslater(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50,unique=True)

contactstatuschoice =((1,'Active'),(2,'Done'))
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    subject = models.TextField()
    message = models.TextField()
    status = models.IntegerField(choices=contactstatuschoice,default=1)
