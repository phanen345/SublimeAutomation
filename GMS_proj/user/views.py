from django.shortcuts import render,redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os
from django.http import HttpResponseBadRequest
from google.oauth2 import id_token
from google.auth.transport import requests
import requests
from google.auth.transport.requests import Request
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password,check_password
from shared_model.models import Profile
from shared_model.models import ComplaintMessage
from .middleware import auth, login_checker
from shared_model.models import CreateComplaint
from django.utils import timezone
from datetime import datetime
from django.utils.crypto import get_random_string
from .exceptions import AuthCanceled
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from pytz import timezone as pytz_timezone
from django.utils.timezone import activate
from django.contrib.auth.middleware import get_user
# def emp_profile_admin(request):
#     return render(request, 'emp_profile_admin.html')
# def view_emp_profile_admin(request):
#     return render(request, 'view_emp_profile_admin.html')
#########User section############
##GOOGLE OAUTH2
def google_auth(request):
    # Redirect to Google OAuth consent screen
    google_auth_url = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=762745589913-76oh6hhoomkv428f13vp76pcnksupfid.apps.googleusercontent.com&redirect_uri=http://localhost:8000/auth/google/callback&scope=openid%20email%20profile"
    return redirect(google_auth_url)
import requests
from google.oauth2 import id_token
from google.auth.transport.requests import Request
@login_checker
def google_auth_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error == 'access_denied':
        print("ERROR IS", error)
        # Handle access denied error, e.g., redirect to a specific page
        return redirect('user:login')  # Adjust URL as needed
    else:
        if code:
            try:
                # Exchange authorization code for ID token
                token_url = "https://oauth2.googleapis.com/token"
                token_data = {
                    'code': code,
                    'client_id': '762745589913-76oh6hhoomkv428f13vp76pcnksupfid.apps.googleusercontent.com',
                    'client_secret': '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',
                    'redirect_uri': 'http://localhost:8000/auth/google/callback',
                    'grant_type': 'authorization_code',
                }
                token_response = requests.post(token_url, data=token_data)
                id_token_info = id_token.verify_oauth2_token(token_response.json()['id_token'], Request())
                email = id_token_info.get('email')
                
                if Profile.objects.filter(email=email).exists():
                    user = Profile.objects.get(email=email)
                    request.session['is_logged_in'] = True
                    request.session['profile_id'] = user.id
                    request.session['name'] = user.name             
                    request.session['profile_type_id'] = user.profile_type_id   
                    print("EMAIL EXIST IN DB", email) 
                    return redirect("user:dashboard") 
                else:
                    print("Email does not exist in db", email)
                    password = get_random_string(8)
                    profile_type_id = 2
                    name = id_token_info.get('name')
                    user = Profile.objects.create(name=name, email=email, password=password, profile_type_id=profile_type_id)
                    print(user)
                    request.session['is_logged_in'] = True
                    return redirect("user:dashboard") 
            except Exception as e:
                print("Exception:", e)
                return HttpResponseBadRequest("Failed to authenticate with Google.")

        else:
            return HttpResponseBadRequest("Authorization code not provided.")
