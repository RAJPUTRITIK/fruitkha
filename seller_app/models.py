from django.db import models

# Create your models here.
class Seller_User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)

    def __str__(self):
        return  self.email
    
class Product(models.Model):
    pname=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    p_quantity=models.IntegerField(default=0)
    desc=models.CharField(max_length=500)
    pimage=models.FileField(upload_to='seller_profile',default='anonymous1.jpg')
    seller=models.ForeignKey(Seller_User,on_delete=models.CASCADE)

    def __str__(self):
        return self.pname