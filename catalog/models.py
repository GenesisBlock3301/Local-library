from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200, help_text="Entre the book's natural Language")
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)

    #foreign key use because one book have one author , but author can have multiple book . That means one to many relationship
    #Author as a string rather than object because it has not declared yet in the file
    #foreign key means one to many field
    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    summary = models.TextField(max_length=1000,help_text='Enter a brief descriptions the book')
    isbn = models.CharField('ISBN',max_length=13,help_text='13 Character ISBN nmuber must Enter')
    #Many to many Field used because genre can contain many books, Books can cover many genre
    #Genre class already has been define so we can specify the object above
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book.')
    #one to many relationship
    language = models.ForeignKey('Language',on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:2])
    # display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4, help_text='Unique id for particular book')
    book = models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)
    borrow = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS ={
        ('m','Maintainance'),
        ('0','On loan'),
        ('a','Available'),
        ('r','Reserved'),
    }

    status = models.CharField(max_length=1, choices=LOAN_STATUS,blank=True, default='m',help_text='Book availability')

    class Meta:
        ordering = ['-due_back']

        """ define the permission """
        permissions = (
            ("can_mark_returned","Set book as returned"),
        )

    def __str__(self):
        return f'{self.id} ({ self.book.title })'


class Author (models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} , {self.first_name }'


# from django.contrib.auth.models import User
# user = User.objects.create_user('myusername','myusername@gmail.com','mypassword')
# user.first_name = "Sifat"
# user.last_name = "Nas"
# user.save()