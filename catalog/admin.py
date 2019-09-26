from django.contrib import admin

from catalog.models import *




class BooksInLine(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','date_of_birth','date_of_death']
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    inlines = [BooksInLine]

admin.site.register(Genre)


class BooksInstanceInLine(admin.TabularInline):
    model = BookInstance

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book','status','borrow','due_back','id']
    list_filter = ['status','due_back']
    fieldsets = (
        (None, {
            'fields': ('book','imprint','id')
        }),
        ('Availability',{
           'fields':('status','due_back','borrow')
        }),
    )


class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','isbn','display_genre','language','id']
    inlines = [BooksInstanceInLine]
admin.site.register(Book,BookAdmin)

admin.site.register(Language)

