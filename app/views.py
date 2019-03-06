import math
import random
import re
import smtplib
import ssl
import datetime
import time
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator



from django.shortcuts import render
from .models import UserRegister, property, addproperty, contactUs



def Home(request):
    type=request.GET.get("type")
    return render(request,"index.html",{"type":type})


def Register(request):
    type=request.GET.get("type")
    return render(request,"index.html",{"type":type})


def Sale(request):
    type=request.GET.get("type")
    return render(request,"index.html",{"type":type})


def login(request):
    type=request.GET.get("type")
    return render(request,"index.html",{"type":type})


def RegisterDetails(request):
    name=request.POST.get("t1")
    email=request.POST.get("t2")
    password=request.POST.get("t3")
    con_password=request.POST.get("t4")
    contact=request.POST.get("t5")
    file=request.FILES["t6"]
    r = UserRegister.objects.values("email")
    digits="0123456789"
    OTP=""
    for x in range(4):
        OTP+=digits[math.floor(random.random()*10)]
    smtp_server="smtp.gmail.com"
    port=465
    From_mail="prasadnaidu766@gmail.com"
    To_email=email
    e_password="njzgvtdzgjruayoa"
    message = " Hello "+name+" This Is Your OTP  For Registration: " + OTP + "Username :" + email + "password :" +password
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(From_mail, e_password)
        server.sendmail(From_mail, To_email, message)

    email_id = []
    for x in r:
        email_id.append(x["email"])
    if email in email_id:
        return render(request, "index.html", {"type": "register", "message": "Email already exists"})
    elif len(password) < 8 and len(con_password) < 8 :
        return render(request, "index.html",
                      {"type": "register", "message": "Your password must br more than 8 characters"})

    elif re.search('[0-9]', password) is None:
        return render(request, "index.html",
                      {"type": "register", "message": "Make sure your password has a digit  in it "})

    elif re.search('[A-Z]', password) is None:
        return render(request, "index.html",
                      {"message": "Make sure your password has a Capital letter in it ", "type": "register"})

    elif re.search('[a-z]', password) is None:
        return render(request,"index.html",
                      {"message": "Make sure your password has a Small letter in it ", "type": "register"})
    elif password != con_password:
        return render(request, "index.html", {"type": "register", "message": "Your password did not match"})
    else:
       UserRegister(name=name, contact=contact, email=email, password=password,
                        con_password=con_password,image=file,otp=OTP).save()

    return render(request,"index.html",{"type":"otpvalidation"})


def OtpValidate(request):
    otp=request.POST.get("t5")
    res=UserRegister.objects.filter(otp=otp)
    name=""
    image=""
    email=""
    if res:
        for x in res:
            name=x.name
            image=x.image
            email=x.email
        Name=name.upper()


        return render(request,"LoginWelcome.html",{"name":Name,"image":image,"email":email})
    else:
        return render(request,"index.html",{"type":"otpvalidation"})


def LoginDetails(request):
    email=request.POST.get("u1")
    password=request.POST.get("u2")

    res=UserRegister.objects.filter(email=email,password=password)

    qs=addproperty.objects.filter(email=email)
    p1=qs.count()
    count=0
    name=""
    email=""
    image=""
    if res:

        for x in res:
            name = x.name
            email = x.email
            image = x.image
        Name = name.upper()
        request.session["status"]=True
        request.session["email"]=email
        result = addproperty.objects.all().exclude(email=email)
        p=Paginator(result,6)
        page=p.page(1)

        return render(request,"LoginWelcome.html",{"name":Name,"email":email,"image":image,"result":page,"p":p1})
    else:
        type="login"

        return render(request,"index.html",{"type":type})


def Update(request):
    email=request.GET.get("email")
    user=UserRegister.objects.filter(email=email)
    name=""
    email_id=""
    password=""
    con_password=""
    contact=""
    if user:
        for x in user:
            name=x.name
            email_id=x.email
            password=x.password
            con_password=x.con_password
            contact=x.contact
        return render(request,"update.html",{"user":user,"name":name,"email":email_id,"password":password,"con_password":con_password,"contact":contact})
    else:
        return render(request,"LoginWelcome.html")


def UpdateDetails(request):
    name=request.POST.get("t1")
    email=request.POST.get("t2")
    password=request.POST.get("t3")
    con_password=request.POST.get("t4")
    contact=request.POST.get("t5")
    UserRegister.objects.filter(email=email).update(name=name,password=password,con_password=con_password,contact=contact)
    return render(request,"LoginWelcome.html",{"message":"Updated SuccessFully"})


