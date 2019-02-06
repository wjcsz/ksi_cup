from django.test import TestCase
from .models import CupOwner
from mail import MailSender
# Create your tests here.

class CupOwnerTest(TestCase):
    def setUp(self):
        Kowalski = CupOwner.objects.create(name='Jan', surname='Kowalski', mail='1234521@test.kowalski')
        Kowalski.cup_set.create(is_dirty=True)

    def test(self):
        test_object = CupOwner.objects.get(name='Jan')
        self.assertIsNotNone(test_object)
        self.assertTrue(test_object.cup_set.get().is_dirty)

class CupTest(TestCase):
    def setUp(self):
        Kowalski = CupOwner.objects.create(name='Jan', surname='Kowalski', mail='1234521@test.kowalski')
        Kowalski.cup_set.create(is_dirty=False)

    def test(self):
        test_object = CupOwner.objects.get(name='Jan')
        test_object_cup = test_object.cup_set.get()
        test_object_cup.mark_as_dirty()
        test_object_cup.increase_rebuke_count()
        test_object_cup.increase_rebuke_count()

        self.assertTrue(test_object_cup.is_dirty)
        self.assertEqual(test_object_cup.rebukes_count, 2)

class FunctionalityTest(TestCase):
    def setUp(self):
        Kowalski = CupOwner.objects.create(name='Jan', surname='Kowalski', mail='1234521@test.kowalski')
        Kowalski.cup_set.create(is_dirty=True)

    def test(self):
        cup_owner = CupOwner.objects.get(name='Jan')
        cup = cup_owner.cup_set.get()

        sender = MailSender(cup_owner)
        sender.send_rebuke()

        self.assertTrue(cup.is_dirty)
        self.assertEqual(cup.rebukes_count, 1)

        cup.clean()

        self.assertFalse(cup.is_dirty)