@auth
def edit_profile(request):
            p_id=request.session.get("profile_id")
            if request.method == 'POST':
                            name = request.POST.get('name','')
                            mobile = request.POST.get('mobile','')
                            email = request.POST.get('email','')
                            error_msg = []

                            response_data = {
                                'status':'',
                                'message':[],
                                'data':''
                            }
                            if name == '':
                                error_msg.append('Field Name cannot be Empty.')
                            if email == '':
                                error_msg.append('Field Email cannot be Empty.')
                            if mobile == '':
                                error_msg.append('Field Mobile Number cannot be Empty.')
                            if len(mobile) != 10:
                                error_msg.append('Mobile number must be 10 character in length.')
                            if Profile.objects.filter(email=email).exclude(id=p_id).exists():
                                error_msg.append('Email already exists. Please use a different email address.')
                            if Profile.objects.filter(mobile=mobile).exclude(id=p_id).exists():
                                error_msg.append('Mobile Number already exists. Please use a different Mobile No.')
                            profile = None
                            if p_id is not None:
                                # Fetch the existing profile if it exists
                                try:
                                    profile = Profile.objects.get(id=p_id)
                                except Profile.DoesNotExist:
                                    profile = None
                                    print('esser jkhkjh')
                            print(error_msg)
                            if(len(error_msg) == 0):
                                # Update only the fields provided in the POST request
                                print("Name:", name)
                                print("Mobile:", mobile)
                                print("Email:", email)
                                # if name:
                                #     profile.name = name
                                # if mobile:
                                #     profile.mobile = mobile
                                # if email:
                                #     profile.email = email
                                # else:
                                profile.name = name
                                profile.mobile = mobile
                                profile.email = email    
                                profile.save()     
                                print("Name:", name)
                                print("Mobile:", mobile)
                                print("Email:", email)
                                response_data['status'] = 'success'
                                response_data['message'] = ['Profile Updated Successfully.']
                                # Construct response data with updated name value
                                response_data = {
                                    'status': 'success',
                                    'message': ['Profile Updated Successfully.'],
                                    'data': {
                                        'name': name,  # Pass the updated name explicitly
                                        'mobile': mobile,
                                        'email': email
                                    }
                                }
                            else:
                                # Construct response data with error message and original data
                                response_data = {
                                    'status': 'error',
                                    'message': error_msg,
                                    'data': {
                                        'name': profile.name if profile else '',
                                        'mobile': profile.mobile if profile else '',
                                        'email': profile.email if profile else ''
                                    }
                                }
                            return render(request, 'profile.html', response_data)
            else:
                # chg_profile = get_object_or_404(Profile, id=p_id)
                # return render(request, 'profile.html', {'chg_profile': chg_profile})
                print("POST not done")
                pass
            
    

# def logout_user(request):
# #     logout(request)
# def login_with_google(request):
#     print("...............................................................")
#     profile_type="User"
#     print(type(request.user))
#     email=request.user.email
#     request.session['email_id'] = email
#     request.session['is_logged_in'] = True
#     if Profile.objects.filter(email=email).exists():
#         print("EMAIL EXIST IN DB",email) 
#         return redirect("user:dashboard") 
#     else:
#         try:
#              # Optionally, you can render an erro
#             print("Email does not exist in db",email)
#             password = get_random_string(8)
#             name = request.user.first_name + " " + request.user.last_name
#             user=Profile.objects.create(name=name,email=email, password=password,profile_type=profile_type)
#             print(user)
#             request.session['is_logged_in'] = True
#             return redirect("user:dashboard") 
#          # Your view logic here
#         except AuthCanceled as e:
#             # Handle the AuthCanceled exception
#             print(f"Authentication canceled by gmail: {e}")
#             return redirect(reverse('user:login'))
        


@auth
def navigation(request):
    return render(request, 'navigation_user.html')
#########User section############
@auth
def dashboard(request):
    p_id=request.session.get("profile_id")
    complaints = CreateComplaint.objects.filter(profile_id=p_id)
    request.session['is_logged_in'] = True
    return render(request, 'user/dashboard.html', {'complaints': complaints})

@auth
def profile(request):
    profile_id = request.session.get('profile_id')
    print("PROFILE ID IS",profile_id)
    if profile_id is not None:
                print("Working id is", profile_id)
                profile = get_object_or_404(Profile, id=profile_id)
                return render(request, 'profile.html', {'profile': profile})
    else:
         print("Not working")
    return render(request, 'profile.html')

@login_checker
def forgot_password(request):
    return render(request, 'forgot_password.html')
