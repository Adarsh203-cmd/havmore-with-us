
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
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator 
from .models import *
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now


# Create your views here.
def loginview(request):
    return render(request,"app/login.html")

#loginad
def loginrview(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'ramenterprise9a@gmail.com' and password == 'havmor@123':
            return render(request, 'app/reports.html')
        
    return render(request, 'app/login1.html')

def menuview(request):
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


# Login Function
def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = usertable.objects.get(email=email)
            
            if check_password(password, user.password):  # Validate password
                user.last_login = now()
                user.save()
                
                # Store user details in session
                request.session['user_id'] = user.id  # Use user ID for uniqueness
                request.session['name'] = user.cname
                request.session['email'] = user.email  # Optional

                if user.is_superuser:  # Admin check
                    return redirect('controls')  # Redirect to admin page
                else:
                    return redirect('items')  # Redirect to user dashboard
            else:
                return render(request, 'login.html', {'error': 'Invalid password.'})
        
        except usertable.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist.'})
    
    return render(request, 'login.html')

def logout(request):
    return render(request, "app/login1.html")
#singupview
def signup(request):
    return render(request,"app/signup.html")

#forgotp
def forgotview(request):
    return render(request,"app/forgotp.html")

def newpassword(request):
    return render(request,"app/newpassword.html")

# Email OTP Verification
from django.shortcuts import redirect

# Email OTP Verification
def verify_email_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']

        # Check if the email and OTP match
        user = usertable.objects.filter(email=email, otp=otp).first()

        if user:
            # Clear the OTP and mark the user as verified
            user.otp = None
            user.is_verified = True
            user.save()

            # Display a success message and redirect to login
            messages.success(request, "Your account has been verified! You can now log in.")
            return redirect('login')  # Redirect to the login page route
        else:
            # Display an error message if OTP is invalid
            message = "Invalid OTP! Please try again."
            return render(request, 'app/verify_otp.html', {'email': email, 'msg': message})

    return render(request, 'app/verify_otp.html')



# Register user function
def registeruser(request):
    if request.method == 'POST':
        # Retrieve user details from the form
        name = request.POST['name']
        pno = request.POST['number']
        email = request.POST['email']
        add = request.POST['address']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # Validate if passwords match
        if password != cpassword:
            message = "Passwords do not match! Please try again."
            return render(request, "app/signup.html", {'msg': message})

        # Check if the email is already registered
        if usertable.objects.filter(email=email).exists():
            message = "This email ID is already registered! Please re-enter."
            return render(request, "app/signup.html", {'msg': message})

        # Create a new user instance
        user = usertable(
            cname=name,
            cno=pno,
            email=email,
            address=add,
            is_verified=False  # Mark as not verified initially
        )
        user.set_password(password)  # Hash the password before saving
        user.save()

        # Generate a 6-digit OTP for verification
        otp = ''.join(random.choices('0123456789', k=6))

        # Save the OTP to the user object
        user.otp = otp
        user.save()

        # Send the OTP to the user's email
        subject = 'Verify Your Account - OTP'
        message = f'Hi {user.cname},\n\nYour OTP for account verification is: {otp}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            # Handle email sending failure
            user.delete()  # Remove the user record since email failed
            message = f"Failed to send OTP. Please try again later. Error: {str(e)}"
            return render(request, "app/signup.html", {'msg': message})

        # Redirect to OTP verification page
        return render(request, "app/verify_otp_email.html", {'email': email})
    
    # Render the sign-up page for GET requests
    return render(request, "app/signup.html")

def showp(request):
    return render(request,"app/show.html")

# Place Order
def place_order(request):
    if request.method == 'POST':
        items = Items.objects.all()
        checked_items = []
        user_id = request.session.get('user_id')  # Fetch user ID from session
        
        if not user_id:
            return redirect('login')  # Redirect to login if user is not logged in
        
        for item in items:
            item_id = str(item.id)
            checkbox_name = f'item_checkbox_{item_id}'
            quantity_name = f'quantity_{item_id}'

            if checkbox_name in request.POST:
                quantity = int(request.POST.get(quantity_name, '0'))
                if quantity > 0:
                    checked_items.append((item, quantity))

        if not checked_items:
            message = "Please use the checkbox to select Items."
            return render(request, 'app/user1.html', {'message': message})
        
        # Retrieve the logged-in user
        user = get_object_or_404(usertable, id=user_id)
        order = Order.objects.create(user=user, total_amount=0)
        total_amount = 0

        # Process selected items
        for item, quantity in checked_items:
            OrderItem.objects.create(order=order, item=item, quantity=quantity)
            total_amount += item.rate * quantity
            item.avail_stock = F('avail_stock') - quantity
            item.ci_stock = F('ci_stock') - quantity
            item.save()
        
        # Update order total
        order.total_amount = total_amount
        order.save()

        context = {
            'order': order,
            'order_items': checked_items,
            'total_amount': total_amount,
        }
        
        return render(request, 'app/success.html', context)
    
    items = Items.objects.all()
    return render(request, 'app/user1.html', {'items': items})
    
# Admin Order Details
def orders(request):
    orders = Order.objects.order_by('-date_ordered').select_related('user')
    return render(request, "app/corder.html", {'key5': orders})
    

#status update
def update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        # Optionally, you can redirect to a different page or render a success message here.

    return redirect('orders')

# User's Orders
def display_orders(request):
    user_id = request.session.get('user_id')  # Use user ID to fetch orders
    
    if not user_id:
        return redirect('login')  # Redirect to login if user is not logged in
    
    user = get_object_or_404(usertable, id=user_id)
    orders = Order.objects.filter(user=user).order_by('-date_ordered')
    
    return render(request, 'app/orders.html', {'orders': orders, 'user': user})

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


from datetime import datetime

# Helper function to check if the card is expired
def is_card_expired(expiry_month, expiry_year):
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Convert inputs to integers (in case they're passed as strings)
    expiry_month = int(expiry_month)
    expiry_year = int(expiry_year)

    # If the expiry year is in the past
    if expiry_year < current_year:
        return True
    # If the expiry year is the current year but the month is in the past
    if expiry_year == current_year and expiry_month < current_month:
        return True

    # The card is not expired
    return False

    
#payment
def payment(request, order_id):
    print("Payment function called")
    if request.method == 'POST':
        name_on_card = request.POST.get('nameoncard')
        card_number = request.POST.get('cardnumber')
        expiry_month = request.POST.get('month')
        expiry_year = request.POST.get('year')
        csv = request.POST.get('csv')

        # Check if the card is expired
        if is_card_expired(expiry_month, expiry_year):
            return render(request, 'payment_form.html', {
                'order_id': order_id,
                'error': 'Card is expired. Please use a valid card.'
            })

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
                user.set_password(new_password)  # Hash the password before saving
                user.save()

                return render(request, 'app/login.html')
            else:
                message = "User not found!"
                return render(request, 'app/reset_password.html', {'email': email, 'msg': message})
        else:
            message = "Passwords do not match!"
            return render(request, 'app/reset_password.html', {'email': email, 'msg': message})

    return render(request, 'app/reset_password.html')