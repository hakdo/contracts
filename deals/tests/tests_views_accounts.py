from django.test import TestCase
import uuid

class TestViewRegister(TestCase):
    def test_register_fails_on_wrong_uuid(self):
            random_uuid = uuid.uuid4()
            mydata = {
                'username': 'johnnytheheadbanger',
                'password': 'I am a blind cat from th3 FutUrE!',
                'confirm_password': 'I am a blind cat from th3 FutUrE!',
                'secret_code': str(random_uuid)
                }
            response = self.client.post('/team/register', data=mydata)
            print(response.status_code)
            self.assertEqual(response.status_code, 200)
