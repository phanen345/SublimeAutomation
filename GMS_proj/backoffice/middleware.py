from django.shortcuts import render,redirect



def auth_b(view_function):
    def wrapped_view(request, *args, **kwargs):
        print("case 2 auth_b")
        print("session:",request.session.items())
        if 'is_logged_in' not in request.session:
              request.session['is_logged_in'] = False
              return redirect('backoffice:login')
        elif 'is_logged_in' in request.session:
            if request.session['is_logged_in'] == False:   
                return redirect('backoffice:login')
             
             
             
             # admin  Admin ADMIN 
                
            
        

        return view_function(request, *args, **kwargs)
    return wrapped_view

def login_checker_b(view_function):
    def wrapped_view(request, *args, **kwargs):
        print('case 1')
        if 'is_logged_in' in request.session:
            if request.session['is_logged_in'] == True :
                return redirect('backoffice:dashboard')
            
      
        return view_function(request, *args, **kwargs)
    return wrapped_view
