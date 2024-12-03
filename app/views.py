
import datetime
import smtplib
import string
from tokenize import generate_tokens
from django.utils import timezone
from datetime import date, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.shortcuts import render, redirect
from app.custom_filters import is_expired
from app.forms import OTPVerificationForm
from app.models import usertable
from django.contrib import messages
from app.models import *
from app.models import Items,Order
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from reportlab.pdfgen import canvas
from io import BytesIO
import time
from django.contrib.auth.hashers import make_password

from .models import *
from django.contrib import messages

#from django.contrib.auth import authenticate, login
#from django.contrib.auth import logout
#from django.urls import reverse_lazy
#from django.contrib.auth.views import PasswordResetView
#from django.contrib.messages.views import SuccessMessageMixin

#preset
'''from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.conf import settings'''


# Create your views here.
def loginview(request):
    return render(request,"app/login.html")

#loginad
def loginrview(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'havmor@gmail.com' and password == 'havmor@123':
            return render(request, 'app/reports.html')
        
    return render(request, 'app/login1.html')

def menuview(request):
    '''send_mail(
        # title:
        "Testing mail",
        # message:
        'email_plaintext_message',
        # from:
        "adarshpacharya268@gmail.com",
        # to:
        ['adarshpacharya90@gmail.com'],
        fail_silently=False,
    )'''
    return render(request,"app/menu.html")

def indexview(request):
    return render(request,"app/index.html")

def aboutus(request):
    return render(request,"app/about.html")

def index1(request):
    return render(request,"app/controls.html")

def itemadd(request):
    return render(request,"app/itemadd.html")

#userpage
def userpage(request):
    current_date = date.today()
    #fetching data
    iteminfo=Items.objects.all()
    valid_items = []
    for item in iteminfo:
        if item.exp_date >= current_date:
            valid_items.append(item)
    
    return render(request,"app/user1.html",{'key3':valid_items})

#ideamadd
def item(request):
    pname=request.POST['pname']
    division=request.POST['division']
    item=request.POST['item']
    exp=request.POST['exp']
    rate=request.POST['rate']
    cistock=request.POST['cistock']
    avstock=request.POST['avstock']
    ciprice=request.POST['ciprice']
    avprice=request.POST['avprice']

    current_date =  timezone.now().date()
    exp = datetime.strptime(exp, '%Y-%m-%d').date()
    if exp < current_date:
            messages.info(request, "****The product is already expired!!!***")
            return HttpResponseRedirect('/itemadd/')

    item1=Items.objects.filter(material=item)
    if item1:
        messages.info(request, "****item already in stock!! Reenter new product.***")
        return HttpResponseRedirect('/itemadd/')
    else:
        newitems=Items.objects.create(plant_name=pname,division=division,material=item,exp_date=exp,rate=rate,ci_stock=cistock,avail_stock=avstock,ci_stock_price=ciprice,avail_stock_price=avprice)
        messages.info(request, '***The Item was Successfully Added***')
        return HttpResponseRedirect('/itemadd/')



#delet_item
def deleteitem(request,d):
    ddata=Items.objects.get(id=d)

    #query to delete
    ddata.delete()
    messages.success(request,"Item deleted successfully!")
    return redirect('/show/')

#edititem
def edititem(request,pk):
    getd=Items.objects.get(id=pk)
    return render(request,"app/itemedit.html",{'key3':getd})

#updateedit
def updatedata(request,pk):
    update=Items.objects.get(id=pk)
    update.exp_date=request.POST['exp']
    update.rate=request.POST['rate']
    update.ci_stock=request.POST['cistock']
    update.avail_stock=request.POST['avstock']
    update.ci_stock_price=request.POST['ciprice']
    update.avail_stock_price=request.POST['avprice']

    current_date =  timezone.now().date()
    exp_datee=request.POST['exp']
    exp_date = datetime.strptime(exp_datee, '%Y-%m-%d').date()
    if exp_date < current_date:
            messages.info(request, "****The product is already expired!!!***")
            return redirect('edit', pk=pk)

    update.save()
    messages.success(request,"Item updated successfully!")
    return render(request,"app/controls.html")
    

#cart
def filter_item_list(request):
    available_items = []
    
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(f"key:{key},value:{value}")
            if key.startswith('available_'):
                item_id = key.replace('available_', '')
                item = Items.objects.get(id=item_id)
                if value == 'on':
                    available_items.append(item)

    context = {
        'available_items': available_items,
    }
    return render(request, "app/filtered_item_list.html", context)

#items details
def show(request):
    #fetching all the data
    all_data=Items.objects.all()
    for item in all_data:
        item.is_expired = is_expired(item.exp_date)
    return render(request,"app/controls.html",{'key1':all_data})

#user details
def usershow(request):
    #fetching all user data
    user_data=usertable.objects.all()
    return render(request,"app/controls.html",{'key2':user_data})


#login
def userlogin(request):
       if request.POST['email']=='havmor@gmail.com':
        if request.POST['password']=='havmor@123':
           return render(request,"app/controls.html")
        else:
           message="password doesn't match!"
           return render(request,"app/login.html",{'msg':message})
           
       if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=usertable.objects.filter(email=email).first()
        if user:
             if user.password==password:
                request.session['name']=user.cname
                request.session['number']=user.cno
                request.session['email']=user.email
                request.session['address']=user.address
                return render(request, "app/user1.html")
             else:
                message="password does not match!"
                return render(request,"app/login.html",{'msg':message})
        else:
             message="user does not exist"
             return render(request,"app/login.html",{'msg':message})

#singupview
def signup(request):
    return render(request,"app/signup.html")

#forgotp
def forgotview(request):
    return render(request,"app/forgotp.html")

def newpassword(request):
    return render(request,"app/newpassword.html")

#registeruser
def registeruser(request):
    if request.method=='POST':
        name=request.POST['name']
        pno=request.POST['number']
        email=request.POST['email']
        add=request.POST['address']
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        user=usertable.objects.filter(email=email)
         
        if user:
            message="this emailID was already registered! Re-Enter"
            return render(request,"app/signup.html",{'msg':message})
        else:
            if password==cpassword:
                usertable.objects.create(cname=name,cno=pno,email=email,address=add,password=password)

                return render(request,"app/login.html")
           #else:
               # message="password does not match!"
                #return render(request,"app/signup.html",{'msg':message})

def showp(request):
    return render(request,"app/show.html")

#order

def place_order(request):
    if request.method == 'POST':
        items = Items.objects.all()
        checked_items = []
        user_name = request.session.get('name')
        
      
        for item in items:
            item_id = str(item.id)
            checkbox_name = 'item_checkbox_' + item_id
            quantity_name = 'quantity_' + item_id

            if checkbox_name in request.POST:
                quantity = request.POST.get(quantity_name, '0')
                quantity = int(quantity)
                if quantity > 0:
                    checked_items.append((item, quantity))

        if not checked_items:
            message = "Please use the checkbox to select Items."
            return render(request, 'app/user1.html', {'message': message})
        else:
            message="order places successsfully!"

        user = get_object_or_404(usertable, cname=user_name)
        order = Order.objects.create(user=user,total_amount=0)
        order.save()  
        total_amount = 0  # Initial total amount

        for item, quantity in checked_items:
            order_item = OrderItem.objects.create(order=order, item=item, quantity=quantity)
            total_amount += item.rate * quantity
            item.avail_stock=F('avail_stock')-quantity
            item.ci_stock=F('ci_stock')-quantity
            item.save()
    
        order.total_amount = total_amount  # Update the total amount
        order.save()

        context = {
            'order': order,
            'order_items': checked_items,
            'total_amount': total_amount,
            
        }
        
        return render(request, 'app/success.html',context)
    
    items = Items.objects.all()
    return render(request, 'app/user1.html', {'items': items})
    
#orders detail
def orders(request):
    orders = Order.objects.order_by('-date_ordered')
    return render(request, "app/corder.html",{'key5':orders})
    

#status update
def update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        # Optionally, you can redirect to a different page or render a success message here.

    return redirect('orders')

#user order
def display_orders(request):
    user_name = request.session.get('name')
    user = usertable.objects.get(cname=user_name)
    orders = Order.objects.filter(user=user)
    return render(request, 'app/orders.html', {'orders': orders,'user': user})

#payment form
def payment_form(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'app/payment_form.html', context)

import random

def generate_invoice_number():
    prefix = "INV"
    random_number = random.randint(1000, 9999)
    return f"{prefix}-{random_number}"


# Helper function to check if card is expired
def is_card_expired(expiry_month, expiry_year):
    current_year = datetime.now().year
    current_month = datetime.now().month

    # If the card's expiry year is before the current year, it's expired
    if int(expiry_year) < current_year:
        return True
    # If the card's expiry year is the same as the current year, check the month
    if int(expiry_year) == current_year and int(expiry_month) < current_month:
        return True
    return False
    
#payment
def payment(request, order_id):
    print("Payment function called")
    if request.method == 'POST':
        name_on_card = request.POST['nameoncard']
        card_number = request.POST['cardnumber']
        expiry_month = request.POST['month']
        expiry_year = request.POST['year']
        csv = request.POST['csv']

        order = get_object_or_404(Order, id=order_id)

        # Generate the invoice number (you can use your preferred method here)
        invoice_number = generate_invoice_number()

        # Update the order with the invoice number and payment status
        order.invoice_number = invoice_number
        order.pay_status = True
        order.save()  # Set payment_status to True

        # Create a new CardPayment instance and save it
        card_payment = CardPayment(
            order=order,
            card_number=card_number,
            cardholder_name=name_on_card,
            expiration_month=expiry_month,
            expiration_year=expiry_year,
            cvv=csv
        )
        card_payment.save()

        # Perform the remaining payment processing and handle the payment flow

        # Redirect to the paysuccess page with the invoice number
        return paysuccess(request, invoice_number)

    # If the request method is GET, simply render the payment form
    return render(request, 'payment_form.html', {'order_id': order_id})

#payment_confirmation
def payment_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    card_payment = CardPayment.objects.filter(order=order).first()  # Fetch the CardPayment instance related to the order

    return render(request, 'app/userdetails.html', {'order': order, 'card_payment': card_payment})

'''def payment(request, order_id):
    # Payment processing code...

    # Redirect to the bill generation URL after a successful payment
    return redirect('generate_bill_pdf', order_id=order_id)'''

from django.shortcuts import render, get_object_or_404
from .models import Order

def paysuccess(request, invoice_number):
    order = get_object_or_404(Order, invoice_number=invoice_number)
    seller = order.items.first().material  # Assuming 'seller' is a ForeignKey in the Items model

    return render(request, 'app/paysuccess.html', {'order': order, 'seller': seller})

#bill on admin intreface
def generate_bill(request, order_id):
    # Retrieve the order and other required data
    order = Order.objects.get(id=order_id)
    seller = usertable.objects.all()  # Example, adjust this to your actual seller model

    # Render the HTML template with the order and seller data
    template = get_template('paysuccess1.html')
    context = {'order': order, 'seller': seller}
    html = template.render(context)

    # Create a PDF document from the rendered HTML
    pdf_file = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=pdf_file)

    # Set the response headers for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bill.pdf"'

    # Write the PDF document to the response
    response.write(pdf_file.getvalue())
    pdf_file.close()

    return response


