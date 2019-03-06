from django.contrib import admin

from .models import property,UserRegister,addproperty
class propertydetails(admin.ModelAdmin):
    list_display = ('property_id','property_name')
    class Meta:
        model=property
class userdetails(admin.ModelAdmin):
    list_display = ("name","email","password","con_password","otp","image")
    class Meta:
        model=UserRegister
class property_details(admin.ModelAdmin):
    list_display = ("name","date","contact","property","email","address","selling_price","image")
    class Meta:
        model=addproperty

admin.site.register(property,propertydetails)
admin.site.register(UserRegister,userdetails)
admin.site.register(addproperty,property_details)
