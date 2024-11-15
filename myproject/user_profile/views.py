from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import Address
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required





User = get_user_model()

# Create your views here.
def address(request):
    address = Address.objects.filter(user=request.user, status='listed') 
    msg=None
    print('address:',address)
    print('user:',request.user)
    if request.method=='POST':
         
        user, created = User.objects.get_or_create(id=request.user.id)
        
        if created:
            messages.error(request, "User authentication issue. Please log in again.")
            return redirect('login')
 
        address_line1=request.POST.get('address_line1')
        city=request.POST.get('city')
        state=request.POST.get('state')
        postal_code=request.POST.get('postal_code')
        country=request.POST.get('country')
        phone_number=request.POST.get('phone_number')
        
        adress=Address.objects.create(user=request.user,address_line1=address_line1,city=city,state=state,postal_code=postal_code,country=country,phone_number=phone_number)
        msg='address created sucessfully!!!'
        return redirect('user_profile:address')
    context={
        'address':address,
        'msg':msg
    }
    return render(request,'user_profile/address.html',context)            
def editaddress(request,id):
    address = get_object_or_404(Address, id=id) 
    msg1=None
    if request.method=='POST':
       address.address_line1=request.POST.get('address_line1')
       address.city=request.POST.get('city')
       address.state=request.POST.get('state')
       address.postal_code=request.POST.get('postal_code')
       address.country=request.POST.get('country')
       address.phone_number=request.POST.get('phone_number')
       address.save()
       msg1='updated sucessfully'
       return redirect('user_profile:address')
    context={
        'address':address,
        'msg1':msg1
    }
    return render(request,'user_profile/address.html',context)
                
def listaddress(request,id):
    if request.method=='POST':
        address=get_object_or_404(Address,id=id)
        if address.status=='listed':
            address.status='dislisted'
         
        address.save()
        return redirect('address')  
    return render(request,'user/address.html')  


def blockuser(request,id):
    user=User.objects.get(id=id)
    user.is_active=not user.is_active
    user.save()
    return redirect('user_profile:users')


def users(request):
    User = get_user_model()
    users = User.objects.filter(is_superuser=False)
    context={
        'users':users
    }
    return render(request,'user_profile/users.html',context)

def profile(request):
    user=request.user
    print(user)
    if user.is_authenticated:
        print(f"User is authenticated: {user.username}") 
    else:
        print("User is not authenticated")

    
    if request.method=='POST' and request.FILES.get('profile_picture'):
        profile_picture=request.FILES.get('profile_picture')
        user.profile_image=profile_picture
        user.save()
        return redirect('user_profile:profile')
    print('user:', user)
    context={
         'user': user
    }
    return render(request,'user_profile/profile.html',context)
def editprofile(request):
    user=request.user
    if request.method=='POST':
        user.email=request.POST.get('email')
        user.phone=request.POST.get('phone')
        user.dob=request.POST.get('dob')
        user.gender=request.POST.get('gender')
        user.city=request.POST.get('city')
        user.country=request.POST.get('country')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile:profile')
    return render(request,'user/profile.html')

@never_cache
@login_required(login_url='/auth/login/')
def change_password(request):
    error_messageprofile=None
    modal_open = False
    print('hii')
    if request.method=="POST":
        print('hlo')
        currentpassword=request.POST.get('current_password')
        newpasssword=request.POST.get('new_password')
        comfirmpassword=request.POST.get('confirm_password')
        
        if not request.user.check_password(currentpassword):
            error_messageprofile= "The current password is incorrect."
            modal_open = True
            print("error_messageprofile :",error_messageprofile)
            print('modal_open :',modal_open)
            return render(request, 'user_profile/profile.html', {
                'error_messageprofile': error_messageprofile,
                'modal_open': modal_open
            })
        if newpasssword!=comfirmpassword:
            error_messageprofile= "The new passwords do not match."
            modal_open = True
            return render(request, 'user_profile/profile.html', {
                'error_messageprofile': error_messageprofile,
                'modal_open': modal_open
            })
        if newpasssword:
            request.user.set_password('newpasssword')
            request.user.save()
            print('password changed')
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('user_profile:profile')
        
        else:
            messages.error(request, "Please enter a valid new password.")
            return redirect('change_password')
    context={
        'error_messageprofile':error_messageprofile,
        'modal_open':modal_open
    }
    return render(request,'user_profile/profile.html',context)
