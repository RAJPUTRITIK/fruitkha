from django.db import models
from seller_app.models import Product
# Create your models here.
class User(models.Model):
    firstname=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    propic=models.FileField(upload_to='buyer_profile/',default='anonymous1.jpg')

    def __str__(self):
        return self.email
    

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    total=models.IntegerField(default=0)

    def __str__(self):
        return str(self.quantity)