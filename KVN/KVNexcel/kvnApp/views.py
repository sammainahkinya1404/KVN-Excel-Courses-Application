from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from validate_email import validate_email
from .models import Profile
from .forms import LoginForm, SignUpForm, VideoCourseForm
from django.core.mail import EmailMessage
from django.conf import settings
from .decorators import auth_user_should_not_access
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str,DjangoUnicodeDecodeError
from .utils import generate_token
import threading
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('Activation.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()

# @auth_user_should_not_access
def Login(request):
    form = SignUpForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified:
            messages.error(request, 'Email is not verified, please check your email inbox')
            return render(request, 'Login.html')

        if not user:
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'Login.html')

        login(request, user)

        return redirect(reverse('Dashboard'))

    return render(request, 'Login.html', {'form':form})

# @auth_user_should_not_access
def Register(request):
    form = SignUpForm()

    if request.method == "POST":
        context = {'has_error': False}
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.error(request, 'Password should be at least 6 characters for greater security')
            return redirect('Register')

        if password1 != password2:
            messages.error(request, 'Password Mismatch! Your Passwords Do Not Match')
            return redirect('Register')

        if not validate_email(email):
            messages.error(request, 'Password Mismatch! Your Passwords Do Not Match')
            return redirect('Register')

        if not username:
            messages.error(request, 'Username is required!')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken! Choose another one')

            return render(request, 'Register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken! Choose another one')

            return render(request, 'Register.html')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.save()

        if not context['has_error']:
            send_activation_email(user, request)

            messages.success(request, 'Sign Up Successful! We sent you an email to verify your account')
            return redirect('Register')

    return render(request, 'Register.html', {'form':form})

def Logout(request):
    
    logout(request)
    messages.success(request, 'Successfully Logged Out!')

    return redirect(reverse('Login'))

def ActivateUser(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.success(request, 'Email Verified! You can now Log in')
        return redirect(reverse('Login'))

    return render(request, 'Activation Failed.html', {"user": user})



from django.shortcuts import render
from .models import Video_courses, UserSubscription
def Dashboard(request):
    subscribed_courses = UserSubscription.objects.filter(user=request.user).select_related('module','transaction')
    user_favorites = request.session.get('user_favorites', [])
    
    context = {'subscribed_courses': subscribed_courses, 'user_favorites': user_favorites}
    return render(request, 'Dashboard.html', context)


  # Create your views here.
from django.db.models import Count

def home(request):
    videos = Video_courses.objects.filter(level='Basic')

    module_name = 'Basic'

    module = SubscriptionModule.objects.get(name=module_name)  # Assuming you have a 'name' field in SubscriptionModule
    learners = UserSubscription.objects.filter(module=module)
    views = learners.count()
    
    # Calculate counts for each topic
    excel101_count = videos.filter(topic='Excel101').count()
    excel_shortcuts_count = videos.filter(topic='Excel Shortcuts').count()
    conditional_formatting_count = videos.filter(topic='Conditional Formating').count()
    math_count = videos.filter(topic='Maths').count()
    
    return render(request, 'index.html', {
        'videos': videos,
        'excel101_count': excel101_count,
        'excel_shortcuts_count': excel_shortcuts_count,
        'conditional_formatting_count': conditional_formatting_count,
        'math_count': math_count,
        'learners':learners,
        'views':views,
    })



def adv(request):
     videos=Video_courses.objects.filter(level='Advanced')
     formula_count=Video_courses.objects.filter(topic='Formulas').count()
     visual_count=Video_courses.objects.filter(topic='Visualization').count()
     pivotal_count=Video_courses.objects.filter(topic='Pivot Tables').count()
     analysis_count=Video_courses.objects.filter(topic='Data Analysis').count()
     array_count=Video_courses.objects.filter(topic='Arrays').count()
     powerbi_count=Video_courses.objects.filter(topic='Power Bi').count()

     module_name = 'Advanced'

     module = SubscriptionModule.objects.get(name=module_name)  # Assuming you have a 'name' field in SubscriptionModule
     learners = UserSubscription.objects.filter(module=module)
     views = learners.count()
      
     return render(request,'advanced.html',
                   {
                     'videos':videos,
                     'formula_count':formula_count,
                     'visual_count':visual_count,
                     'pivotal_count':pivotal_count,
                     'analysis_count':analysis_count,
                     'array_count':array_count,
                     'powerbi_count':powerbi_count,
                     'learners':learners,
                     'views':views,
                     


                   }
                   )

def analysis(request):
    videos=Video_courses.objects.filter(level='Advanced',topic='Data Analysis')
    return render(request, 'advanced/analysis.html',{'videos':videos})

def arrays(request):
    videos=Video_courses.objects.filter(level='Advanced',topic='Arrays')
    return render(request, 'advanced/arrays.html',{'videos':videos})

def formulas(request):
    videos=Video_courses.objects.filter(level='Advanced',topic='Formulas')
    return render(request, 'advanced/formulas.html',{'videos':videos})


def pivotal(request):
    videos=Video_courses.objects.filter(level='Advanced',topic='Pivot Tables') 
    return render(request, 'advanced/pivotal.html',{'videos':videos})

def powerbi(request):
    videos=Video_courses.objects.filter(level='Advanced',topic='Power Bi')
    return render(request, 'advanced/powerbi.html',{'videos':videos})

def visual(request):
    videos=Video_courses.objects.filter(level='Advanced',topic='Visualization')
    return render(request, 'advanced/visual.html',{'videos':videos})




def hyb(request):
     module_name = 'Hybrid'

     module = SubscriptionModule.objects.get(name=module_name)  # Assuming you have a 'name' field in SubscriptionModule
     learners = UserSubscription.objects.filter(module=module)
     views = learners.count()
     return render(request,'hybrid.html',{
         'learners':learners,
          'views':views,
     })

def cart(request):
   
    return render(request,'cart.html')
def video(request):
    

    if request.method == 'POST':
        form = VideoCourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pricing')  # Redirect to a page showing all uploaded video courses
    else:
        form = VideoCourseForm()

    return render(request, 'courses1.html', {'form': form})
# @login_required
def pricing(request):
    return render(request, 'pricing.html')
from django.shortcuts import render
from .models import Video_courses
# 

def basic_courses(request):
    courses = Video_courses.objects.filter(level='Basic',topic='Excel101')
    return render(request, 'basic/Excel101.html', {'courses': courses})


def Excel_shortcuts(request):
    courses = Video_courses.objects.filter(level='Basic',topic='Excel Shortcuts')
    return render(request, 'basic/Excel_shortcuts.html', {'courses': courses})

def Conditional_formating(request):
    courses = Video_courses.objects.filter(level='Basic',topic='Conditional Formating')
    return render(request, 'basic/Coditional_formating.html',{'courses': courses})
def Maths(request):
    courses = Video_courses.objects.filter(level='Basic',topic='Maths')
    return render(request, 'Basic/Maths.html',{'courses': courses})

def advanced_courses(request):
    courses = Video_courses.objects.filter(level='Advanced')
    return render(request, 'adv_courses.html', {'courses': courses})

@login_required
def R_advanced(request):
    courses=Video_courses.objects.filter(level='R_Advanced')
    return render(request, 'R_Advanced.html',{'courses': courses})

@login_required
def R_basic(request):
    courses=Video_courses.objects.filter(level='R_Basic')
    return render(request, 'R_Basic.html',{'courses': courses})

#login_required
import requests
import base64
import json
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import Transaction
from .generateAccesstoken import get_access_token
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import base64
from datetime import datetime
from .models import SubscriptionModule, Transaction, Video_courses
@login_required
# In views.py

# ...

@login_required
# In views.py

# ...

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        module_name = request.POST.get('item')
        phone_number = request.POST.get('phone_number')

        # Check if the selected module exists
        subscription_module = get_object_or_404(SubscriptionModule, name=module_name)
        amount = subscription_module.price

        access_token_response = get_access_token(request)
        if isinstance(access_token_response, JsonResponse):
            access_token = access_token_response.content.decode('utf-8')
            access_token_json = json.loads(access_token)
            access_token = access_token_json.get('access_token')
            if access_token:
                business_short_code = '174379'
                passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
                callback_url = 'https://mydomain.com/path'
                reference = 'KVNExcel LTD'
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
                party_a = phone_number

                stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                stk_push_headers = {
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json'
                }

                stk_push_payload = {
                    'BusinessShortCode': business_short_code,
                    'Password': password,
                    'Timestamp': timestamp,
                    'TransactionType': 'CustomerPayBillOnline',
                    'Amount': float(amount),  # Convert amount to float
                    'PartyA': party_a,
                    'PartyB': business_short_code,
                    'PhoneNumber': party_a,
                    'CallBackURL': callback_url,
                    'AccountReference': reference,
                    'TransactionDesc': f'Payment for {module_name}'
                }

                try:
                    response = requests.post(stk_push_url, headers=stk_push_headers, json=stk_push_payload)
                    response.raise_for_status()
                    response_data = response.json()
                    checkout_request_id = response_data['CheckoutRequestID']
                    response_code = response_data['ResponseCode']

                    if response_code == "0":
                        # Create a Transaction object referencing the selected subscription module
                        transaction = Transaction.objects.create(
                            purchased_by=request.user,
                            item=subscription_module,
                            amount=amount,
                            phone_number=phone_number
                        )
                        
                        # Create a UserSubscription instance to associate the user, course, and transaction
                        UserSubscription.objects.create(
                            user=request.user,
                            module=subscription_module,
                            transaction=transaction
                        )

                        return JsonResponse({'CheckoutRequestID': checkout_request_id, 'ResponseCode': response_code, 'Amount': float(amount)})

                    else:
                        return JsonResponse({'error': 'STK push failed.'})
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'error': 'Access token not found.'})
        else:
            return JsonResponse({'error': 'Failed to retrieve access token.'})
    else:
        return render(request, 'payment_processing.html', {'items': ['Basic', 'Advanced', 'Hybrid']})



