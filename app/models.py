from operator import itemgetter
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
from django.utils import timezone 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, cname, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, cname=cname, **extra_fields)
        user.set_password(password)  # Hash password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, cname, password, **extra_fields)

# Custom user model
class usertable(AbstractBaseUser, PermissionsMixin):  # Added PermissionsMixin for compatibility
    id = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=50)
    cno = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Required for Django's authentication
    is_verified = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cname']  # Required fields for creating a user

    def __str__(self):
        return self.email


# ItemStock model for inventory management
class Items(models.Model):
    plant_name = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    material = models.CharField(max_length=50)
    exp_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    available_days = models.IntegerField(blank=True, null=True)
    rate = models.IntegerField(default=1)
    ci_stock = models.IntegerField()
    avail_stock = models.PositiveIntegerField()
    ci_stock_price = models.IntegerField()
    avail_stock_price = models.IntegerField()

# Order model for handling customer orders
class Order(models.Model):
    user = models.ForeignKey(usertable, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Items, through='OrderItem')
    status = models.CharField(max_length=10, blank=True, null=True)
    pay_status = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=255, blank=True, null=True)

# OrderItem model to link items to orders
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()

# CardPayment model for handling payments through card
class CardPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=255)
    expiration_month = models.PositiveIntegerField()
    expiration_year = models.PositiveIntegerField()
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Card Payment for Order {self.order.id}"

# Feedback model for collecting customer feedback
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    feedback = models.TextField()

    def __str__(self):
        return self.name

# Password reset signal handler
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "adarshpacharya268@gmail.com",  # Replace with a valid email
        # to:
        [reset_password_token.user.email]
    )

