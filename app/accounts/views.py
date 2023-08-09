from accounts.models import Account, Address
from cart.models import Cart, CartItem, Wishlist
from .forms import RegistrationForm, AddressForm

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Verification
from django.contrib.sites.shortcuts import  get_current_site
from django.template.loader import render_to_string
from django.utils.http import  urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# OTP verification
#from twilio.rest import Client
import secrets

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]+phone_number
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, phone_number=phone_number)
            user.phone_number_prefix = '+91'
            user.save()
            # if user_activaation_mail(request, user, email):
            #     return redirect('/accounts/login/?command=verification&email='+email)
            request.session['phone_number'] = phone_number
            return redirect('otp_generation')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def login(request):
    flag = True
    if request.user.is_authenticated:
        messages.success(request, "You are already logged")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email = email, password=password)
        if user:
            is_cart_exist = Cart.objects.filter(user=user).exists()
            is_wishlist_exist = Wishlist.objects.filter(user=user).exists()
            if not is_cart_exist:
                Cart.objects.create(user = user)
            if not is_wishlist_exist:
                Wishlist.objects.create(user=user)            
            auth.login(request,user)
            return redirect('dashboard')
        else:
            if Account.objects.filter(email=email).exists():
                user = Account.objects.get(email__exact=email)
                if not user.is_active:
                    messages.info(request, 'Your account is successfully created but not verifide please click on below link to verify')
                    request.session['phone_number'] = user.phone_number
                    flag = False
                    return render(request,'login.html',{'flag':flag}) 
                else:
                    messages.error(request, 'Invalid login credentials or account is not activated')
                    return render(request, "login.html", {'flag':flag})      
            else:
                messages.error(request, 'Invalid login credentials or account is not activated')
                return render(request, "login.html", {'flag':flag})
    else:
        return render(request,'login.html',{'flag':flag})     


def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


def activate(request, uidb64, token):
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Your accout has been verified')
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')

def user_activaation_mail(request, user, email):
            current_site = get_current_site(request)  
            mail_subject = 'Please activate your account'
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=(to_email,))
            send_email.send()
            return True

def user_activaation_mail_send(request,  email):
    user = request.user
    if user_activaation_mail(request, user, email):
        print('send')
        return redirect('profile')
    else:
        pass
def user_password_reset_mail(request, user, email):
    current_site = get_current_site(request)  
    mail_subject = 'Reset your password'
    message = render_to_string('reset_password_email.html', {
        'user': user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=(to_email,))
    send_email.send()
    messages.success(request, 'Password reset email has been sent to your email address')        


def forgotpassword(request):
    if request.method == 'POST':
        keyword = request.POST.get('email')
        if Account.objects.filter(email=keyword).exists():
            user = Account.objects.get(email__exact=keyword)
            user_password_reset_mail(request, user, keyword)
            return redirect('login')
        elif Account.objects.filter(phone_number = keyword).exists():
            user = Account.objects.get(phone_number__exact=keyword)
            return redirect('otp_generation')  
        else:
            messages.error(request, 'Account does not exist')
            redirect('forgotpassword')    
    return render(request, 'forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    messages.success(request, 'Create your new passsword')
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token): 
        request.session['uid'] = uid
        if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password == confirm_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('login')
            else:
                messages.error(request, 'Password do not match!')
                return render(request, 'resetpassword.html')
        else:
            return render(request, 'resetpassword.html')
    else:
        messages.error(request, 'The link has expired')
        return redirect('login')    


# def send_otp(mobile, otp):
#     account_sid = "AC0871a2ce4b0987606c46162bff9e84c3"
#     auth_token  = "734961c9e6c3397f19dd063fe2c5eeb5"
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         to=mobile,
#         from_="+19542483195",
#         body="Your registration otp is " + str(otp))
#     print(message.sid)

def check_otp(request):
    phone_number = request.session['phone_number']
    context = {'phone_number':phone_number}
    user = Account.objects.filter(phone_number=phone_number).first()
    if request.method == 'POST':
        otp = ""
        for i in range(1,7):
            otp += request.POST.get('digit' + str(i))
        if otp == user.otp and user.is_active == False:
            user.is_active = True
            user.is_phone_verified = True
            user.otp = secrets.token_hex(32)
            user.save()
            messages.success(request, 'Your accout has been verified')
            return redirect('login')
        elif otp == user.otp and user.is_active == True:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            user.otp = secrets.token_hex(32)
            user.save()
            messages.success(request, 'Create your new passsword')
            return HttpResponseRedirect(reverse('resetpassword_validate', args=[str(uid), str(token)]))
        else:
            context = {'message' : 'Wrong OTP' , 'class' : 'danger','mobile':phone_number }
            return render(request,'otp.html' , context) 
    return render(request,'otp.html' , context)

def otp_generation(request):
    phone_number = request.session['phone_number']
    user = Account.objects.filter(phone_number=phone_number).first()
    mobile = user.phone_number_prefix + user.phone_number
    otp = 100000 + secrets.randbelow(899999)
    print(otp)
    user.otp = otp
    user.save()
    # send_otp(mobile, otp)
    return redirect('check_otp')

def user_profile(request):
    saved_address = Address.objects.filter(user=request.user).all()
    address_form = AddressForm()
    context = {
        'saved_address' : saved_address,
        'address_form':address_form
    }
    return render(request, 'profile.html', context)