def user_details(request):
    return render(request, 'user_details.html')

from django.shortcuts import render
from .models import Video_courses, UserProgress

def basic_dashboard(request):
    # Retrieve basic level courses from the database
    basic_courses = Video_courses.objects.filter(level='Basic')

    # Retrieve basic level topics (assuming topics are stored in the 'topic' field)
    basic_topics = Video_courses.objects.filter(level='Basic').values_list('topic', flat=True).distinct()

    # Retrieve user progress for the logged-in user (you may need to adjust this based on your authentication system)
    user_progress = UserProgress.objects.filter(user=request.user)

    context = {
        'level': 'Basic',
        'courses': basic_courses,
        'topics': basic_topics,
        'user_progress': user_progress,
    }

    return render(request, 'course/basic_dashboard.html', context)

def advanced_dashboard(request):
    # Retrieve advanced level courses from the database
    advanced_courses = Video_courses.objects.filter(level='Advanced')

    # Retrieve advanced level topics (assuming topics are stored in the 'topic' field)
    advanced_topics = Video_courses.objects.filter(level='Advanced').values_list('topic', flat=True).distinct()

    # Retrieve user progress for the logged-in user (you may need to adjust this based on your authentication system)
    user_progress = UserProgress.objects.filter(user=request.user)

    context = {
        'level': 'Advanced',
        'courses': advanced_courses,
        'topics': advanced_topics,
        'user_progress': user_progress,
    }

    return render(request, 'course/advanced_dashboard.html', context)

def playground(request):
    return render(request, 'playground.html')
def corp(request):
    return render(request, 'corprate.html')