from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from . models import Contract, Partner, Organization
from django.contrib.auth.decorators import login_required
from .forms import ContractForm, PartnerForm, MemberConfigForm, RegisterForm
from django import forms
from django.contrib.auth.models import User
import uuid

# Create your views here.
@login_required()
def index(request, status='active'):
    # View to list contracts based on status. The default is active.
    if status not in ['active', 'negotiation', 'expired', 'cancelled', 'terminated', 'all']:
        raise Http404('Invalid contract status')
    elif status == 'all':
        mycontracts = Contract.objects.filter(contract_party__owner = request.user.profile.organization)
    else:
        mycontracts = Contract.objects.filter(status=status, contract_party__owner = request.user.profile.organization)
    heading = 'Contracts: ' + status
    return render(request, 'deals/index.html', {'contracts': mycontracts, 'activetab': 'contracts', 'heading': heading, 'status': status})

@login_required()
def contract_detail(request, pk):
    # View to see the details of a specific contract
    mycontract = get_object_or_404(Contract, pk=pk, contract_party__owner=request.user.profile.organization)
    return render(request, 'deals/contract_details.html', {'contract': mycontract, 'activetab': 'contracts'})

@login_required()
def partners(request):
    # Get a list of all contract partners
    partners = Partner.objects.filter(owner = request.user.profile.organization)
    # Iterate over partners and add to each item the number of contracts
    for partner in partners:
        pcons = Contract.objects.filter(contract_party=partner)
        partner.numcon = len(pcons)
    return render(request, 'deals/partners.html', {'partners': partners, 'activetab': 'partners'})

@login_required()
def partner_detail(request, pk):
    partner = get_object_or_404(Partner, pk=pk, owner = request.user.profile.organization)
    pcontracts = Contract.objects.filter(contract_party=partner)
    return render(request, 'deals/index.html', {'heading': partner.name, 'activetab': 'partners', 'contracts': pcontracts})

@login_required()
def search(request):
    # View to return search results using the index template
    query = request.GET.get('query', '') 
    partnersearch = Contract.objects.filter(contract_party__name__contains=query)
    # Check in description field
    descriptionsearch = Contract.objects.filter(description__contains=query)
    mycontracts = (partnersearch | descriptionsearch).filter(contract_party__owner = request.user.profile.organization).distinct()
    heading = "Search results for query "
    status = 'all'
    if len(mycontracts) < 1:
        errmsg = "No results found for query."
    else:
        errmsg = ''
    return render(request, 'deals/index.html', {'contracts': mycontracts, 'activetab': 'contracts', 'heading': heading, 'status': status, 'error': errmsg, 'queryterm': query})

@login_required()
def new_contract(request):
    partners = Partner.objects.filter(owner = request.user.profile.organization)
    # Change the dropdown possibilities to your own orgs. 
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save()
            return redirect('contract_detail', pk=contract.pk)
    else:
        form = ContractForm()
        form.fields['contract_party'].queryset = partners
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': 'New Contract', 'activetab': 'contracts', 'submitvalue': 'Create contract record'})

@login_required()
def edit_contract(request, pk):
    partners = Partner.objects.filter(owner = request.user.profile.organization)
    myinstance = get_object_or_404(Contract, pk=pk, contract_party__in = partners)
    if request.method == 'POST':
        contract = ContractForm(request.POST, instance = myinstance)
        contract.save()
        return redirect('contract_detail', pk=pk)
    else:
        form = ContractForm(instance=myinstance)
        form.fields['contract_party'].queryset = partners
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': 'Editing Contract ' + str(myinstance.contract_number), 'activetab': 'contracts', 'submitvalue': 'Save changes'})

@login_required()
def new_partner(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save(commit=False)
            partner.owner = request.user.profile.organization
            partner.save()
            return redirect('partners')
    else:
        form = PartnerForm()
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': 'New Partner', 'activetab': 'partners', 'submitvalue': 'Create contract partner'})

@login_required()
def team(request):
    if not request.user.profile.is_admin:
        return redirect('index')
    else:
        # Is a team admin, can go to the page
        # Get all team members so far
        members = User.objects.filter(profile__organization=request.user.profile.organization)
        if request.method == "POST":
            form = MemberConfigForm(request.POST)
            accepting_members = request.user.profile.organization.accepting_members
            if form.is_valid():
                # First see if there is a change in accepting_members:
                myorg = request.user.profile.organization
                if form.cleaned_data['allow_new_members'] != accepting_members:
                    # Update accepting_members setting
                    myorg.accepting_members = form.cleaned_data['allow_new_members']
                    myorg.save()
                if form.cleaned_data['update_organization_secret']:
                    # Generate a new uuid4 and save...
                    myorg.orgsecret = uuid.uuid4()
                    myorg.save()
        form = MemberConfigForm(initial={'allow_new_members': request.user.profile.organization.accepting_members})
        return render(request, 'deals/team.html', {'members': members, 'configform': form})

def register(request):
    # Registration of a user with an invite code. Fields for registration would 
    # include email, password, password-confirm, secretcode
    errormsg = ''
    # if the person is already registered and logged in, redirect to the index page
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            secret_code = form.cleaned_data['secret_code']
            myorg = Organization.objects.get(orgsecret = secret_code)
            user = User.objects.create_user(username, '', password)
            user.profile.organization = myorg
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': 'Register your account', 'errormsg': errormsg, 'submitvalue': 'Register'})
