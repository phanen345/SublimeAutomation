from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password,check_password
from shared_model.models import Profile
from .middleware import auth, login_checker
from shared_model.models import CreateComplaint
 



# def emp_profile_admin(request):
#     return render(request, 'emp_profile_admin.html')
# def view_emp_profile_admin(request):
#     return render(request, 'view_emp_profile_admin.html')


# def logout_user(request):
#     logout(request)

def navigation(request):
    return render(request, 'navigation.html')
#########User section############
def user(request, operation):
    match operation:
        case 'dashboard_user':
            # @auth
            def dashboard_user(request):
                User = Profile.objects.all()
                return render(request, 'dashboard.html', {'users': User})

        case 'profile':
            @auth
            def profile(request):
                return render(request, 'profile.html')
            # def complaint_list(request):
            #     return render(request, 'complaint_list.html')
            # def home(request):
                
        case 'forgot_password':  
            def forgot_password(request):
                return render(request, 'forgot_password.html')
        case 'login':
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
        case 'logout_view':
            def logout_view(request):
                            # Clear session data
                            request.session.clear()
                            # Redirect to the login page or any other desired page
                            return redirect('user:user', operation='login')        
        case 'user_registration':
            def user_registration(request):
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
                                

                                return render(request,'user_registration.html',response_data)
                            else:
                                return render(request, 'user_registration.html')
    
#########Complaint section############
def complaint(request, operation):
    match operation:
        case 'complaint_reply_user':
            # Logic for view_complaint_reply_user
            return render(request, 'complaint_reply_user.html')
        # case 'specific_complaint':
        #     return render(request, 'specific_complaint.html')  

        case 'complaint_user':
                    if request.method== 'POST' and request.session['is_logged_in'] == True:
                            # Retrieve the profile_id from the session
                            p_id = request.session.get('profile_id')
                            profile = Profile.objects.get(id=p_id)
                            # Now you can use profile_id in this function
                            # For example, print it
                            print("Profile ID:", p_id)
                            print("Profile email:", profile.name)
                            print("Profile mobile:", profile.mobile)
                            
                            data_to_send={
                                "p_id":p_id,
                                "name":profile.name,
                                "mobile":profile.mobile,
                            }
                            
                            subject=request.POST.get("subject","")
                            # current_handler=request.POST.get("current_handler","")
                            message=request.POST.get("message","")
                            # created_at=request.POST.get("created_at","")
                            # updated_at=request.POST.get("updated_at","")
                            
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
                                return render(request, 'complaint_list.html', {'complaints': [complaint], 'response_data': response_data})

                            else:
                                response_data['status'] = 'error'
                                response_data['message'] = error_msg
                                response_data['data'] = request.POST
                        

                            return render(request,'complaint_user.html',response_data)
                    else:
                        return render(request, 'complaint_user.html')
                
        
        # def view_complaint_reply_user(request):
        #     return render(request, 'view_complaint_reply_user.html')    

            
        # def profile(request,operation='view'):
        #     match operation :
        #         case 'view':
        #             profile_id = request.session['profile_id']
        #              # profile_data = model
        #             return render(request, 'profile.html',{'profile':'profile_data'})
        #         case 'edit':
        #             # post_data = POST
        #             #  if true 
        #             #   response_data['status'] = 'success'
        #             # response_data['message'] = 'Profile Updated Successfully'
        #             # response_data['data'] = request.POST
        #             response_data = {}
                    
        #             return render(request, 'profile.html',response_data
        #         case 'chnage-password':
        #            response = this.change_profile_password(request)
                    
                    

        #     }
        # def complaint(request,operation='view',id=None):
        #     match operation :
        #         case 'view':
        #             if id != None:
        #                 #return specific complaint data to view_complaint_datails.html
        #                 return render(request, 'view_complaint_datails.html',{'complaint':'complaint_Data'})
                    
        #             else:
        #                 all_ = request.session['profile_id']
        #                 # profile_data = model
        #                 return render(request, 'complaint.html',{'complaints':'complaint_Data'})
        #         case operation == 'view':
        #             # post_data = POST
        #             #  if true 
        #             #   response_data['status'] = 'success'
        #             # response_data['message'] = 'Profile Updated Successfully'
        #             # response_data['data'] = request.POST
        #             response_data = {}
                    
        #             return render(request, 'profile.html',response_data
        #         case 'chnage-password':
        #            response = hange_profile_password(request)
                    
                    

        #     }
            
            
        # def change_profile_password(data):
        #     pass
        
        #########THINGS to LOOK FOR############
    
def view_all_complaint_admin(request):
    return render(request, 'view_all_complaint_admin.html')
