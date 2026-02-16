from django.db import models

# Create your models here.

class UserModel(models.Model):
    user_id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length=200)
    user_mail = models.EmailField(max_length=50)
    user_phone = models.BigIntegerField()
    user_address = models.CharField(max_length=50)
    user_profile = models.ImageField( upload_to='images/')
    password = models.CharField(help_text = "Enter your Password", max_length=60,null=True)
    user_otp_status = models.CharField(default='otp is pending', max_length=50)
    user_otp = models.CharField(max_length=10,null=True)
    regs_date = models.DateField(auto_now_add = True,null=True)
    onclick_date = models.DateTimeField(auto_now = True,null=True)


    class Meta:
        db_table = "user_details"

class FeedBackModel(models.Model):
    feedbk_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserModel,models.CASCADE,null=True)
    feedback = models.IntegerField(help_text = 'data',null = True)
    feedback1 = models.IntegerField(help_text = 'feedback1',null=True)
    feedback2 = models.IntegerField(help_text = 'feedback2',null=True)
    overreview = models.CharField(max_length=400,null=True)
    sentiment = models.CharField(help_text='sentiment',null=True,max_length=60)

    class Meta:
        db_table = "feedback_details"
