import unittest
from werkzeug.datastructures import ImmutableMultiDict
from app import app
from datetime import datetime
from website.domain.models import Post,User,db
from website.service.serviceCalendar import ServiceCalendar
from website.utils.detectDepressionModel import DepressionDetector


class TestAll(unittest.TestCase):

    def setUp(self):
         self.client = app.test_client()


    def test_login_with_valid_credentials(self):
        with app.app_context():
            client = app.test_client()
            response = client.post('/login', method='POST', data=ImmutableMultiDict([('email', 'test@example.com'), ('password', 'password')]),follow_redirects=True)
            user = User(email='test@example.com', username='hah',password='password', role='pacient')
            db.session.add(user)
            db.session.commit()
            self.assertEqual(response.status_code, 200)


    def test_login_with_nonexistent_email(self):
        with app.app_context():
            client = app.test_client()
            response = client.post('/login', method='POST', data=ImmutableMultiDict([('email', 'test11@example.com'), ('password', 'password')]),follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Email does not exist.', response.data)

    def test_login_with_get_request(self):
        with app.app_context():
            client = app.test_client()
            response = client.post('/login', method='GET')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)

    def test_get_method(self):
        with app.app_context():
            # Create a test Pacient user
            pacient = User(username='test_pacient', email='test_pacient@example.com', role='pacient',
                           password='password')
            db.session.add(pacient)
            db.session.commit()

            # Create test Posts for the Pacient user
            post1 = Post(text='Test Post 1', date_created=datetime.now(), result='depressed', author=pacient.id)
            post2 = Post(text='Test Post 2', date_created=datetime.now(), result='happy', author=pacient.id)
            db.session.add(post1)
            db.session.add(post2)
            db.session.commit()

            # Call the method with test data
            data = ServiceCalendar.get(month=5, year=2023, pacient=pacient.id)

            # Check the returned data is correct
            assert data is not None
            assert len(data) == 2

            assert data[post1.id]['result'] == 'depressed'
            assert data[post1.id]['color'] == 'gray'
            assert data[post1.id]['date'] == post1.date_created

            assert data[post2.id]['result'] == 'happy'
            assert data[post2.id]['color'] == 'green'
            assert data[post2.id]['date'] == post2.date_created

            # Clean up the test data
            db.session.delete(post1)
            db.session.delete(post2)
            db.session.delete(pacient)
            db.session.commit()

    def test_detect_depression_from_text(self):
        with app.app_context():
            # Define an example text
            text = "Mă simt trist și fără speranță tot timpul. Nu mai simt plăcere în a face lucrurile pe care le iubeam înainte."
            text2 = "O zi incredibil de linistita. doar veselie si ganduri pozitive"

            # Call the method and check the result
            result = DepressionDetector.detectDepressionFromText(text)
            self.assertEqual(result, 'depressed')
            result = DepressionDetector.detectDepressionFromText(text2)
            self.assertEqual(result, 'non-depressed')


