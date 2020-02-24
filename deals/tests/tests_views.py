from django.test import TestCase
from deals.models import Partner
from deals.models import Contract

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