@login_checker 
def login(request): 
        response_data = {
            'status': '',
            'message': [],
            'data': '',
        }

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = Profile.objects.get(email=email)
                if Profile.objects.filter(email=email).exists() and check_password(password, user.password) and user.profile_type_id==2:

                    request.session['is_logged_in'] = True
                    request.session['email_id'] = user.email
                    request.session['profile_id'] = user.id
                    request.session['name'] = user.name
                    request.session['profile_type_id'] = user.profile_type_id
                    # Check if the provided password matches the hashed password
                    # Both email exists and password matches, redirect to dashboard
                    print('login function User App')
                    print(request.session.items())
                    return redirect("user:dashboard") 
                else:
                    # User with given email doesn't exist
                    request.session['is_logged_in'] = False
                    response_data['status'] = 'error'
                    response_data['message'] = ['Invalid Credentials Provided']
            except Profile.DoesNotExist:
                request.session['is_logged_in'] = False
                response_data['status'] = 'error'
                response_data['message'] = ['Invalid Credentials Provided']
                # response_data['data'] = request.POST
       
        
        return render(request, 'login.html', response_data)
# @auth
def logout_view(request):
                # Clear session data
                request.session.clear()
                # Redirect to the login page or any other desired page
                return redirect('user:login')
@login_checker
def registration_user(request):
                if request.method == 'POST':

                    name = request.POST.get('name','')
                    mobile = request.POST.get('mobile','')
                    email = request.POST.get('email','')
                    password = request.POST.get('password','')
                    confirm_password = request.POST.get('confirm_password','')
                

                    error_msg = []

                    response_data = {
                        'status':'',
                        'message':[],
                        'data':''
                    }
                    

                    if name == '':
                        error_msg.append('Field Name cannot be Empty.')
                    if email == '':
                        error_msg.append('Field Email cannot be Empty.')
                    if mobile == '':
                        error_msg.append('Field Mobile Number cannot be Empty.')
                    if password == '':
                        error_msg.append('Field Password cannot be Empty.')
                    if confirm_password == '':
                        error_msg.append('Field Confirm Password cannot be Empty.')

                    try:
                        validate_email(email)
                    except ValidationError as e:
                        error_msg.append('Invalid Email Provided')
                    else:
                        pass

                    if len(mobile) != 10:
                        error_msg.append('Mobile number must be 10 character in length.')

                    if password != confirm_password:
                        error_msg.append('Password donot match confirm password.') 

                    if Profile.objects.filter(email=email).exists():
                            error_msg.append('Email already exists. Please use a different email address.')
                            
                    if(len(error_msg) == 0):
                        response_data['status'] = 'success'
                        response_data['message'] = ['User Registered Successfully.']
                        response_data['data'] = []
                        hashed_password=make_password(password)
                        # If the email doesn't exist, create a new Profile object
                        profile_type = "User"
                        profile_type_id=2
                        user = Profile.objects.create(name=name, mobile=mobile, email=email, password=hashed_password,profile_type=profile_type,profile_type_id=profile_type_id)
                    else:
                        response_data['status'] = 'error'
                        response_data['message'] = error_msg
                        response_data['data'] = request.POST
                    

                    return render(request,'registration_user.html',response_data)
                else:
                    return render(request, 'registration_user.html')