def Property(request):
    type=request.GET.get("type")
    email=request.GET.get("email")
    da=datetime.datetime.today()
    user = UserRegister.objects.filter(email=email)
    qs=property.objects.all()
    name = ""
    image=""
    contact=""
    for x in user:
        name = x.name
        image=x.image
        contact=x.contact
    for y in range(1):
        id=random.randint(1,10000)
    return render(request,"LoginWelcome.html",{"type":type,"name":name,"image":image,"date":da,"contact":contact,"data":qs,"email":email,"id":id})


def AddProperty(request):
    id=request.POST.get("t0")
    name=request.POST.get("t1")
    date=request.POST.get("t2")
    contact=request.POST.get("t3")
    property_name=request.POST.get("t4")
    email=request.POST.get("t5")
    address=request.POST.get("t6")
    Selling_price=request.POST.get("t7")
    property_image=request.FILES["t8"]
    addproperty(name=name,date=date,contact=contact,property=property_name,email=email,address=address,
                selling_price=Selling_price,image=property_image,property_id=id).save()
    qs = addproperty.objects.filter(email=email)
    p = qs.count()


    return render(request,"LoginWelcome.html",{"type":"property","properties":p})


def ShowProperties(request):

    type=request.GET.get("type")
    email=request.GET.get("email")
    qs=addproperty.objects.filter(email=email)
    res = addproperty.objects.all()
    result=UserRegister.objects.filter(email=email)
    p=qs.count()
    p = Paginator(qs, 3)
    if id==None:
        p.page(1)
    else:
        p1=p.page(id)





    image=""

    name=""
    for x in result:
        image=x.image
        name=x.name
    return render(request,"LoginWelcome.html",{"type":type,"res":qs,"image":image,"properties":p,"name":name,"prasad":p1,"email2":email})

def ShowIndex(request):
    id = request.GET.get("page_no")
    res=addproperty.objects.values("address")

    Address=[]
    for x in res:
        if x not in Address:
            Address.append(x["address"])
    Addresss=set(Address)

    qs = addproperty.objects.all()
    p = Paginator(qs, 4)
    if id == None:
        page = p.page(1)
    else:
        page = p.page(id)
    return render(request, "index.html", {"type": type, "result": page,"address":Addresss,"id":id})


def Forget(request):
    type=request.GET.get("type")
    type2="login"
    return render(request,"index.html",{"type1":type,"type":type2})

def ForgetDetails(request):
    email=request.POST.get("u1")
    res=UserRegister.objects.filter(email=email)
    if res:
        type1="forgetdetails"
        type = "login"
        return render(request,"index.html",{"type":type,"email":email,"type1":type1})
    else:
        type="login"
        type2="forget"
        return render(request, "index.html", {"type1": type, "type": type2})


def NewPassword(request):
    email=request.POST.get("u0")
    email_id=request.POST.get("u1")
    password=request.POST.get("u2")
    con_password=request.POST.get("u3")
    if len(password) < 8 and len(con_password) < 8 :
        return render(request, "index.html",
                   {"type": "register", "message": "Your password must br more than 8 characters"})
    elif re.search('[0-9]', password) is None:
        return render(request, "index.html",
                      {"type": "register", "message": "Make sure your password has a digit  in it "})
    elif re.search('[A-Z]', password) is None:
        return render(request, "index.html",
                      {"message": "Make sure your password has a Capital letter in it ", "type": "register"})
    elif re.search('[a-z]', password) is None:
        return render(request,"index.html",
                      {"message": "Make sure your password has a Small letter in it ", "type": "register"})
    elif password != con_password:
        return render(request, "index.html", {"type": "register", "message": "Your password did not match"})
    else:
        UserRegister.objects.filter(email=email).update(password=password)
        type="login"
        return render(request,"index.html",{"type":type})


def PropertyDetails(request):
    type=request.GET.get("type")
    id=request.GET.get("id")
    res=addproperty.objects.filter(property_id=id)
    return render(request,"index.html",{"type":type,"res":res})


def ContactUs(request):
    type=request.GET.get("type")
    return render(request,"index.html",{"type":type})


