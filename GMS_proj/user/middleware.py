# # from functools import wraps
# # from django.shortcuts import redirect

# # def wrapper(view_func):
# #     @login_auth(view_func)
# #     def decorated_view(request, *args, **kwargs):
# #         if not request.user.is_authenticated:
# #             return redirect("login")  # Redirect to the login page if the user is not authenticated
# #         else:
# #             return view_func(request, *args, **kwargs)
# #     return decorated_view

# from functools import wraps
# from django.shortcuts import redirect

# def unauthenticated_user(view_func):
#     @login_auth(view_func)
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect("index")  # Redirect to the index page if the user is already authenticated
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper

from django.shortcuts import render,redirect



def auth(view_function):
    def wrapped_view(request, *args, **kwargs):
        if 'is_logged_in' not in request.session:
              request.session['is_logged_in'] = False
              return redirect('user:login')
        elif 'is_logged_in' in request.session:
            if request.session['is_logged_in'] == False:   
                return redirect('user:login')
            
            
        # if 'profile_type_id' in request.session:
        #     if request.session['profile_type_id'] == 1 : 
        #         print("condition checked TRUE .................")
        #         return redirect('backoffice:login')
        # else :
        #     return redirect('user:login')
        
        return view_function(request, *args, **kwargs)
    return wrapped_view

def login_checker(view_function):
    def wrapped_view(request, *args, **kwargs):
        print('case 1')
        if 'is_logged_in' in request.session:
            if request.session['is_logged_in'] == True :
                return redirect('user:dashboard')
            
      
        return view_function(request, *args, **kwargs)
    return wrapped_view

