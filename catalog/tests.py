
from django.test import TestCase

from catalog.models import Author


"""Author Model Test"""
class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """set up non-modified objects used by all test method"""
        Author.objects.create(first_name='Big',last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        """ we can't get the verbose name directly using author.first_name.verbose_name 
        because author.first_name is a string , so as access first_name object so we usr _meta """

        field_label = author._meta.get_field('first_name').verbose_name
        print(field_label)
        self.assertEquals(field_label,'first_name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_lable = author._meta.get_field('date_of_death').verbose_name
        print(field_lable)
        self.assertEquals(field_lable,'died')

    def first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_lenght
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name},{author.first_name}'
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1/')



""" Form Test """
import datetime
from django.utils import timezone
from catalog.forms import RenewBookForm

class RenewBookForm(TestCase):

    def test_renew_from_date_field_label(self):
        form = RenewBookForm()
        print(form.fields['renewal_date'].label)
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')






