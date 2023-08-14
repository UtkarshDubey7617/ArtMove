from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import os
import razorpay
from django.conf import settings
from requests import session
from artmove.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
from django.core.mail import send_mail
from random import randint


from .models import *

def home(request):
    products = Product.objects.all()
    title  = Product.objects.all()
    product = products[:6:-1]
    products = products[:8:-1]
    title = title[:1:-1]
    if(request.method=='POST'):
        try:
            email = request.POST.get('email')
            n = Newslater()
            n.email = email
            n.save()
            subject = 'Thank you! To Subscribe our Newslater : Team Art Move'
            message =  """
                                ! Thank you to Subscribe our Newslater! 
                                Thanks to Join with Us.
                                Team : Art Move
                                keep Shopping with us
                                http://localhost:8000                    
                           """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [n.email, ]
            send_mail( subject, message, email_from, recipient_list )
        except:
            pass
        return HttpResponseRedirect('/')
    return render(request,"index.html",{'Product':product,'Products':products,'Title':title})

def shoppage(request,mc,sc,br):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if(request.method=='POST'):
        search = request.POST.get('search')
        products = Product.objects.filter(Q(name__icontains=search))
    else:
        if(mc=="All" and sc=="All" and br=="All"):
            products = Product.objects.all()
        elif(mc!="All" and sc=="All" and br=="All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc))
        elif(mc=="All" and sc!="All" and br=="All"):
            products = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc))
        elif(mc=="All" and sc=="All" and br!="All"):
            products = Product.objects.filter(brand=Brand.objects.get(name=br))
        elif(mc!="All" and sc!="All" and br=="All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc))
        elif(mc!="All" and sc=="All" and br!="All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br))
        elif(mc=="All" and sc!="All" and br!="All"):
            products = Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))
        else:
            products = Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br))
    products = products[::-1]
    return render(request,"shop.html",{'Product':products,'Maincategory':maincategory,'Subcategory':subcategory,'Brand':brand,'mc':mc,'sc':sc,'br':br})

def login(request):
    if(request.method=='POST'):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request,"Invalid User Name or Password")
    return render(request,"login.html")