#########Complaint section############
@auth
def complaint(request, operation):
    match operation:
        case 'home':
             return render(request, 'complaint_dashboard.html')
             

        case 'create':
                    if request.method == 'POST' and request.session['is_logged_in'] == True or request.FILES.get('image'):
                            # Retrieve the profile_id from the session
                            # print("REQUEST.FILES",request.FILES)
                            p_id = request.session.get('profile_id')
                            profile = Profile.objects.get(id=p_id)
                            complaint=CreateComplaint.objects.filter(profile_id=p_id)
                            
                            # Now you can use profile_id in this function
                            # For example, print it
                            print("Profile ID:", p_id)
                            print("Profile email:", profile.name)
                            print("Profile mobile:", profile.mobile)
                            # Get the timezone object for Asia/Kolkata
                            kolkata_timezone = pytz_timezone('Asia/Kolkata')

                            # Activate Asia/Kolkata timezone
                            activate(kolkata_timezone)

                            # Get the current time in Asia/Kolkata timezone
                            current_time_in_raipur = timezone.localtime(timezone.now())
                            
                            subject=request.POST.get("subject","")
                            message=request.POST.get("message","")
                            error_msg = []

                            response_data = {
                                'status':'',
                                'message':[],
                                'data':''
                            }
                        
                            if subject == '':
                                error_msg.append('Field Subject cannot be Empty.')
                    
                            if message == '':
                                error_msg.append('Field Message cannot be Empty.')
                            
                            formatted_date_old=current_time_in_raipur.strftime('%d%m%Y')
                            # complaint_id_with_date = f"{formatted_date_old}{complaint.id}"
                            if(len(error_msg) == 0):
                                response_data['status'] = 'success'
                                response_data['message'] = ['Complaint Registered Successfully.']
                                response_data['data'] = []
                            
                                
                                # Format the date and time in dd/mm/yyyy hh:mm format
                                # Assuming current_time_in_raipur is a datetime object
                                formatted_date_time = current_time_in_raipur.strftime('%Y-%m-%d %H:%M')
                                
                                file=request.FILES.get('image')
                                if file:
                                    fs=FileSystemStorage()
                                    filename=fs.save(file.name,file)
                                    url=fs.url(filename)
                                    # formatted_date_time_obj = datetime.strptime(formatted_date_time, '%Y-%m-%d %H:%M')
                                    
                                    # Save the file path to the model instance
                                    
                                    # Convert formatted date time string to datetime object
                                    
                                    complaint = CreateComplaint.objects.create(profile_id=p_id, subject=subject, message=message,created_at=formatted_date_time,image=url,updated_at=formatted_date_time)
                                    print("COMPLAINT CREATED",complaint)
                                    # Generate the complaint ID with the date format
                                    
                                    return render(request, 'complaint_user.html', response_data)
                                elif not file:
                                    url="Null"
                                    complaint = CreateComplaint.objects.create(profile_id=p_id, subject=subject, message=message,created_at=formatted_date_time,image=url,updated_at=formatted_date_time)
                                    print("COMPLAINT CREATED",complaint)
                                    return render(request, 'complaint_user.html', response_data)
                            else:
                                response_data['status'] = 'error'
                                response_data['message'] = error_msg
                                response_data['data'] = request.POST
                        

                            return render(request,'complaint_user.html',response_data)
                    else:
                        return render(request, 'complaint_user.html')
        case 'view':
               complaint_id = request.GET.get('id')
               request.session['complaint_id'] = complaint_id
               if complaint_id is not None:
                print("Working id is", complaint_id)
                complaint = get_object_or_404(CreateComplaint, id=complaint_id)
                return render(request, 'specific_complaint.html', {'complaint': complaint})
               else:
                p_id = request.session.get('profile_id')
                print("profile_id",p_id)
                complaints = CreateComplaint.objects.filter(profile_id=p_id)
                return render(request, 'complaint_list_user.html', {'complaints': complaints})
               
        case 'list':
               complaint_id = request.GET.get('id')
               request.session['complaint_id'] = complaint_id
               if complaint_id is not None:
                print("Working id is", complaint_id)
                complaint = get_object_or_404(CreateComplaint, id=complaint_id)
                return render(request, 'specific_complaint.html', {'complaint': complaint})
               else:
                p_id = request.session.get('profile_id')
                print("profile_id",p_id)
                complaints = CreateComplaint.objects.filter(profile_id=p_id)
                return render(request, 'complaint_list_user.html', {'complaints': complaints})
               
                # profile_id = request.GET.get('id')
                # if profile_id is not None:
                    
                #     complaints = CreateComplaint.objects.filter(profile_id=profile_id)

                #     return render(request, 'complaint_list_user.html', {'complaints': complaints}) 
                # else:
                #     ###if id matches with the complaint created those complaints only show it to the user
                    
                #     complaints = CreateComplaint.objects.all()
                #     return render(request, 'complaint_list_user.html', {'complaints': complaints})  
        case 'message':
            #request.session['is_logged_in'] = True
            profile_id = request.session.get('profile_id')
            complaint_id = request.GET.get('id')
            print("COMPLAINT ID IS THIS:",complaint_id)
            # profile_type_id=request.session.get('profile_type_id')
            # print("COMPLAINT ID REPLY",complaintid)
            if request.method=='POST':
                 message= request.POST.get('message')
                 complaint_id= request.POST.get('complaint_id')
                 print("ID IS",complaint_id)
                # Get the timezone object for Asia/Kolkata
                 kolkata_timezone = pytz_timezone('Asia/Kolkata')
                 
                # Activate Asia/Kolkata timezone
                 activate(kolkata_timezone)

                # Get the current time in Asia/Kolkata timezone
                 current_time_in_raipur = timezone.localtime(timezone.now())
                 reply = ComplaintMessage.objects.create( profile_id=profile_id,message=message, created_at=current_time_in_raipur,complaint_id=complaint_id)
                #  reply = Reply.objects.all()
                #  request.session['id']=reply.id
                #showing the chats
                 chat = ComplaintMessage.objects.filter(complaint_id=complaint_id)
            else:
                 
                 chat = ComplaintMessage.objects.filter(complaint_id=complaint_id)


            return render(request, 'user/reply_user.html',{'complaintid':complaint_id,'chats': chat})


