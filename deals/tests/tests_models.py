from django.test import TestCase
from deals.models import Partner
from deals.models import Contract

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
    
    

