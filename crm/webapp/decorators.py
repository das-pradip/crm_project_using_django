# from django.shortcuts import redirect
# from django.contrib import messages

# def role_required(allowed_roles=[]):
#     def decorator(view_func):
        
#         def wrapper(request, *args, **kwargs):

#             # Safety check
#             if not hasattr(request.user, 'userprofile'):
#                 messages.error(request, "Profile not found")
#                 return redirect('dashboard')

#             if request.user.userprofile.role not in allowed_roles:
#                 messages.error(request, "Access denied")
#                 return redirect('dashboard')

#             return view_func(request, *args, **kwargs)

#         return wrapper
#     return decorator



from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            user = request.user

            # Safety: profile may not exist
            if not hasattr(user, 'profile'):
                messages.error(request, "User profile not found")
                return redirect('dashboard')

            role = user.profile.role

            # Allow superuser ALWAYS
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            if role not in allowed_roles:
                messages.error(request, "Access denied")
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.profile.role != 'admin':
            messages.error(request, "Admin access only")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper