from sys import flags
from mainApp.models import Product
from django import template

register = template.Library()

@register.filter('cartsize')
def cartsize(request, num):
    cart = request.session.get('cart',None)
    if(cart):
        return cart[num][2]
    else:
        return ''

@register.filter('cartqty')
def cartqty(request, num):
    cart = request.session.get('cart',None)
    if(cart):
        return cart[num][1]
    else:
        return ''

@register.filter('carttotal')
def carttotal(request, num):
    cart = request.session.get('cart',None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return cart[num][1]*p.finalprice
    else:
        return ''

@register.filter('cartproduct')
def cartproduct(request, num):
    cart = request.session.get('cart',None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p
    else:
        return ''

@register.filter('cartname')
def cartname(request, num):
    cart = request.session.get('cart',None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.name
    else:
        return ''

@register.filter('cartprice')
def cartprice(request, num):
    cart = request.session.get('cart',None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.finalprice
    else:
        return ''

@register.filter('cartimage')
def cartimage(request, num):
    cart = request.session.get('cart',None)
    if(cart):
        try:
            p = Product.objects.get(id=int(cart[num][0]))
            return p.pic1.url
        except:
            pass
    else:
        return ''