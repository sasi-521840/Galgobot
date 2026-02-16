from django.shortcuts import render,redirect
from django.contrib import messages
from userapp.models import UserModel,FeedBackModel
import datetime

# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        name = request.POST.get('adminname')
        password = request.POST.get('adminpassword')

        if(name == 'admin' and password == 'admin'):
            messages.success(request,"Login Successfully")
            return redirect('admin-index')

        else:
            messages.warning(request,"Invalid Username or Password")
            return redirect('admin-login')


    return render(request,'admin/admin-login.html')

def admin_index(request):
    d = UserModel.objects.all()
    e = FeedBackModel.objects.all()
    return render(request,'admin/admin-index.html',{'d':d,'e':e})

def admin_interactions(request):
    c = UserModel.objects.all()
    return render(request,'admin/admin-interactions.html',{'c':c})

def admin_sentiment_analy(request):
    b = FeedBackModel.objects.all()
    return render(request,'admin/admin-sentiment-analy.html',{'b':b})

def admin_sentiment_graph(request):
    positive = FeedBackModel.objects.filter(sentiment="positive").count()
    negitive = FeedBackModel.objects.filter(sentiment="negitive").count()
    neutral = FeedBackModel.objects.filter(sentiment="neutral").count()
    verypositive = FeedBackModel.objects.filter(sentiment="verypositive").count()
    verynegitive = FeedBackModel.objects.filter(sentiment = "verynegitive").count()
    return render(request,'admin/admin-sentiment-graph.html',{'positive':positive,'negitive':negitive,'neutral':neutral,'verypositive':verypositive,'verynegitive':verynegitive})

def admin_user_details(request):
    d = UserModel.objects.all()
    return render(request,'admin/admin-user-details.html',{'d':d})

def admin_userfeedback(request):
    a = FeedBackModel.objects.all()
    return render(request,'admin/admin-userfeedback.html',{'a':a})