# def change_password(request):
#     if request.method == 'POST':
#         old_password = request.POST.get('old_password','')
#         new_password = request.POST.get('new_password','')
#         confirm_password = request.POST.get('confirm_password')

#         profile = request.user.Profile
        
             

#         error_msg =[]
#         response_data = {
#              'status':'',
#              'message':'',
#              'data':''
#         }


#         if not check_password(old_password, request.user.password):
#             messages.error(request, 'Incorrect old password.')
#             return redirect('change_password')

#         # Check if new password and confirm password match
#         if new_password != confirm_password:
#             messages.error(request, 'New password and confirm password do not match.')
#             return redirect('change_password')
        
#         profile.user.set_password(new_password)
#         profile.user.save()

#         messages.success(request, 'Password successfully updated.')
#         return redirect('profile')
#     return  render(request,'change_password.html')

# def profile_update(request):
#     p_id = request.session.get('profile_id')
#     print(p_id)
#     return render(request,'profile.html')


#Authentication login

# def oauth_gmail_login(request):
#     # Redirect to Gmail authentication
#     print("My URL:::",'social:begin', 'google-oauth2')
#     return redirect('social:begin', 'google-oauth2')


# def oauth_callback(request):
#     # Process the callback from the authentication provider
#     return redirect('user:dashboard')


# # def custom_login(request):
# #     print('..................Success ......................')
# #     profile_type="User"
# #     # print(type(request.username))
# #     # email=request.user.email
# #     # print(vars(request.user))
    
# #     # print(request.email)
# #     # print(user_lazy.is_authenticated)  # Accessing an attribute to force evaluation
# #     # print(user_lazy._wrapped)
# #     # request.session['email_id'] = email
# #     # request.session['is_logged_in'] = True
# #     # if Profile.objects.filter(email=email).exists():
# #     #     print("EMAIL EXIST IN DB",email) 
# #     #     return redirect("user:dashboard") 
# #     # else:
# #     #     try:
# #     #          # Optionally, you can render an erro
# #     #         print("Email does not exist in db",email)
# #     #         password = get_random_string(8)
# #     #         name = request.user.first_name + " " + request.user.last_name
# #     #         user=Profile.objects.create(name=name,email=email, password=password,profile_type=profile_type)
# #     #         print(user)
# #     #         request.session['is_logged_in'] = True
# #     #         return redirect("user:dashboard") 
# #     #      # Your view logic here
# #     #     except AuthCanceled as e:
# #     #         # Handle the AuthCanceled exception
# #     #         print(f"Authentication canceled by gmail: {e}")
# #     #         return redirect(reverse('user:login'))
# #     return redirect('user:dashboard')

# # def login_with_gmail(request):
    
# #     # Redirect the user to Google OAuth2 authorization URL
# #     return redirect('https://accounts.google.com/o/oauth2/auth?client_id=121742523439-s30kcv1je7lg798uen7rd4ntk1oagh39.apps.googleusercontent.com&redirect_uri=http://127.0.0.1:8000/user/complete/gmail_login/&state=PgNlIlTgE1FkGxspG8ZLTbybjrJC1H5V&response_type=code&scope=openid+email+profile')