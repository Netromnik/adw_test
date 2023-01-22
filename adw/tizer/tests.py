from django.test import TestCase
from tizer.models import Wallet, Tizer, Transaction
from django.contrib.auth import get_user_model
from tizer.process import Process
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class TizerProcessingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345', is_superuser=True)
        self.tizers = [
            Tizer.objects.create(
                title="test 1", author=self.user, status=Tizer.Status.WAIT),
            Tizer.objects.create(
                title="test 2", author=self.user, status=Tizer.Status.PAY),
            Tizer.objects.create(
                title="test 3", author=self.user, status=Tizer.Status.FAlL),
        ]

    def test_process_pos_fail(self):
        tizer = Tizer.objects.create(
            title="test 12", author=self.user, status=Tizer.Status.WAIT)
        res = Process(tizer, Tizer.Status.FAlL, self.user).run()
        self.assertAlmostEqual(True, res)
        self.assertAlmostEqual(Tizer.Status.FAlL, tizer.status)

    def test_process_pos_pay(self):
        tizer = Tizer.objects.create(
            title="test 12", author=self.user, status=Tizer.Status.WAIT)
        res = Process(tizer, Tizer.Status.PAY, self.user).run()
        self.assertAlmostEqual(True, res)
        self.assertAlmostEqual(Tizer.Status.PAY, tizer.status)
        w = Wallet.get_user(tizer.author)
        self.assertNotAlmostEqual(0, w.cost)

    def test_process_neg_pay(self):
        tizer = Tizer.objects.create(
            title="test 12", author=self.user, status=Tizer.Status.PAY)
        res = Process(tizer, Tizer.Status.FAlL, self.user).run()
        self.assertAlmostEqual(False, res)
        self.assertAlmostEqual(Tizer.Status.PAY, tizer.status)


class TizerApiTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345', is_superuser=True)
        self.tizers = [
            Tizer.objects.create(
                title="test 1", author=self.user, status=Tizer.Status.WAIT),
            Tizer.objects.create(
                title="test 2", author=self.user, status=Tizer.Status.PAY),
            Tizer.objects.create(
                title="test 3", author=self.user, status=Tizer.Status.FAlL),
        ]

    def test_post_pos(self):
        superuser = User.objects.create_superuser(
            username='superhaki',
            email='me@hakibenita.com',
            password='secret',
        )
        tizer = Tizer.objects.create(
            title="test 12", author=self.user, status=Tizer.Status.WAIT)
        client = APIClient()
        client.login(username='superhaki', password='secret')
        req = client.post(
            '/api/v1/tizers/', {'id': tizer.id, 'status': Tizer.Status.FAlL}, format='json')
        self.assertTrue(status.is_success(req.status_code))
        tizer.refresh_from_db()
        self.assertAlmostEqual(Tizer.Status.FAlL, tizer.status)

    def test_post_pos(self):
        superuser = User.objects.create_superuser(
            username='superhaki',
            email='me@hakibenita.com',
            password='secret',
        )
        tizer = Tizer.objects.create(
            title="test 12", author=self.user, status=Tizer.Status.WAIT)
        client = APIClient()
        client.login(username='superhaki', password='secret')
        req = client.post(
            '/api/v1/tizers/', {'id': tizer.id, 'status': Tizer.Status.PAY}, format='json')
        self.assertTrue(status.is_success(req.status_code))
        tizer.refresh_from_db()
        self.assertAlmostEqual(Tizer.Status.PAY, tizer.status)

    def test_post_neg(self):
        superuser = User.objects.create_superuser(
            username='superhaki',
            email='me@hakibenita.com',
            password='secret',
        )
        tizer = Tizer.objects.create(
            title="test 12", author=self.user, status=Tizer.Status.PAY)
        client = APIClient()
        client.login(username='superhaki', password='secret')
        req = client.post(
            '/api/v1/tizers/', {'id': tizer.id, 'status': Tizer.Status.FAlL}, format='json')
        self.assertFalse(status.is_success(req.status_code))
        tizer.refresh_from_db()
        self.assertAlmostEqual(Tizer.Status.PAY, tizer.status)
