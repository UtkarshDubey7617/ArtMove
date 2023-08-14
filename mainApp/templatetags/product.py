from django import template

from mainApp.models import Checkout, CheckoutProducts

register = template.Library()

@register.filter('checksize')
def checksize(size, item):
    flag = False
    for i in size.split(','):
        if(i==item):
            flag = True
            break
    return flag

@register.filter('orderstatus')
def orderstatus(request, num):
    if(num==0):
        return 'Cancel'
    elif(num==1):
        return 'Not Packed'
    elif(num==2):
        return 'Packed'
    elif(num==3):
        return 'Out For Delivery'
    else:
        return 'Delivered'

@register.filter('paymentstatus')
def paymentstatus(request, num):
    if(num==1):
        return 'Pending'
    else:
        return 'Done'

@register.filter('paymentstatuscon')
def paymentstatuscon(request, num):
    if(num==1):
        return True
    else:
        return False

@register.filter('orderitem')
def orderitem(request, num):
    check = Checkout.objects.get(id=num)
    p = CheckoutProducts.objects.filter(checkout=check)
    return p

@register.filter('price')
def price(request, num):
    check = Checkout.objects.get(id=num)
    price = CheckoutProducts.objects.get("price")
    return price

@register.filter('stock')
def stock(request, data):
    if(data=='In Stock'):
        return True
    else:
        return False