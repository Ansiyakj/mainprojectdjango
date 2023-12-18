from django.shortcuts import render,redirect
from cart.models import Cart,Gift,Order,Account,Wishlist
from shop.models import Product
from django.contrib.auth.decorators import login_required
@login_required
def add_to_cart(request,p):
    product = Product.objects.get(pname=p)
    user = request.user
    try:
        cart = Cart.objects.get(user=user, product=product)
        if (cart.quantity < cart.product.stock):
            cart.quantity += 1
        cart.save()
    except Cart.DoesNotExist:
        cart = Cart.objects.create(product=product, user=user, quantity=1)
        cart.save()
    return redirect('cart:cart_view')
@login_required
def cart_view(request):
    Total = 0
    Grant=0
    user=request.user

    try:
        cart=Cart.objects.filter(user=user)
        gift = Gift.objects.all()
        for i in cart:
            Total+=i.quantity*i.product.price
            Grant=Total+50
    except:
        pass
    return render(request,'cartview.html',{'cart':cart,'Total':Total,'Grant':Grant,'gift':gift})
@login_required
def cart_remove(request,p):
    product=Product.objects.get(pname=p)
    user=request.user
    try:
        cart=Cart.objects.get(user=user,product=product)
        if(cart.quantity>1):
            cart.quantity-=1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return redirect('cart:cart_view')


@login_required
def full_remove(request,p):
    product = Product.objects.get(pname=p)
    user = request.user
    try:
        cart = Cart.objects.get(user=user, product=product)
        cart.delete()

    except:
        pass
    return redirect('cart:cart_view')


def orderform(request):
    if (request.method == "POST"):
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['n']
        payment=request.POST['payment']
        user = request.user
        cart = Cart.objects.filter(user=user)
        total = 0
        grand=0
        for i in cart:
            total += i.quantity * i.product.price
            grand=total+50
        if payment == 'cod':
            for i in cart:
                o = Order.objects.create(user=user, product=i.product, phone=p, place=a, no_of_items=i.quantity,
                                         order_status="pending")
                o.save()
                i.product.stock = i.product.stock - i.quantity
                i.product.save()
            cart.delete()
            msg = "Order Placed Successfully with COD"
            return render(request, 'orderconfirm.html', {'msg': msg})

        elif payment == "online":
            try:
                acct = Account.objects.get(acctnumber=n)
                if (acct.balance > grand):
                    acct.balance = acct.balance - grand
                    acct.save()
                    for i in cart:
                        o = Order.objects.create(user=user, product=i.product, phone=p, place=a, no_of_items=i.quantity,
                                             order_status="paid")
                        o.save()
                        i.product.stock = i.product.stock - i.quantity
                        i.product.save()
                    cart.delete()
                    msg = "Order Placed Successfully through online payment :)"
                    return render(request, 'orderconfirm.html', {'msg': msg})
                else:
                    msg = "Insufficient Amount!.You can't place order :("
                    return render(request, 'orderconfirm.html', {'msg': msg})
            except:
                msg = "Invalid account number"
                return render(request, 'noaccount.html', {'msg': msg})


    return render(request,'orderform.html')

def order_view(request):
    user = request.user

    order = Order.objects.filter(user=user)
    gift=Gift.objects.all()

    return render(request,'orderview.html',{'order':order,'u':user.username,'gift':gift})

@login_required
def add_wishlist(request,p):
    product = Product.objects.get(pname=p)
    user = request.user
    try:
        wish = Wishlist.objects.get(user=user, product=product)

        wish.save()
    except Wishlist.DoesNotExist:
        wish = Wishlist.objects.create(product=product, user=user,quantity=1)
        wish.save()
    return redirect('cart:wish_view')
@login_required
def wish_view(request):
    user=request.user
    try:
        wish=Wishlist.objects.filter(user=user)
    except:
        pass
    return render(request,'wish_view.html',{'wish':wish})
@login_required
def wish_full_remove(request,p):
    product = Product.objects.get(pname=p)
    user = request.user
    try:
        wish = Wishlist.objects.get(user=user, product=product)
        wish.delete()

    except:
        pass
    return redirect('cart:wish_view')