#bill
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_bill_pdf(request, order_id):
    # Retrieve the order and other required data
    order = Order.objects.get(id=order_id)
    seller = usertable.objects.all()  # Example, adjust this to your actual seller model

    # Render the HTML template with the order and seller data
    template = get_template('paysuccess.html')
    context = {'order': order, 'seller': seller}
    html = template.render(context)

    # Create a PDF document from the rendered HTML
    pdf_file = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=pdf_file)

    # Set the response headers for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bill.pdf"'

    # Write the PDF document to the response
    response.write(pdf_file.getvalue())
    pdf_file.close()

    return response

#feedback
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback

#feedback
def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        feedback = request.POST.get('feedback')

        # Create a new Feedback object and save it to the database
        new_feedback = Feedback(name=name, email=email, phone=phone, address=address, feedback=feedback)
        new_feedback.save()

        messages.success(request, 'Your feedback is successfully sent!')

        return redirect('feedback')

    return render(request, 'app/feedback.html')

#display feedback
def feedbackk(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'app/feedbackk.html', {'feedbacks': feedbacks})

#report
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Sum

from django.db.models import Sum

def report(request):
    current_datetime = timezone.now()
    start_date_daily = current_datetime.date()
    end_date_daily = start_date_daily + timezone.timedelta(days=1)
    selected_month = request.GET.get('month')

    if selected_month and selected_month != 'all':
        selected_month_start = current_datetime.date().replace(day=1).replace(month=int(selected_month))
        selected_month_end = selected_month_start.replace(month=int(selected_month) + 1)
        transactions = Order.objects.filter(date_ordered__gte=selected_month_start, date_ordered__lt=selected_month_end, pay_status=True)
        monthly_profit = Order.objects.filter(date_ordered__gte=selected_month_start, date_ordered__lt=selected_month_end, pay_status=True).aggregate(total=Sum('total_amount'))['total'] or 0
        daily_profit = Order.objects.filter(date_ordered__gte=start_date_daily, date_ordered__lt=end_date_daily, pay_status=True).aggregate(total=Sum('total_amount'))['total'] or 0
    elif selected_month == 'all':
        transactions = Order.objects.filter(pay_status=True)
        monthly_profit = Order.objects.filter(pay_status=True).aggregate(total=Sum('total_amount'))['total'] or 0
        daily_profit = Order.objects.filter(date_ordered__gte=start_date_daily, date_ordered__lt=end_date_daily, pay_status=True).aggregate(total=Sum('total_amount'))['total'] or 0
    else:
        transactions = None
        monthly_profit = 0  # Set monthly profit as 0
        daily_profit = Order.objects.filter(date_ordered__gte=start_date_daily, date_ordered__lt=end_date_daily, pay_status=True).aggregate(total=Sum('total_amount'))['total'] or 0

    return render(request, 'app/reports.html', {
        'daily_profit': daily_profit,
        'monthly_profit': monthly_profit,
        'transactions': transactions,
        'selected_month': selected_month,
    })



