from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password,check_password
from shared_model.models import Profile
# from .middleware import auth, login_checker
from shared_model.models import CreateComplaint
# def emp_profile_admin(request):
#     return render(request, 'emp_profile_admin.html')
# def view_emp_profile_admin(request):
#     return render(request, 'view_emp_profile_admin.html')


# def logout_user(request):
#     logout(request)

def navigation(request):
    return render(request, 'navigation_user.html')
#########User section############

# @auth
def dashboard(request):
    p_id=request.session.get("profile_id")
    complaints = CreateComplaint.objects.filter(profile_id=p_id)
    return render(request, 'dashboard.html', {'complaints': complaints})

# @auth
def profile(request):
    profile_id = request.session.get('profile_id')
    if profile_id is not None:
                print("Working id is", profile_id)
                profile = get_object_or_404(Profile, id=profile_id)
                return render(request, 'profile.html', {'profile': profile})
    else:
         print("Not working")
    return render(request, 'profile.html')

    
def forgot_password(request):
    return render(request, 'forgot_password.html')
# @login_checker 
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
                if Profile.objects.filter(email=email).exists() and check_password(password, user.password):
                    request.session['is_logged_in'] = True
                    request.session['email_id'] = user.email
                    request.session['profile_id'] = user.id
                    # Check if the provided password matches the hashed password
                    # Both email exists and password matches, redirect to dashboard
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
def logout_view(request):
                # Clear session data
                request.session.clear()
                # Redirect to the login page or any other desired page
                return redirect('user:login')        
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
                        user = Profile.objects.create(name=name, mobile=mobile, email=email, password=hashed_password)
                    else:
                        response_data['status'] = 'error'
                        response_data['message'] = error_msg
                        response_data['data'] = request.POST
                    

                    return render(request,'registration_user.html',response_data)
                else:
                    return render(request, 'registration_user.html')

#########Complaint section############
# @auth
def complaint(request, operation,complaint_id=None,):
    match operation:
        case 'home':
             return render(request, 'complaint_dashboard.html')
            
        case 'reply':
            # Logic for view_complaint_reply_user
            return render(request, 'complaint_reply_user.html')
        # case 'specific_complaint':
        #     return render(request, 'specific_complaint.html')  

        case 'create':
                    if request.method== 'POST' and request.session['is_logged_in'] == True:
                            # Retrieve the profile_id from the session
                            p_id = request.session.get('profile_id')
                            profile = Profile.objects.get(id=p_id)
                            # Now you can use profile_id in this function
                            # For example, print it
                            print("Profile ID:", p_id)
                            print("Profile email:", profile.name)
                            print("Profile mobile:", profile.mobile)
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
                        
                            if(len(error_msg) == 0):
                                response_data['status'] = 'success'
                                response_data['message'] = ['Complaint Registered Successfully.']
                                response_data['data'] = []
                                complaint = CreateComplaint.objects.create(profile_id=p_id, subject=subject, message=message)
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
                profile_id = request.GET.get('id')
                if profile_id is not None:
                    
                    complaints = CreateComplaint.objects.filter(profile_id=profile_id)

                    return render(request, 'complaint_list_user.html', {'complaints': complaints}) 
                else:
                    ###if id matches with the complaint created those complaints only show it to the user
                    
                    complaints = CreateComplaint.objects.all()
                    return render(request, 'complaint_list_user.html', {'complaints': complaints})       
        
    
def view_all_complaint_admin(request):
    return render(request, 'view_all_complaint_admin.html')

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password','')
        new_password = request.POST.get('new_password','')
        confirm_password = request.POST.get('confirm_password')

        profile = request.user.Profile
        
             

        error_msg =[]
        response_data = {
             'status':'',
             'message':'',
             'data':''
        }


        if not check_password(old_password, request.user.password):
            messages.error(request, 'Incorrect old password.')
            return redirect('change_password')

        # Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password')
        
        profile.user.set_password(new_password)
        profile.user.save()

        messages.success(request, 'Password successfully updated.')
        return redirect('profile')
    return  render(request,'change_password.html')

def profile_update(request):
    p_id = request.session.get('profile_id')
    print(p_id)
    return render(request,'profile.html')


#Authentication login
def oauth_gmail_login(request):
    # Redirect to Gmail authentication
    return redirect('social:begin', 'google-oauth2')


def oauth_callback(request):
    # Process the callback from the authentication provider
    return redirect('user:dashboard')