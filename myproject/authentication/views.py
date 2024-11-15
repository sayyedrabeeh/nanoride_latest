from django.shortcuts import render
from django.contrib.auth import get_user_model
import time
from django.contrib import messages
from django.shortcuts import redirect
import re
from django.contrib.auth import login
import random
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login



def generate_otp():
    return str(random.randint(100000, 999999))



def signup(request): 
    print("THIS IS SIGNUP")
    if request.user.is_authenticated:
        return redirect('products:home')
    User = get_user_model()
    if request.method == 'POST':
        print('hii')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print('username:',username)
        print('email:',email)
        print('password1:',password1)
        print('password2:',password2)
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if ' ' in username:
            messages.error(request, 'Username cannot contain spaces.', extra_tags='signup-page username')
        elif len(username) < 3 or len(username) > 150:
            messages.error(request, 'Username must be between 3 and 150 characters.', extra_tags='signup-page username')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.', extra_tags='signup-page username')
        
        # Validate email
        elif not re.match(email_regex, email):
            messages.error(request, 'Please enter a valid email address.', extra_tags='signup-page email')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.', extra_tags='signup-page email')
        
        # Validate password match
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.', extra_tags='signup-page password')
        
        # Validate password length and check for spaces
        elif len(password1) < 6:
            messages.error(request, 'Passwords must be at least 6 characters long.', extra_tags='signup-page password')
        elif ' ' in password1:
            messages.error(request, 'Password cannot contain spaces.', extra_tags='signup-page password')
        else:
            user = User(username=username, email=email)
            user.set_password(password1)
            otp = generate_otp()
            print("generated otp",otp)
            subject = 'Your OTP Code'
            message = f'Your OTP code is {otp}'
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, [email])
                request.session['otp'] = otp 
                request.session['otp_generated_time'] = time.time() 
                request.session['otp_expiration_time'] = 300
                request.session['resend_otp_time'] = 30   
                request.session['user_data'] = {'username': username, 'email': email, 'password': password1}
                return redirect('authentication:verify_otp')  
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}',extra_tags='signup-page')
                return render(request, 'authentication/otp.html',{'error': str(e)}) 
    return render(request,'authentication/signup.html')

def verify_otp(request):
    print("THIS IS VERIFY OTP")
    if request.user.is_authenticated:
        return redirect('products:home')
    User = get_user_model()
    if request.method == 'POST':
        otp_inputs = [
            request.POST.get('otp_1'),
            request.POST.get('otp_2'),
            request.POST.get('otp_3'),
            request.POST.get('otp_4'),
            request.POST.get('otp_5'),
            request.POST.get('otp_6'),
        ]
        entered_otp = ''.join(filter(None, otp_inputs))
        generated_otp = request.session.get('otp')
        user_data = request.session.get('user_data')
        print('Generated OTP:', generated_otp)
        print('Entered OTP:', entered_otp)
        otp_generated_time = request.session.get('otp_generated_time')
        otp_expiration_time = request.session.get('otp_expiration_time', 300)
        current_time = time.time()
        if otp_generated_time is None:
            messages.error(request, 'No OTP generated. Please request a new one.')
            return redirect('authentication:verify_otp')
        if current_time - otp_generated_time > otp_expiration_time:
            messages.error(request, 'Your OTP has expired. Please request a new one.')
            return render(request, 'authentication/otp.html', context={'otp_form': True})
        if entered_otp == generated_otp:
            print('Valid OTP:', entered_otp)
            if user_data:
                if User.objects.filter(username=user_data['username']).exists():
                    messages.error(request, 'Username is already taken. Please choose a different one.')
                    return render(request, 'authentication/otp.html', context={'otp_form': True})
                if User.objects.filter(email=user_data['email']).exists():
                    messages.error(request, 'Email is already taken. Please choose a different one.')
                    return render(request, 'authentication/otp.html', context={'otp_form': True})
                user = User(username=user_data['username'], email=user_data['email'])
                user.set_password(user_data['password'])
                try:
                    user.full_clean()  
                    user.save()  
                    messages.success(request, 'Account created successfully!')
                    login(request, user) 
                    del request.session['otp']
                    del request.session['user_data']
                    return redirect('authentication:login') 
                except ValidationError as e:
                    messages.error(request, f'Error creating account: {str(e)}')
            else:
                messages.error(request, 'User data not found in session.')
        else:
            messages.error(request, 'Invalid OTP or expired OTP. Please try again.')
        return render(request, 'authentication/otp.html', context={'otp_form': True})
    return render(request, 'authentication/otp.html', context={'otp_form': True})

def resend_otp(request):
    print("RESEND OTP")
    User = get_user_model()
    if request.method == 'POST':
        last_resend_time = request.session.get('otp_generated_time', 0) + request.session.get('resend_otp_time', 0)
        email = request.session.get('user_data', {}).get('email')  
        if time.time() < last_resend_time:
            return JsonResponse({'status': 'error', 'message': 'Please wait before requesting a new OTP.'})
        email = request.session.get('user_data', {}).get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'User not found in session.'})
        otp = generate_otp() 
        subject = 'Your OTP Code'
        message = f'Your new OTP code is {otp}'
        from_email = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, from_email, [email])
            request.session['otp'] = otp
            request.session['otp_generated_time'] = time.time()  
            request.session['otp_expiration_time'] = 300   
            return JsonResponse({'status': 'success', 'message': 'OTP has been resent.'})  
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})  
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}) 

def user_login(request):
    print("THIS IS LOGIN ")
    User = get_user_model()
    if request.user.is_authenticated:
        return redirect('products:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username:', username)
        print('password:', password)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist. Please sign up.', extra_tags='login-page')
            return render(request, 'authentication/login.html', {'username': username})

        if not user.is_active:
            messages.error(request, "Your account is blocked. You are not allowed to log in.", extra_tags='login-page')
            return render(request, 'authentication/login.html', {'username': username})

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('products:home')   
            return redirect('products:home')   
        else:
            messages.error(request, 'Incorrect username or password.', extra_tags='login-page')
            return render(request, 'authentication/login.html', {'username': username})
    
    return render(request, 'authentication/login.html')

def custom_logout_view(request):
    request.session.flush()  
    return redirect('products:home')