#preset
'''def generate_otp(length=6):
    # Generate a random OTP
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(length))
    return otp


def send_otp_via_email(sender_email, sender_password, recipient_email, otp):
    # SMTP server configuration (for Gmail)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Email content
    subject = 'One-Time Password (OTP)'
    body = f'Your OTP is: {otp}'
    message = f'Subject: {subject}\n\n{body}'

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email to the recipient
        server.sendmail(sender_email, recipient_email, message)
        print(f'OTP sent to {recipient_email} successfully!')
        return True

    except Exception as e:
        print(f'Error sending the OTP: {e}')
        return False


def send_otp(request):
    if request.method == 'POST':
        # Set the sender's email and password
        sender_email = 'ramenterprise9a@gmail.com'
        sender_password = 'auywmyyqlgsvggwr'

        # Get the recipient's email from the form input
        recipient_email = request.POST.get('recipient_email')

        # Generate the OTP
        otp = generate_otp()

        # Send the OTP via email
        if send_otp_via_email(sender_email, sender_password, recipient_email, otp):
            request.session['otp'] = otp  # Store the OTP in the session for verification
            return redirect('verify_otp')  # Redirect to the verify_otp view
        else:
            return HttpResponse('Failed to send OTP.')

    # Render the template with the form
    return render(request, 'app/send_otp.html')

#verifu otp
def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')  # Retrieve the stored OTP from the session
            if otp == stored_otp:
                del request.session['otp']  # Delete the OTP from the session after successful verification
                messages.success(request, 'OTP verified successfully.')
                return redirect('change_password')  # Replace 'change-password' with the desired redirect page
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()

    return render(request, 'app/verify_otp.html', {'form': form})

#change password
from .custom_filters import custom_hash_function
from django.core.exceptions import ValidationError

def change_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('/change-password/')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email.')
            return redirect('/change-password/')

        user = usertable.objects.filter(email=email).first()
        if user:
            if user.otp == otp:
                hashed_password = custom_hash_function(new_password)
                user.password = hashed_password
                user.save()
                messages.success(request, 'Password successfully changed. Please log in with your new password.')
                return redirect('/login/')
            else:
                messages.error(request, 'Invalid OTP.')
                return redirect('/change-password/')
        else:
            messages.error(request, 'Invalid email.')
            return redirect('/change-password/')

    return render(request, 'app/change_password.html')'''



