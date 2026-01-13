from django.shortcuts import redirect, render
from .forms import CreateUserForm, LeadForm, LoginForm, CreateRecordForm, UpdateRecordForm, UpdateLeadForm


from .decorators import admin_required
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.db.models import Count

from .models import Lead, Record

from django.contrib import messages



# Home page

def home(request):
    # return HttpResponse("Welcome to the CRM Home Page")
    # First we use the HttpResponse to return a simple text response.Now we'll render a template.
    return render(request, 'webapp/index.html')


#  Register a user page

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Account created successfully! Please login.')

            return redirect("my-login")

    context = {'form': form}

    return render(request, 'webapp/register.html', context=context)

#  Login a user page

def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')


    context = {'form': form}    

    return render(request, 'webapp/my-login.html', context=context)

#  Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()
    

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)


# Create a record
@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        
        if form.is_valid():
            form.save()

            messages.success(request, 'Your record has been created successfully!')


            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'webapp/create-record.html', context=context)


# Update a record
@login_required(login_url='my-login')
def update_record(  request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()

            messages.success(request, 'Your record has been updated successfully!')


            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'webapp/update-record.html', context=context)





# Read / View a singular record

@login_required(login_url='my-login')
def singular_record(  request, pk):

     all_records = Record.objects.get(id=pk)

     context = {'record': all_records}

     return render(request, 'webapp/view-record.html', context=context)


# Delete a record
@login_required(login_url='my-login')
def delete_record(  request, pk):

    record = Record.objects.get(id=pk)
    record.delete()

    messages.success(request, 'The record has been deleted successfully!')

    return redirect("dashboard")



# user logout

def user_logout(request):
    auth.logout(request)
    messages.success(request, 'Logout success!')
    return redirect("my-login")


@login_required
def create_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            return redirect('leads')
    else:
        form = LeadForm()

    return render(request, 'webapp/create-lead.html', {'form': form})




# @login_required
# def leads_list(request):
#     if request.user:
#         leads = Lead.objects.all()
#     else:
#         leads = Lead.objects.filter(assigned_to=request.user)

#     return render(request, 'webapp/leads.html', {'leads': leads})



# @login_required(login_url='my-login')
# def leads_list(request):

#     leads = Lead.objects.all()

#     if request.method == 'POST':
#         lead_id = request.POST.get('lead_id')
#         status = request.POST.get('status')

#         lead = Lead.objects.get(id=lead_id)
#         lead.status = status
#         lead.save()

#         messages.success(request, 'Lead status updated successfully!')
#         return redirect('leads')

#     context = {
#         'leads': leads,
#         'status_choices': Lead.STATUS_CHOICES
#     }
#     return render(request, 'webapp/leads.html', context)



@login_required(login_url='my-login')
def leads_list(request):

    user_role = request.user.profile.role

    # VIEW PERMISSION
    if user_role == 'sales':
        leads = Lead.objects.filter(assigned_to=request.user)
    else:
        leads = Lead.objects.all()

    # UPDATE PERMISSION
    if request.method == 'POST':

        if user_role not in ['admin', 'manager', 'sales']:
            messages.error(request, "You are not allowed to update lead status")
            return redirect('leads')

        lead_id = request.POST.get('lead_id')
        status = request.POST.get('status')

        lead = Lead.objects.get(id=lead_id)

        # Optional: Sales can update ONLY their assigned leads
        if user_role == 'sales' and lead.assigned_to != request.user:
            messages.error(request, "You cannot update this lead")
            return redirect('leads')

        # Prevent update after conversion
        if lead.is_converted:
            messages.warning(request, "Converted leads cannot be updated")
            return redirect('leads')

        lead.status = status
        lead.save()

        messages.success(request, "Lead status updated successfully")
        return redirect('leads')

    context = {
        'leads': leads,
        'status_choices': Lead.STATUS_CHOICES
    }
    return render(request, 'webapp/leads.html', context)


@login_required(login_url='my-login')
def update_lead(  request, pk):

    lead = Lead.objects.get(id=pk)

    form = UpdateLeadForm(instance=lead)

    if request.method == 'POST':
        form = UpdateLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()

            messages.success(request, 'Your lead has been updated successfully!')


            return redirect('lead', pk=pk)

    context = {
        'form': form,
        'lead': lead,
        'status_choices': Lead.STATUS_CHOICES

    }

    return render(request, 'webapp/update-lead.html', context=context)



# Read / View a singular lead

@login_required(login_url='my-login')
def singular_lead(  request, pk):

     lead = Lead.objects.get(id=pk)

     context = {'lead': lead}

     return render(request, 'webapp/view-lead.html', context=context)


# Delete a lead
@login_required(login_url='my-login')
def delete_lead(  request, pk):

    lead = Lead.objects.get(id=pk)
    lead.delete()

    messages.success(request, 'The lead has been deleted successfully!')

    return redirect("leads")


