from django.test import TestCase
from .. models import Organization
import uuid

class TestRegisterForm(TestCase):
    def setUp(self):
        myorg = Organization(name='Donkey', active=True, accepting_members=True, orgsecret=str(uuid.uuid4()))
        myorg.save()
        myorg2 = Organization(name='Donkey2', active=True, accepting_members=False, orgsecret=str(uuid.uuid4()))
        myorg2.save()

    def test_form_register_blocks_invalid_secret_code(self):
        random_uuid = uuid.uuid4()
        mydata = {
            'username': 'johnnytheheadbanger',
            'password': 'I am a blind cat from th3 FutUrE!',
            'confirm_password': 'I am a blind cat from th3 FutUrE!',
            'secret_code': random_uuid
        }
        response = self.client.post('/team/register', data=mydata)
        self.assertFormError(response, 'form', 'secret_code',['This invite code is invalid.'])
    
    def test_form_register_blocks_registration_when_not_accepting_members(self):
        myorg = Organization.objects.filter(name='Donkey2')[0]
        mydata = {
            'username': 'johnnytheheadbanger',
            'password': 'I am a blind cat from th3 FutUrE!',
            'confirm_password': 'I am a blind cat from th3 FutUrE!',
            'secret_code': myorg.orgsecret
        }
        response = self.client.post('/team/register', data=mydata)
        self.assertFormError(response, 'form', 'secret_code',['This invite code is invalid or has expired.'])
