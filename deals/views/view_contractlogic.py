from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .. models import Contract, Partner, Organization
from django.contrib.auth.decorators import login_required
from .. forms import ContractForm, PartnerForm, MemberConfigForm, RegisterForm
from django import forms
from django.contrib.auth.models import User
import uuid
from django.utils.translation import gettext as _

contract_types = ['employment','sales','loi','nda','partnership','dpa','other']

# Create your views here.
@login_required()
def index(request, status='active'):
    # View to list contracts based on status. The default is active.
    errmsg = ''
    if status not in ['active', 'negotiation', 'expired', 'cancelled', 'terminated', 'all']:
        raise Http404('Invalid contract status')
    elif status == 'all':
        mycontracts = Contract.objects.filter(contract_party__owner = request.user.profile.organization)
    else:
        mycontracts = Contract.objects.filter(status=status, contract_party__owner = request.user.profile.organization)
    cfilter = request.GET.get('filter', None)
    sortby = request.GET.get('sort', None)
    if cfilter in contract_types:
        mycontracts = mycontracts.filter(contract_type = cfilter)
    elif cfilter is not None:
        mycontracts = Contract.objects.none()
        errmsg = 'No match for your filter.'
    if sortby in ['contract_party', 'contract_type', 'status', 'expires']:
        mycontracts = mycontracts.order_by(sortby)
    elif sortby is not None:
        errmsg = 'Your sort key is invalid.'
    for contract in mycontracts:
        contract.status_trans = _(contract.status)
        contract.contract_type_trans = _(contract.contract_type)
    heading = _('Contracts: ') + _(status)
    return render(request, 'deals/index.html', {'contracts': mycontracts, 'activetab': 'contracts', 'heading': heading, 'status': status, 'error': errmsg})

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
        partner.entity_type_trans = _(partner.entity_type)
    return render(request, 'deals/partners.html', {'partners': partners, 'activetab': 'partners'})

@login_required()
def partner_detail(request, pk):
    partner = get_object_or_404(Partner, pk=pk, owner = request.user.profile.organization)
    pcontracts = Contract.objects.filter(contract_party=partner)
    for contract in pcontracts:
        contract.status_trans = _(contract.status)
        contract.contract_type_trans = _(contract.contract_type)
    return render(request, 'deals/index.html', {'heading': partner.name, 'activetab': 'partners', 'contracts': pcontracts})

@login_required()
def search(request):
    # View to return search results using the index template
    query = request.GET.get('query', '') 
    partnersearch = Contract.objects.filter(contract_party__name__icontains=query)
    # Check in description field
    descriptionsearch = Contract.objects.filter(description__icontains=query)
    mycontracts = (partnersearch | descriptionsearch).filter(contract_party__owner = request.user.profile.organization).distinct()
    heading = _("Search results for query ")
    status = 'all'
    if len(mycontracts) < 1:
        errmsg = _("No results found for query.")
    else:
        errmsg = ''
    for contract in mycontracts:
        contract.status_trans = _(contract.status)
        contract.contract_type_trans = _(contract.contract_type)
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
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': _('New Contract'), 'activetab': 'contracts', 'submitvalue': _('Create contract record')})

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
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': _('Editing Contract ') + str(myinstance.contract_number), 'activetab': 'contracts', 'submitvalue': _('Save changes')})

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
    return render(request, 'deals/new_contract.html', {'form': form, 'heading': _('New Partner'), 'activetab': 'partners', 'submitvalue': _('Create contract partner')})