def Contact(request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    message=request.POST.get("message")
    contactUs(name=name,email=email,message=message).save()
    return render(request,"index.html")


def Logout(request):
    request.session["status"]=False
    request.session["email"]=""
    id = request.GET.get("page_no")
    qs = addproperty.objects.all()
    p = Paginator(qs, 4)
    if id == None:
        page = p.page(1)
    else:
        page = p.page(id)
    return render(request, "index.html", {"type": type, "result": page})


def UpdateProperty(request):
    id=request.GET.get("id")
    result=addproperty.objects.filter(property_id=id)
    data=property.objects.all()
    id=""
    contact=""
    email=""
    price=""
    for x in result:
        id=x.property_id
        contact=x.contact
        email=x.contact
        price=x.selling_price
    return render(request,"LoginWelcome.html",{"type":"UpdateDetails","result":result,"id":id,
                                               "contact":contact,"email":email,"price":price,"data":data})


def UpdatePropertyDetails(request):
    id=request.POST.get("t1")
    contact=request.POST.get("t2")
    p_name=request.POST.get("t3")
    price=request.POST.get("t4")
    addproperty.objects.filter(property_id=id).update(contact=contact,property=p_name,selling_price=price)
    return render (request,"LoginWelcome.html",{"type":"UpdateDetails","message":"Updated SuccessFully"})


def DeleteProperty(request):
    id=request.GET.get("id")
    qs=addproperty.objects.filter(property_id=id).delete()

    res = addproperty.objects.all()
    type="showProperties"
    return render(request,"LoginWelcome.html",{"res":res,"type":type})


def BuyProperty(request):

    id=request.GET.get("id")
    res=addproperty.objects.filter(property_id=id)
    price=""
    for x in res:
        price=x.selling_price
    tax=price*18/100
    total=price+tax
    return render(request,"LoginWelcome.html",{"type":"BuyingDetails","price":price,"tax":tax,"total":total,"id":id})


def ProceedToPay(request):
    id=request.POST.get("id")
    res = addproperty.objects.filter(property_id=id)
    return render(request, "index.html", {"type":"buy_properties","message":"Goto PaymentGateway"})



def LoginIndex(request):
    email=request.GET.get("email")
    number=request.GET.get("page_no")
    res=UserRegister.objects.filter(email=email)
    image=""
    for  x in res:
        image=x.image
    addproperty.objects.all()
    result = addproperty.objects.all()
    p = Paginator(result, 4)
    if number== None:
        page = p.page(1)
    else:
        page=p.page(number)
    return render(request, "LoginWelcome.html",{"result": page,"image":image})


def ChangeProfile(request):
    email=request.GET.get("email")
    res=UserRegister.objects.filter(email=email)
    image=""
    for x in res:
        image=x.image
    if res:
        return render(request,"LoginWelcome.html",{"type":"changeprofile","res":res,"image":image,"email":email})
    else:
        return render(request,"LoginWelcome.html",{"type":"login"})


def ImageUploading(request):
    file = request.FILES["t1"]
    email=request.POST.get("e1")
    res=UserRegister.objects.filter(email=email).update(image=file)
    return render(request,"LoginWelcome.html",{"type":"login","image":file})


def HelpLine(request):
    email=request.GET.get("email")
    type=request.GET.get("type")
    return render(request,"LoginWelcome.html",{"type":type,"email":email})


def HelpLineDetails(request):
    email=request.POST.get("t2")
    msg=request.POST.get("msg")
    res=UserRegister.objects.values("email")
    email_id=[]
    for x in res:
        email_id.append(x["email"])
    smtp_server = "smtp.gmail.com"
    port = 465
    From_mail = "prasadnaidu766@gmail.com"
    To_email =email
    e_password = "njzgvtdzgjruayoa"
    message = msg
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(From_mail, e_password)
        server.sendmail(From_mail, To_email, message)
    return render(request,"LoginWelcome.html",{"type":"helpline"})


def Address(request):
    type=request.GET.get("type")
    Address=request.GET.get("Address")
    res=addproperty.objects.filter(address=Address).values("selling_price","image","contact","property_id")
    return render(request,"index.html",{"type":type,"res":res})


def Buy_Property(request):
    type=request.GET.get("type")
    id=request.GET.get("id")
    res = addproperty.objects.filter(property_id=id)
    price = ""
    for x in res:
        price = x.selling_price
    tax = price * 18 / 100
    total = price + tax
    return render(request, "index.html",
                  {"type": type, "price": price, "tax": tax, "total": total, "id": id})

