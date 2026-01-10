from django.shortcuts import redirect, render
from .forms import CreateUserForm, LeadForm, LoginForm, CreateRecordForm, UpdateRecordForm, UpdateLeadForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
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



@login_required(login_url='my-login')
def leads_list(request):

    leads = Lead.objects.all()

    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        status = request.POST.get('status')

        lead = Lead.objects.get(id=lead_id)
        lead.status = status
        lead.save()

        messages.success(request, 'Lead status updated successfully!')
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
    lead.status = 'converted'
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
def lead_status_analytics(request):

    status_counts = (
        Lead.objects
        .values('status')
        .annotate(count=Count('id'))
    )

    # Convert queryset → dictionary
    analytics = {item['status']: item['count'] for item in status_counts}

    context = {
        'analytics': analytics,
    }

    return render(request, 'webapp/lead-analytics.html', context)
