from django.shortcuts import redirect, render
from .forms import CreateUserForm, LeadForm, LoginForm, CreateRecordForm, UpdateRecordForm, UpdateLeadForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

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




@login_required
def leads_list(request):
    if request.user:
        leads = Lead.objects.all()
    else:
        leads = Lead.objects.filter(assigned_to=request.user)

    return render(request, 'webapp/leads.html', {'leads': leads})






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

    context = {'form': form}

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