@login_required(login_url='my-login')
def convert_lead(request, pk):

    lead = Lead.objects.get(id=pk)

    # Safety check
    if lead.status != 'qualified':
        messages.error(request, 'Only qualified leads can be converted!')
        return redirect('lead', pk=pk)
    
    if lead.is_converted:
        messages.info(request, 'Lead already converted')
        return redirect('lead')

    
    # DUPLICATE CUSTOMER CHECK 
    if Record.objects.filter(email=lead.email).exists():

        lead.is_converted = True
        lead.save()

        messages.error(request, 'Customer already exists!')
        return redirect('lead', pk=pk)

    # Create Record (Customer)
    Record.objects.create(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone=lead.phone,
        address='N/A',
        city='N/A',
        state='N/A',
        country='N/A',
    )

    # Update lead status
    # lead.status = 'converted'
    lead.status = 'qualified'
    lead.is_converted = True
    lead.save()

    messages.success(request, 'Lead converted to customer successfully!')
    return redirect('leads')



# Kanban pipeline view
@login_required(login_url='my-login')
def lead_pipeline(request):
    new = list(Lead.objects.filter(status='new'))
    contacted = list(Lead.objects.filter(status='contacted'))
    qualified = list(Lead.objects.filter(status='qualified'))
    converted = list(Lead.objects.filter(status='converted'))
    lost = list(Lead.objects.filter(status='lost'))

    max_len = max(
        [len(new), len(contacted), len(qualified), len(converted), len(lost)],
        default=0
    )

    rows = []
    for i in range(max_len):
        rows.append({
            'new': new[i] if i < len(new) else None,
            'contacted': contacted[i] if i < len(contacted) else None,
            'qualified': qualified[i] if i < len(qualified) else None,
            'converted': converted[i] if i < len(converted) else None,
            'lost': lost[i] if i < len(lost) else None,
        })

    context = {
        'rows': rows
    }
    return render(request, 'webapp/kanban-lead-view.html', context)


@login_required(login_url='my-login')
@role_required(['admin', 'manager'])
def lead_status_analytics(request):


    # user_role = request.user.profile.role
    

    total_leads = Lead.objects.count()
    converted_leads = Lead.objects.filter(is_converted=True).count()
    
    conversion_rate = (
       round((converted_leads / total_leads) * 100, 2)
        if total_leads > 0 else 0
    )

    status_counts = (
        Lead.objects
        .values('status')
        .annotate(count=Count('id'))
    )

    STATUS_LABELS = dict(Lead.STATUS_CHOICES)

    labels = []
    data = []


    analytics = {item['status']: item['count'] for item in    status_counts}
    

    for item in status_counts:
        labels.append(STATUS_LABELS.get(item['status']))
        data.append(item['count'])

    context = {
        'labels': labels,
        'data': data,

        'analytics': analytics,
        'conversion_rate': conversion_rate
    }

    return render(request, 'webapp/lead-analytics.html', context)




# @login_required(login_url='my-login')
# @admin_required
# def manage_user_roles(request):

#     users = User.objects.select_related('profile')

#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         role = request.POST.get('role')

#         if str(request.user.id) == user_id:
#             messages.error(request, "You cannot change your own role.")
#             return redirect('manage-roles')

#         user = User.objects.get(id=user_id)
#         user.profile.role = role
#         user.profile.save()

#         messages.success(request, f"Role updated for {user.username}")
#         return redirect('manage-roles')

#     context = {
#         'users': users,
#         'roles': ['admin', 'manager', 'sales']
#     }

#     return render(request, 'webapp/manage-roles.html', context)

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import admin_required

@login_required(login_url='my-login')
@admin_required
def manage_user_roles(request):

    users = User.objects.select_related('profile')

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        user = User.objects.get(id=user_id)

        #  PREVENT SELF ACTION
        if user == request.user:
            messages.error(request, "You cannot modify or delete yourself")
            return redirect('manage-roles')

        #  UPDATE ROLE
        if action == 'update':
            role = request.POST.get('role')

            # Prevent removing last admin
            if user.profile.role == 'admin' and role != 'admin':
                admin_count = User.objects.filter(profile__role='admin').count()
                if admin_count <= 1:
                    messages.error(request, "At least one admin is required")
                    return redirect('manage-roles')

            user.profile.role = role
            user.profile.save()
            messages.success(request, f"Role updated for {user.username}")

        #  DELETE USER
        elif action == 'delete':

            # Prevent deleting superuser
            if user.is_superuser:
                messages.error(request, "Superuser cannot be deleted")
                return redirect('manage-roles')

            # Prevent deleting last admin
            if user.profile.role == 'admin':
                admin_count = User.objects.filter(profile__role='admin').count()
                if admin_count <= 1:
                    messages.error(request, "Cannot delete the last admin")
                    return redirect('manage-roles')

            user.delete()
            messages.success(request, "User deleted successfully")

        return redirect('manage-roles')

    context = {
        'users': users,
        'roles': ['admin', 'manager', 'sales']
    }

    return render(request, 'webapp/manage-roles.html', context)


# Show user profile

@login_required
def profile_view(request):
    profile = request.user.profile

    # if request.method == 'POST':
    #     profile.profile_image = request.FILES.get('profile_image')
    #     profile.save()
    #     messages.success(request, "Profile updated successfully")
    #     return redirect('profile')

    if request.method == "POST":
        if request.FILES.get('profile_image'):   #  CHECK FILE EXISTS
            profile.profile_image = request.FILES['profile_image']
            profile.save()
            messages.success(request, "Profile image updated successfully!")
        else:
            messages.warning(request, "Please select an image before updating.")

        return redirect('profile')

    return render(request, 'webapp/profile.html', {'profile': profile})
