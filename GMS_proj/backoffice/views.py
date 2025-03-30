from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from textblob import TextBlob
# from transformers import pipeline
# from langdetect import detect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password,check_password
from shared_model.models import Profile
from backoffice.middleware import auth_b, login_checker_b
from shared_model.models import Profile
from shared_model.models import ComplaintMessage
from shared_model.models import CreateComplaint
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from django.utils import timezone 
from datetime import datetime
from pytz import timezone as pytz_timezone
from django.utils.timezone import activate, localtime, now as django_now
# from django.contrib.auth.decorators import login_required
@auth_b
def profile(request):
    profile_id = request.session.get('profile_id')
    if profile_id is not None:
                print("Working id is", profile_id)
                profile = get_object_or_404(Profile, id=profile_id)
                return render(request, 'profile.html', {'profile': profile})
    else:
         print("Not working")
@login_checker_b
def oauth_gmail_login(request):
    # Redirect to Gmail authentication
    return redirect('social:begin', 'google-oauth2')

@login_checker_b
def oauth_callback(request):
    print("hello")
    print(request.method)
    return redirect('backoffice:dashboard')


# def get_user_email(request):
#     # Check if the user is authenticated
#     if request.user.is_authenticated:
#         # Retrieve the user's social authentication details
#         try:
#             user_social_auth = request.user.social_auth.get(provider='google-oauth2')
#             # Access the email address from the user's social authentication details
#             user_email = user_social_auth.extra_data.get('email')
#             if user_email:
#                 return user_email
#             else:
#                 # Handle the case where email is not available in social authentication details
#                 return None
#         except UserSocialAuth.DoesNotExist:
#             # Handle the case where the user is not authenticated via Google OAuth2
#             return None
#     else:
#         # Handle the case where the user is not authenticated
#         return None

# def logout_view(request):
#     # Clear session data
#     request.session.clear()
#     # Redirect to the login page or any other desired page
#     return redirect('login') 
@auth_b
def navigation_admin(request):
    return render(request, 'backoffice/navigation_admin.html')


@auth_b
def dashboard(request):
    User = Profile.objects.all()
    complaint = CreateComplaint.objects.all()
    create_complaint = CreateComplaint.objects.all()
    # print(get_user_email(request))
    return render(request, 'backoffice/dashboard.html', {'user': User, 'complaints': complaint,'create_complaint':create_complaint})
@auth_b
def create_complaint(request):
    create_complaint = CreateComplaint.objects.all()
    return render(request, 'backoffice/create_complaint.html',{'create_complaint':create_complaint})

     
def employee_add(request):
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
                response_data['message'] = ['Employee Registered Successfully.']
                response_data['data'] = []
                hashed_password=make_password(password)
                # If the email doesn't exist, create a new Profile object
                profile_type_id=1
                user = Profile.objects.create(name=name, mobile=mobile, email=email, password=hashed_password,profile_type_id=profile_type_id)
            else:
                response_data['status'] = 'error'
                response_data['message'] = error_msg
                response_data['data'] = request.POST
            

            return render(request,'backoffice/employee_add.html',response_data)
        else:
            return render(request, 'backoffice/employee_add.html')

@auth_b
def profile(request):
    return render(request, 'backoffice/profile.html')
@login_checker_b   
def forgot_password(request):
    return render(request, 'backoffice/forgot_password.html')

@login_checker_b
def login_page(request ,response_data=None):
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
                    if Profile.objects.filter(email=email).exists() and check_password(password, user.password) and user.profile_type_id == 1:
                        request.session['is_logged_in'] = True
                        request.session['email_id'] = user.email
                        request.session['profile_id'] = user.id
                        request.session['name'] = user.name
                        request.session['profile_type_id'] = user.profile_type_id
                        # Check if the provided password matches the hashed password
                        # Both email exists and password matches, redirect to dashboard
                        return redirect("backoffice:dashboard") 
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
            return render(request, 'backoffice/login.html', response_data)
@auth_b
def logout_view(request):
            # Clear session data
            request.session.clear()
            # Redirect to the login page or any other desired page
            return render(request,'backoffice/login.html') 
@login_checker_b
def admin_registration(request):
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
                response_data['message'] = ['Employee Registered Successfully.']
                response_data['data'] = []
                hashed_password=make_password(password)
                profile_type="Admin"
                profile_type_id=1
                # If the email doesn't exist, create a new Profile object
                user = Profile.objects.create(name=name, mobile=mobile, email=email, password=hashed_password,profile_type=profile_type,profile_type_id=profile_type_id)
            else:
                response_data['status'] = 'error'
                response_data['message'] = error_msg
                response_data['data'] = request.POST
            

            return render(request,'backoffice/registration.html',response_data)
        else:
            return render(request, 'backoffice/registration.html')

@auth_b
def complaint(request, operation):
     match operation:
        case 'delete':
               complaint_id = request.GET.get("id")
               
               print("Complaint ID LATEST",complaint_id)
               complaint = get_object_or_404(CreateComplaint,id =complaint_id)
               complaint.delete()
               operation = 'view'  # Set the operation value

               # Generate the URL using reverse and pass the operation as an argument
               url = reverse('backoffice:complaints', kwargs={'operation': operation})

               # Redirect to the generated URL
               return redirect(url)
            
        case 'message':
            complaint_id=request.GET.get("id")
            # complaint_messages = get_object_or_404(ComplaintMessage,id =complaint_id)
                
           
            
            # request.session['is_logged_in'] = True
            profile_id = request.session.get('profile_id')
            # profile_type_id=request.session.get('profile_type_id')
            print("COMPLAINT ID REPLY",complaint_id)
            if request.method=='POST':
                 s_name=request.session['name']
                 message= request.POST.get('message')
                 # Get the timezone object for Asia/Kolkata
                 kolkata_timezone = pytz_timezone('Asia/Kolkata')

                # Activate Asia/Kolkata timezone
                 activate(kolkata_timezone)

                # Get the current time in Asia/Kolkata timezone
                 current_time_in_raipur = timezone.localtime(timezone.now())
                 print(datetime)
                 reply = ComplaintMessage.objects.create( profile_id=profile_id,message=message, created_at=current_time_in_raipur,complaint_id=complaint_id)
                #  reply = Reply.objects.all()
                #  request.session['id']=reply.id
                #showing the chats
                 chat = ComplaintMessage.objects.filter(complaint_id=complaint_id)
            else:
    
                 chat = ComplaintMessage.objects.filter(complaint_id=complaint_id)


            return render(request, 'backoffice/reply_admin.html',{'complaintid':complaint_id,'chats': chat})
          
        case 'view':
            print("case view")
            
        
            complaint_id=request.GET.get("id")
           
            print("working id is",complaint_id)
            if complaint_id is not None:
                print("working id is",complaint_id)
                complaints = get_object_or_404(CreateComplaint,id =complaint_id)
                
                profile_id = complaints.profile_id
                print("profile_id",profile_id)
                
                # profile_id=CreateComplaint.objects.get(profile_id=profile_id)
                # p_id=int(complaints.profile_id)
                
                
                profile = Profile.objects.get(id=profile_id)
                print("PROFILE DATA SUCCESS",profile)
                print(type(profile))
                return render(request, 'backoffice/complaint_view.html',{'complaints': complaints,'profile':profile})
            
                
            else:
                complaints = CreateComplaint.objects.all()
                # Perform sentiment analysis using TextBlob for each complaint
                for complaint in complaints:
                    text = complaint.subject+complaint.message
                    print("text",text)
                    blob = TextBlob(text)
                    sentiment_score = blob.sentiment.polarity
                    complaint.sentiment = 'Positive' if sentiment_score > 0 else 'Negative' if sentiment_score < 0 else 'Neutral'
                    # Re-fetch the complaints ordered by created_at to ensure order after update
                    print(complaint_id)
                return render(request, 'backoffice/complaint_list.html', {'complaints': complaints})
        case 'employee_list':
                employees = Profile.objects.all()
                return render(request, 'backoffice/employee_list.html', {'employees': employees})
        case 'employee_detail':
                employee_id =  request.GET.get('id')
                employees = get_object_or_404(Profile,id =employee_id)
                return render(request, 'backoffice/employee_detail.html',{'employees': employees})
        case 'update':
            complaint_id=request.POST.get('complain_id')
            print("COMPLAINT ID IS",complaint_id)
            if request.method == 'POST':
                            current_handler = request.POST.get('current_handler','')
                            error_msg = []

                            response_data = {
                                'status':'',
                                'message':[],
                                'data':''
                            }
                            if current_handler == '':
                                error_msg.append('Field Current Handler cannot be empty.')
                            
                            # if complaint_id is not None:
                            #     # Fetch the existing profile if it exists
                            #     try:
                            #         complaints = CreateComplaint.objects.get(id=complaint_id)
                            #         print("COMPLAINT OBJECT",complaint)
                            #     except CreateComplaint.DoesNotExist:
                            #         complaint = None
                            print(error_msg)
                            if(len(error_msg) == 0):
                                complaints = CreateComplaint.objects.get(id=complaint_id)
                                 # Get the timezone object for Asia/Kolkata
                                kolkata1_timezone = pytz_timezone('Asia/Kolkata')

                                # Activate Asia/Kolkata timezone
                                activate(kolkata1_timezone)
                                current_time_in_india = timezone.localtime(timezone.now())
                                complaints.current_handler = current_handler
                                complaints.updated_at = current_time_in_india
                                complaints.save()     
                                
                                response_data['status'] = 'success'
                                response_data['message'] = ['Current Handler Updated Successfully.']
                                # Construct response data with updated name value
                                response_data = {
                                    'status': 'success',
                                    'message': ['Current Handler Updated Successfully.'],
                                    'data': {
                                        'current_handler': current_handler,  # Pass the updated name explicitly
                                    }
                                    
                                }
                            else:
                                # Construct response data with error message and original data
                                response_data = {
                                    'status': 'error',
                                    'message': error_msg,
                                    'data': {
                                        'current_handler': complaints.current_handler,
                                    }
                                }
                            return render(request, 'backoffice/complaint_view.html',{**response_data,'complaints': complaints})
            else:
                # chg_profile = get_object_or_404(Profile, id=p_id)
                # return render(request, 'profile.html', {'chg_profile': chg_profile})
                print("POST not done")
                pass
            
    
            
    

