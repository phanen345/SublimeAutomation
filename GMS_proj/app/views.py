from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def index(request):
    return render(request, 'index.html')
def view_all_complaint_admin(request):
    return render(request, 'view_all_complaint_admin.html')
def login(request):
    return render(request, 'login.html')
def view_complaint_reply_user(request):
    return render(request, 'view_complaint_reply_user.html')
def emp_profile_admin(request):
    return render(request, 'emp_profile_admin.html')
def view_emp_profile_admin(request):
    return render(request, 'view_emp_profile_admin.html')
def specific_complaint(request):
    return render(request, 'specific_complaint.html')
def complaint_user(request):
    return render(request, 'complaint_user.html')
def profile(request):
    return render(request, 'profile.html')

def home(request):
    return render(request, 'home.html')


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


        if(len(error_msg) == 0):
            response_data['status'] = 'success'
            response_data['message'] = ['User Registered Successfully.']
            response_data['data'] = []
        else:
            response_data['status'] = 'error'
            response_data['message'] = error_msg
            response_data['data'] = request.POST

        return render(request,'user_registration.html',response_data)



        
    else:
      
       
        return render(request, 'user_registration.html')
        




 