def signup(request):
    if(request.method=="POST"):
        actype = request.POST.get("actype")
        if(actype=="seller"):
            u = Seller()
        else:
            u = Buyer()
        u.name = request.POST.get("name")
        u.username = request.POST.get("username")
        u.email = request.POST.get("email")
        u.phone = request.POST.get("phone")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if(password==cpassword):
            try:
                user = User.objects.create_user(username=u.username,password=password,email=u.email)
                user.save()
                u.save()
                subject = 'Congratulations! Your Account Has been Created Successfully : Team Art Move'
                message =  """
                                %s! Your Account Has Been Created Sucessfully! 
                                Thanks to create an account with Us.
                                Team : Art Move
                                keep Shopping with us
                                http://localhost:8000                    
                           """%(u.name)
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [u.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/login/")
            except:
                messages.error(request,"User Name already Exists")
                return render(request,"signup.html")    
        else:
            messages.error(request,"Password and Confirm Password does not matched!!!!")
    return render(request,"signup.html")

@login_required(login_url='/login/')
def profilePage(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            seller = Seller.objects.get(username=request.user)
            return render(request,"sellerprofile.html",{"User":seller})
        except:
            buyer = Buyer.objects.get(username=request.user)
            wishlist = Wishlist.objects.filter(buyer=buyer)
            return render(request,"buyerprofile.html",{"User":buyer,'Wishlist':wishlist})

def blog(request):
    return render(request,"Blog.html")

def blogdetails(request):
    return render(request,"BlogDetails.html")

def history(request):
    try:
        user = User.objects.get(username=request.user)
        try:
            seller = Seller.objects.get(username= request.user)
            products = Product.objects.filter(seller=seller)
            products = products[::-1]
            return render(request,"Producthistory.html",{"User":seller,'products':products})
        except:
            buyer = Buyer.objects.get(username= request.user)
            checkout = Checkout.objects.filter(buyer=buyer)
            checkout = checkout[::-1]
            return render(request,"Orderhistory.html",{"User":buyer,'orders':checkout})
    except:
        return HttpResponseRedirect("/login/")
    
@login_required(login_url='/login/')
def updateprofile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            user = Seller.objects.get(username=request.user)
        except:
            user = Buyer.objects.get(username=request.user)
        if(request.method=="POST"):
            user.name=request.POST.get('name')
            user.email=request.POST.get('email')
            user.phone=request.POST.get('phone')
            user.addressline1=request.POST.get('addressline1')
            user.addressline2=request.POST.get('addressline2')
            user.addressline3=request.POST.get('addressline3')
            user.pin=request.POST.get('pin')
            user.city=request.POST.get('city')
            user.state=request.POST.get('state')
            if(request.FILES.get('pic')):
                user.pic=request.FILES.get('pic')
            user.save()
            return HttpResponseRedirect("/profile/")
    return render(request,"updateprofile.html",{"User":user})

@login_required(login_url='/login/')
def addproduct(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if(request.method=="POST"):
        p = Product()
        p.name = request.POST.get('name')
        p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
        p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
        p.brand = Brand.objects.get(name=request.POST.get('brand'))
        p.stock = request.POST.get('stock')
        p.baseprice = int(request.POST.get('baseprice'))
        p.discount = int(request.POST.get('discount'))
        p.finalprice = p.baseprice-p.baseprice*p.discount/100
        size=""
        if(request.POST.get("4 x 8")):
          size=size+"4 x 8,"
        if(request.POST.get("5 x 7")):
          size=size+"5 x 7,"
        if(request.POST.get("8 x 10")):
          size=size+"8 x 10,"
        if(request.POST.get("9 x 12")):
          size=size+"9 x 12,"
        if(request.POST.get("11 x 14")):
          size=size+"11 x 14,"
        if(request.POST.get("12 x 12")):
          size=size+"12 x 12,"
        if(request.POST.get("12 x 16")):
          size=size+"12 x 16,"
        if(request.POST.get("16 x 20")):
          size=size+"16 x 20,"
        if(request.POST.get("18 x 24")):
          size=size+"18 x 24,"
        if(request.POST.get("24 x 24")):
          size=size+"24 x 24,"
        if(request.POST.get("24 x 30")):
          size=size+"24 x 30,"
        if(request.POST.get("30 x 30")):
          size=size+"30 x 30,"
        p.size = size
        p.description = request.POST.get('description')
        p.pic1 = request.FILES.get('pic1')
        p.pic2 = request.FILES.get('pic2')
        p.pic3 = request.FILES.get('pic3')
        try:
            p.seller = Seller.objects.get(username=request.user)
        except:
            return HttpResponseRedirect("/profile/")
        p.save()
        subject = 'CheckOut Our Latest Painting on Art Move : Team Art Move'
        message =  """
                        Hey!
                        We upload Some more Latest Painting with best offerce 
                        please checkout
                        Thanks you 
                        Team : Art Move
                        keep Shopping with us
                        http://localhost:8000//singleproduct/%d                    
                   """%(p.id)
        email_from = settings.EMAIL_HOST_USER
        subscribers = Newslater.objects.all()
        recipient_list = subscribers
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect("/history/")
    return render(request,"addproduct.html",{'Maincategory':maincategory,'Subcategory':subcategory,'Brand':brand})

@login_required(login_url='/login/')
def deleteproduct(request,num):
    try:
        p = Product.objects.get(id=num)
        seller = Seller.objects.get(username=request.user)
        if(p.seller==seller):
            p.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def editproduct(request,num):
    try:
        p = Product.objects.get(id=num)
        seller = Seller.objects.get(username=request.user)
        if(p.seller==seller):
            maincategory = Maincategory.objects.exclude(name=p.maincategory)
            subcategory = Subcategory.objects.exclude(name=p.subcategory)
            brand = Brand.objects.exclude(name=p.brand)
            if(request.method=="POST"):
                p.name = request.POST.get('name')
                p.maincategory = Maincategory.objects.get(name=request.POST.get('maincategory'))
                p.subcategory = Subcategory.objects.get(name=request.POST.get('subcategory'))
                p.brand = Brand.objects.get(name=request.POST.get('brand'))
                p.stock = request.POST.get('stock')
                p.baseprice = int(request.POST.get('baseprice'))
                p.discount = int(request.POST.get('discount'))
                p.finalprice = p.baseprice-p.baseprice*p.discount/100
                size=""
                if(request.POST.get("4 x 8")):
                    size=size+"4 x 8,"
                if(request.POST.get("5 x 7")):
                    size=size+"5 x 7,"
                if(request.POST.get("8 x 10")):
                    size=size+"8 x 10,"
                if(request.POST.get("9 x 12")):
                    size=size+"9 x 12,"
                if(request.POST.get("11 x 14")):
                    size=size+"11 x 14,"
                if(request.POST.get("12 x 12")):
                    size=size+"12 x 12,"
                if(request.POST.get("12 x 16")):
                    size=size+"12 x 16,"
                if(request.POST.get("16 x 20")):
                    size=size+"16 x 20,"
                if(request.POST.get("18 x 24")):
                    size=size+"18 x 24,"
                if(request.POST.get("24 x 24")):
                    size=size+"24 x 24,"
                if(request.POST.get("24 x 30")):
                    size=size+"24 x 30,"
                if(request.POST.get("30 x 30")):
                    size=size+"30 x 30,"
                p.size = size
                p.description = request.POST.get('description')
                if(request.FILES.get('pic1')):
                    if(p.pic1):
                        os.remove("media/"+str(p.pic1))
                    p.pic1 = request.FILES.get('pic1')
                if(request.FILES.get('pic2')):
                    if(p.pic2):
                        os.remove("media/"+str(p.pic2))
                    p.pic2 = request.FILES.get('pic2')
                if(request.FILES.get('pic3')):
                    if(p.pic3):
                        os.remove("media/"+str(p.pic3))
                    p.pic3 = request.FILES.get('pic3')
                p.save()
                return HttpResponseRedirect("/history/")
            return render(request,"editproduct.html",{'Product':p,'Maincategory':maincategory,'Subcategory':subcategory,'Brand':brand})
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")
        
@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

def singleproduct(request,num):
    p = Product.objects.get(id=num)
    size = p.size.split(",")
    size = size[:-1]
    return render(request,"singleproduct.html",{'Product':p,'Size':size})

def addtowishlist(request,num):
    try:
        buyer = Buyer.objects.get(username=request.user)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        p = Product.objects.get(id=num)
        flag=False
        for i in wishlist:
            if(i.product==p):
                flag=True
                break
        if(flag==False):
            w = Wishlist()
            w.buyer = buyer
            w.product = p
            w.save()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def deletewishlist(request,num):
    try:
        w = Wishlist.objects.get(id=num)
        buyer = Buyer.objects.get(username=request.user)
        if(w.buyer==buyer):
            w.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")
        
def addtocart(request):
    pid = request.POST.get('pid')
    size = request.POST.get('size')
    cart = request.session.get("cart",None)
    if(cart):
        if(pid in cart.keys()) and size==cart[pid][2]:
                pass
        else:
            count = len(cart.keys())
            count = count+1
            cart.setdefault(str(count),[pid,1,size])
    else:
        cart = {'1':[pid,1,size]}
    request.session['cart']=cart
    return HttpResponseRedirect('/cart/')

def cart(request):
    try:
        cart = request.session.get("cart",None)
        total = 0
        shipping = 0
        final = 0
        if(cart):
            for values in cart.values():
                p = Product.objects.get(id=int(values[0]))
                total=total+p.finalprice*values[1]
            if(len(cart.values())>=1 and total<5000):
                shipping=150
            final=total+shipping
    except:
        return HttpResponseRedirect("/login/")
    return render(request,'cart.html',{'Cart':cart,'Total':total,'Shipping':shipping,'Final':final})

def updatecart(request,id,num):
    cart = request.session.get('cart',None)
    if(cart):
        if(num=='-1'):
            if(cart[id][1]>1):
                q= cart[id][1]
                q=q-1
                cart[id][1]=q
        else:
            q= cart[id][1]
            q=q+1
            cart[id][1]=q
        request.session['cart']=cart
    return HttpResponseRedirect('/cart/')

@login_required(login_url='/login/')
def deletecart(request,id):
    cart = request.session.get('cart',None)
    if(cart):
        cart.pop(id)
        request.session['cart']=cart
    return HttpResponseRedirect("/cart/")

client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login/')
def checkout(request):
    cart = request.session.get('cart',None)
    total = 0
    shipping = 0
    final = 0
    if(cart):
        for values in cart.values():
            p = Product.objects.get(id=int(values[0]))
            total = total+p.finalprice*values[1]
        if(len(cart.values())>=1 and total<5000):
            shipping=150
        final = total+shipping
    else:
        if(total<=0):
            return HttpResponseRedirect('/shop/All/All/All')
    try:
        buyer = Buyer.objects.get(username=request.user)
        if(request.method=="POST"):
            mode = request.POST.get('mode')
            check = Checkout()
            check.buyer=buyer
            check.total=total
            check.shipping=shipping
            check.final=final
            check.save()
            for value in cart.values():
                cp = CheckoutProducts()
                p = Product.objects.get(id=int(value[0]))
                cp.name=p.name
                cp.pic=p.pic1.url
                cp.size=value[2]
                cp.price=p.finalprice
                cp.qty=value[1]
                cp.total=p.finalprice*value[1]
                cp.checkout=check
                cp.save()
                request.session['cart']={}
            if(mode=='COD'):
                return HttpResponseRedirect('/confirmation/')
            else:
                orderAmount = check.final*100
                orderCurrency = "INR"
                paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
                paymentId = paymentOrder['id']
                check.mode="Net Banking"
                check.save()
                return render(request,"pay.html",{
                    "amount":orderAmount,
                    "api_key":RAZORPAY_API_KEY,
                    "order_id":paymentId,
                    "User":buyer
                })
        return render(request,'checkout.html',{'Cart':cart,'Total':total,'Shipping':shipping,'Final':final,"User":buyer})
    except:
        return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def paymentSuccess(request,rppid,rpoid,rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(buyer=buyer)
    check=check[::-1]
    check=check[0]
    check.rppid=rppid
    check.rpoid=rpoid
    check.rpsid=rpsid
    check.paymentstatus=2
    check.save()
    return HttpResponseRedirect('/confirmation/')

@login_required(login_url='/login/')
def paynow(request,num):
    try:
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("/profile/")
    
    check = Checkout.objects.get(id=num)
    orderAmount = check.final*100
    orderCurrency = "INR"
    paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
    paymentId = paymentOrder['id']
    check.save()
    return render(request,"pay.html",{
        "total":check,
        "amount":orderAmount,
        "api_key":RAZORPAY_API_KEY,
        "order_id":paymentId,
        "User":buyer
    })

def contact(request):
    try:
        if(request.method=='POST'):
            c = Contact()
            c.name = request.POST.get('name')
            c.email = request.POST.get('email')
            c.phone = request.POST.get('phone')
            c.subject = request.POST.get('subject')
            c.message = request.POST.get('message')
            c.save()
            subject = 'Your Query Has been Submitted : Team Art Move'
            message =  """
                            Thanks to Share your Query with us
                            Our Team will Contact You Soon
                            Team : Art Move
                            keep shopping with us
                            http://localhost:8000                    
                       """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [c.email, ]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request,"Your Query Has Been Submitted Successfully! Our Team Will Contact You Soon!")
    except:
        HttpResponseRedirect('/+contact/')
    return render(request,"contact.html")

def confirmation(request):
    buyer = Buyer.objects.get(username= request.user)
    checkout = Checkout.objects.filter(buyer=buyer)
    checkout = checkout[::-1]
    subject = 'Your Order Has been Placed Successfully : Team Art Move'
    message =  """
                            Thanks to placed the Order.
                            Team : Art Move
                            keep shopping with us
                            http://localhost:8000                    
                       """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [buyer.email, ]
    send_mail( subject, message, email_from, recipient_list )
    return render(request,"confirmation.html",{"User":buyer,'orders':checkout})

def forgetusername(request):
    if(request.method=='POST'):
        try:
            username = request.POST.get("username")
            user = User.objects.get(username=username)
            if(user is not None):
                try:
                    user = Buyer.objects.get(username=username)
                except:
                    user = Seller.objects.get(username=username)
                num = randint(100000,999999)
                request.session['otp']=num
                request.session['user']=username
                subject = 'OTP for Password Reset : Team Art Move'
                message =  """
                                OTP : %d
                                Team : Art Move
                                keep shopping with us
                                http://localhost:8000                    
                           """%num
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return HttpResponseRedirect("/forgetotp/")
            else:
                messages.error(request,'Username not Found')
        except:
            messages.error(request,'Username not Found')
    return render(request,'forgetusername.html')

def forgetotp(request):
    if(request.method=='POST'):
        otp = int(request.POST.get("otp"))
        sessionotp = request.session.get('otp',None)
        if(otp == sessionotp):                  
            return HttpResponseRedirect('/forgetpassword/')
        else:
            messages.error(request,'Invalid OTP') 
    return render(request,'forgetotp.html')

def forgetpassword(request):
    if(request.method=='POST'):
        password = (request.POST.get("password"))
        cpassword = (request.POST.get("cpassword"))
        if(password == cpassword): 
            user = User.objects.get(username = request.session.get('user'))
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Password and Confirm Doesn't Match")
    return render(request,'forgetpassword.html')