@auth_b
def delete_employee(request):
    
    
    # Get the employee object or return 404 if not found
    employee_id = request.GET.get("id")
    emp_profile = get_object_or_404(Profile,id =employee_id)
    emp_profile.delete()
    print("employee id is",employee_id)
    
    operation = 'employee_list'  # Set the operation value

    # Generate the URL using reverse and pass the operation as an argument
    url = reverse('backoffice:complaints', kwargs={'operation': operation})

    # Redirect to the generated URL
    return redirect(url)
    # employee.delete
    # # Delete the employee
    # if(employee.delete()):
    
    # # Return a JSON response indicating success
    #     response_data = {
    #         'status':'success',
    #         'message':'User deleted successfully',
    #         'data':[]

    #     }
    # else:
    #      response_data = {
    #         'status':'error',
    #         'message':'Unable to delete user.',
    #         'data':[]

    #     }
    # return JsonResponse(response_data)
@auth_b
def profile(request):
    profile_id = request.session.get('profile_id')
    if profile_id is not None:
                print("Working id is", profile_id)
                profile = get_object_or_404(Profile, id=profile_id)
                return render(request, 'backoffice/profile.html', {'profile': profile})
    else:
         print("Not working")
    return render(request, 'backoffice/profile.html')
@auth_b
def update(request):
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
                            return render(request, 'backoffice/profile.html', response_data)
            else:
                # chg_profile = get_object_or_404(Profile, id=p_id)
                # return render(request, 'profile.html', {'chg_profile': chg_profile})
                print("POST not done")
                pass
            
    
            
    