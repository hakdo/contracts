from django.test import TestCase
from .models import Partner
from .models import Contract

# Create your tests here.

"""
* Test that views return as expected
* Test: view context includes correct activetab
"""

class Test_View_Index(TestCase):
    def test_not_in_list(self):
        response = self.client.get('/contracts/notastatus/')
        self.assertEqual(response.status_code, 404)
    
    def test_in_list(self):
        response = self.client.get('/contracts/negotiation/')
        self.assertEqual(response.status_code, 200)
    
    def test_context_sets_heading(self):
        response = self.client.get('/contracts/active/')
        self.assertTrue(response.context['heading'])

    def test_all_returns_all(self):
        response = self.client.get('/contracts/all/')
        view_qs = response.context[0]['contracts']
        matching_qs = Contract.objects.all()
        self.assertQuerysetEqual(view_qs, matching_qs)

    def test_activetab(self):
        response = self.client.get('/contracts/active/')
        activetab_from_view = response.context[0]['activetab']
        self.assertEqual(activetab_from_view, 'contracts')

class Test_View_Partners(TestCase):
    def test_partners_returns_status_200(self):
        response = self.client.get('/partners/')
        self.assertEqual(response.status_code, 200)
    
    def test_activetab(self):
        response = self.client.get('/partners/')
        activetab_from_view = response.context[0]['activetab']
        self.assertEqual(activetab_from_view, 'partners')


""" 
Model tests: 
* Test record creation works
* Test that queries work as they should through the ORM
"""
class Test_Model_Partner(TestCase):
    # Class to test Partners
    def setUp(self):
        # Create a partner
        mypartner = Partner()
        mypartner.name = "TestPartner"
        mypartner.entitytype = "individual"
        mypartner.save()
    
    def test_method_returns_name(self):
        mypartner = Partner.objects.get(id=1)
        self.assertEqual(mypartner.__str__(), "TestPartner")

class Test_Model_Contract(TestCase):
    def setUp(self):
        mypartner = Partner(name="TestPartner", entity_type="individual")
        mypartner.save()
        mycontract = Contract(contract_party=mypartner, contract_type="employment", description="haha", status="active")
        mycontract.save()
    
    def test_method_returns_name(self):
        mycontract = Contract.objects.get(id=1)
        output = "TestPartner" + ': ' + "employment" + ' (' + 'active' + ')'
        self.assertEqual(mycontract.__str__(), output)
    
    

