from django.contrib import admin
from django.urls import path
from mainapp import views as mainapp_views
from userapp import views as userapp_views
from adminapp import views as adminapp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

#mainapp views
    path('',mainapp_views.main_index,name='main-index'),
    path('about',mainapp_views.about,name='about'),
    path('contact',mainapp_views.contact,name='contact'),

#userapp views
    path('user-login',userapp_views.user_login,name='user-login'),
    path('user-register',userapp_views.user_register,name='user-register'),
    path('user-index',userapp_views.user_index,name='user-index'),
    path('my-profile',userapp_views.my_profile,name='my-profile'),
    path('user-feedback',userapp_views.user_feedback,name='user-feedback'),
    path('galgobot',userapp_views.galgobot,name='galgobot'),
    path('otp-verification/<int:id>',userapp_views.user_otpverification,name='user-otpverification'),

#adminapp views
    path('admin-login',adminapp_views.admin_login,name='admin-login'),
    path('admin-index',adminapp_views.admin_index,name='admin-index'),
    path('admin-interactions',adminapp_views.admin_interactions,name='admin-interactions'),
    path('admin-sentiment-analy',adminapp_views.admin_sentiment_analy,name='admin-sentiment-analy'),
    path('admin-sentiment-graph',adminapp_views.admin_sentiment_graph,name='admin-sentiment-graph'),
    path('admin-user-details',adminapp_views.admin_user_details,name='admin-user-details'),
    path('admin-userfeedback',adminapp_views.admin_userfeedback,name='admin-userfeedback'),
    

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)