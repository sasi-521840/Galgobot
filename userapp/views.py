from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from userapp.models import UserModel,FeedBackModel
from textblob import TextBlob
import random
import requests


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)

        try:
            user = UserModel.objects.get(user_mail=email,password=password)
            messages.success(request,"Login Successfully")
            if user.user_otp_status == 'otp verified' or user.user_otp_status == 'Accepted':
                request.session['user_id']=user.user_id
                messages.success(request,"Login Successfully")
                return redirect('user-index')

            elif user.user_otp_status == 'otp is pending':
                gen_otp = str(random.randint(1111,9999))
                print(gen_otp)
                user.user_otp = gen_otp
                user.save()
                url = "https://www.fast2sms.com/dev/bulkV2"
                message = ' Dear {}. Welcome to Reveal. Here is your One Time Password {}. For Your First Time Login'.format(user.user_name,gen_otp)
                numbers = user.user_phone
                payload = f'sender_id=FTWSMS&message={message}&language=english&route=v3&numbers={numbers}'
                headers = {
                'authorization': "xZIssgvbBl4hSeai7mMebAMxcusK4BbhQZGO3v1O0ZlAUjuRFWhLAR5hA2SK",
                'Content-Type': "application/json",
                'Cache-Control': "no-cache",
                }
                response = requests.request("POST", url, data=payload, headers=headers)
                print(response.text,'heloooo')
                messages.info(request, 'OTP has been sent to your registered Mobile Number')
                return redirect('user-otpverification',id=user.user_id)

            elif user.user_otp_status == 'Restricted':
                messages.warning(request, 'Your request is Restricted, so you cannot login')
                return redirect('user-login')    
                                
        except:
            messages.warning(request,"Email does'nt exist")
            return redirect('user-login')

    return render(request,'user/user-login.html')

def user_otpverification(request,id):
    user = get_object_or_404(UserModel,user_id=id)

    if request.method == 'POST':
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        otp = otp1+otp2+otp3+otp4
        print(otp,'userotp')
        print(user.user_otp,'database')
        if user.user_otp == otp:
            user.user_otp_status ="otp verified"
            user.user_otp = None
            user.save()
            request.session['user_id']=user.user_id
            messages.success(request, 'OTP Verified Successfully')

            return redirect('user-index')
        else:
            messages.warning(request, 'Invalid OTP')
            return redirect('user-otpverification',id=id)
    return render(request,'user/user-otpverification.html')
    
def user_register(request):
    if request.method == 'POST' and 'user_profile' in request.FILES:
        name = request.POST.get('fname')
        address = request.POST.get('address')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        user_profile = request.FILES['user_profile']
        

        if UserModel.objects.filter(user_mail=email):
            messages.warning(request,'Email Already Exist')
            print('true')
            return redirect('user-login')

        else:
            user = UserModel.objects.create(user_name=name,user_address=address,user_mail=email,user_phone=mobile,password=password,user_profile=user_profile)
            gen_otp = str(random.randint(1111,9999))
            print(gen_otp)
            user.user_otp = gen_otp
            user.save()
            url = "https://www.fast2sms.com/dev/bulkV2"
            message = ' Dear {}. Welcome to Reveal. Here is your One Time Password {}. For Your First Time Login'.format(user.user_name,gen_otp)
            numbers = user.user_phone
            payload = f'sender_id=FTWSMS&message={message}&language=english&route=v3&numbers={numbers}'
            headers = {
            'authorization': "xZIssgvbBl4hSeai7mMebAMxcusK4BbhQZGO3v1O0ZlAUjuRFWhLAR5hA2SK",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text,'heloooo')
            messages.info(request, 'OTP has been sent to your registered Mobile Number')
 
            return redirect('user-otpverification',id=user.user_id)

    return render(request,'user/user-register.html')

def user_index(request):
    e = UserModel.objects.all().count()
    r = FeedBackModel.objects.all().count()
    return render(request,'user/user-index.html',{'r':r,'e':e})

def my_profile(request):
    user = request.session["user_id"]
    data = get_object_or_404(UserModel,user_id=user)

    if request.method == 'POST':
        data.user_name = request.POST.get('fname')
        data.user_phone = request.POST.get('phone')
        data.password = request.POST.get('password')
        try:
            data.user_profile=request.FILES['user_profile']
        except:
            pass
        data.save()
        messages.success(request, 'Profile Updated Successful')
        return redirect('my-profile')


    return render(request,'user/my-profile.html',{'data':data})

def user_feedback(request):
    user_id = request.session["user_id"]
    r = UserModel.objects.get(user_id = user_id)
    if request.method == 'POST':
        feedbk = request.POST.get('a')
        feedbk1 = request.POST.get('b')
        feedbk2 = request.POST.get('c')
        print(feedbk2,'fffff')
        overreview = request.POST.get('overall')
        if not feedbk or not feedbk1 or  not feedbk2:
            print(feedbk,feedbk1,feedbk2)
            messages.error(request, 'Please Select the ratings')
            return redirect('user-feedback')
        analysis = TextBlob(overreview)
        print(analysis.sentiment)

        sentiment = ''
        if analysis.polarity >= 0.5:
            sentiment = 'verypositive'
        elif analysis.polarity > 0 and analysis.polarity < 0.5:
            sentiment = 'positive'
        elif analysis.polarity < 0 and analysis.polarity >= -0.5:
            sentiment = 'negitive'
        elif analysis.polarity <= -0.5:
            sentiment = 'verynegitive'
        else:
            sentiment = 'neutral'

        FeedBackModel.objects.create(feedback = feedbk, feedback1 = feedbk1,feedback2 = feedbk2,overreview = overreview,user_id= r,sentiment = sentiment)
        messages.success(request,'Feedback Submited')
        return redirect('user-feedback')

    return render(request,'user/user-feedback.html')

def galgobot(request):
    return render(request,'user/galgobot.html')
    