'''def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = usertable.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
            reset_url = request.build_absolute_uri(
                f'/password-reset-confirm/{uid}/{token}/'
            )
            email_subject = 'Password Reset Request'
            email_body = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
                'site_name': get_current_site(request).name,
            })
            send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email])
        return redirect('password_reset_done')
    return render(request, 'password_reset_form.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            return redirect('password_reset_complete')
    
    return render(request, 'password_reset_confirm_form.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')'''


# otp
import random
from django.core.mail import send_mail

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = usertable.objects.filter(email=email).first()

        if user:
            # Generate a 6-digit OTP
            otp = ''.join(random.choices('0123456789', k=6))

            # Save the OTP in the user object
            user.otp = otp
            user.save()

            # Send the OTP to the user's email
            subject = 'Password Reset OTP'
            message = f'Your OTP is: {otp}'
            from_email = 'ramenterprise9a@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            # Render the OTP verification form
            return render(request, 'app/verify_otp.html', {'email': email})
        else:
            message = "This email is not registered!"
            return render(request, 'app/forgot_password.html', {'msg': message})

    return render(request, 'app/forgot_password.html')

#verify otp
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        user = usertable.objects.filter(email=email, otp=otp).first()

        if user:
            # Clear the OTP field
            user.otp = None
            user.save()

            # Render the password reset form
            return render(request, 'app/reset_password.html', {'email': email})
        else:
            message = "Invalid OTP!"
            return render(request, 'app/verify_otp.html', {'email': email, 'msg': message})

    return render(request, 'app/verify_otp.html')

#update new password
def update_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            # Find the user by email
            user = usertable.objects.filter(email=email).first()

            if user:
                # Update the user's password
                user.password = new_password
                user.save()

                return render(request, 'app/login.html')
            else:
                message = "User not found!"
                return render(request, 'app/reset_password.html', {'email': email, 'msg': message})
        else:
            message = "Passwords do not match!"
            return render(request, 'app/reset_password.html', {'email': email, 'msg': message})

    return render(request, 'app/reset_password.html')