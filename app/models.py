from operator import itemgetter
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django_rest_passwordreset.signals import reset_password_token_created

# Create your models here.
class usertable(models.Model):
    cname=models.CharField(max_length=50)
    cno=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    otp = models.CharField(max_length=6, default="")
    is_active=models.BooleanField(default=False)
    is_created=models.DateTimeField(auto_now_add=True, null=True, blank=True)

#ItemStock
class Items(models.Model):
    plant_name=models.CharField(max_length=50)
    division=models.CharField(max_length=50)
    material=models.CharField(max_length=50)
    exp_date=models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    available_days=models.IntegerField(blank=True, null=True)
    rate=models.IntegerField(default=1)
    ci_stock=models.IntegerField()
    avail_stock=models.PositiveIntegerField()
    ci_stock_price=models.IntegerField()
    avail_stock_price=models.IntegerField()

#cartitem

class Order(models.Model):
    user = models.ForeignKey(usertable, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    items=models.ManyToManyField(Items,through='OrderItem')
    status=models.CharField(max_length=10,blank=True,null=True)
    pay_status = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=255, blank=True, null=True)


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    item=models.ForeignKey(Items,on_delete=models.CASCADE)
    quantity=models.IntegerField()

#payment
class CardPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiration_month = models.PositiveIntegerField()
    expiration_year = models.PositiveIntegerField()
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Card Payment for Order {self.order.id}"
    
#feedback
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    feedback = models.TextField()

    def __str__(self):
        return self.name
    
    
'''class Invoice(models.Model):
    invoice_number = models.CharField(max_length=255)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)'''
#preset
'''class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email'''

#p_reset
'''@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "adarshpacharya268@gmail.com",
        # to:
        [reset_password_token.user.email]
    )'''