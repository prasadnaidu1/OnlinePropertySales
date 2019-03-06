from django.db import models

class UserRegister(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(primary_key=True)
    password=models.CharField(max_length=15)
    con_password=models.CharField(max_length=15)
    contact=models.IntegerField()
    otp=models.CharField(max_length=10)
    image=models.ImageField(upload_to="prasad",blank=True)

class property(models.Model):
    property_id=models.IntegerField(primary_key=True)
    property_name=models.CharField(max_length=20)
    def __str__(self):
        return self.property_name

class addproperty(models.Model):
    property_id=models.AutoField(primary_key=True,default=False)
    name=models.CharField(max_length=30)
    date=models.CharField(max_length=30)
    contact=models.IntegerField()
    property=models.CharField(max_length=20)
    email=models.EmailField()
    address=models.TextField()
    selling_price=models.DecimalField(max_digits=20,decimal_places=2)
    image=models.ImageField(upload_to="propertyImages")

class contactUs(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    message=models.TextField(max_length=200)


