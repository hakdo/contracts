from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .. models import Contract, Partner, Organization
from django.contrib.auth.decorators import login_required
from .. forms import ContractForm, PartnerForm, MemberConfigForm, RegisterForm, RegisterNew
from django import forms
from django.contrib.auth.models import User
import uuid

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

def new(request):
    errormsg = ''
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterNew(request.POST)
        if form.is_valid():
            username = form.cleaned_data['epost']
            password = form.cleaned_data['passord']
            confirm_password = form.cleaned_data['bekreft_passord']
            orgnr = form.cleaned_data['organisasjonsnummer']
            company_name = form.cleaned_data['firmanavn']
            # Create new organization
            org = Organization(name=company_name, orgnr=orgnr)
            org.save()
            user = User.objects.create_user(username, '', password)
            user.profile.organization = org
            user.save()
            return redirect('login')
    else:
        form = RegisterNew()
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': 'Register your account', 'errormsg': errormsg, 'submitvalue': 'Register'})