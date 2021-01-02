from django.shortcuts import render,HttpResponse,Http404,get_object_or_404
from .models import *
from django.views import generic,View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from catalog.forms import *
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView


""" permission for function base view """
# @permission_required('catalog.can_mark_returned')
# @permission_required('catalog.can_edit')
# def my_view(request):
#     return HttpResponse("hello world")

""" permission for class base view """


class MyView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'
    #for multiple permission
    permission_required = ('catalog.can_mark_returned','catalog.can_edit')
    #note that 'catalog.can_edit' just an example
    # catalog app doesn't have such permission

@login_required
def index(request):
    """create home page"""
    #count number of book
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    #available book (status 'a')
    num_instance_available = BookInstance.objects.filter(status='a').count()

    #The all() is implied by default.
    num_authors = Author.objects.count()

    #genre numbers
    num_genre = Genre.objects.all().count()

    #exist genre
    available_genre_book = Book.objects.filter(genre__name='Western').count()

    #number of visitors
    num_visitors = request.session.get('num_visitors',0)
    request.session['num_visitors'] = num_visitors + 1
    context = {
        'num_books':num_books,
        'num_instance':num_instance,
        'num_instance_available':num_instance_available,
        'num_authors':num_authors,
        'available_genre_book':available_genre_book,
        'num_visitors': num_visitors
    }
    return render(request,'index.html',context=context)


class BookListView(LoginRequiredMixin,generic.ListView):
    # login_url = '/login/'
    # redirect_field_name = 'login'
    model = Book
    #own name for the book list in template view
    context_object_name = 'book_list'
    template_name = 'book/book.html'
    paginate_by = 5


    """
    query set
    queryset = Book.objects.filter(title__icontains='The')

    also override method inside this view for send data to template
    def get_queryset(self):
        return Book.objects.filter(title__icontains='The')

    for additional context data we can use
    def get_context_data(self, **kwargs):
        #Call the base implentation first to the get the context
        context = super(BookListView,self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context
    """


class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book
    template_name = 'book/book-detail.html'

"""
def book_detail_view(request,id):
    # try:
    #     book = Book.objects.get(pk=id)
    # except Book.DoesNotExist:
    #     raise Http404("Book does not exist.")

    #alternativly we can use
    book = get_object_or_404(Book,pk=id)
    return render(request,'book/book-detail.html',context={'book':book})
"""


class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author
    #own name for the book list in template view
    context_object_name = 'Author_list'
    template_name = 'author/author-list.html'
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author/author-detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """ Gemeric class base view listing book on loan to current usr"""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrow=self.request.user).filter(status__exact='0').order_by('due_back')


class WhoLoanedBookShowlibrianList(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'Who Loaned Book Show librarian.html'
    context_object_name = "all_borrow_books"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='0').order_by('due_back')


def renew_book_librarian(request,id):
    book_instance = get_object_or_404(BookInstance,pk=id)

    if request.method == 'POST':
        """create form instance and populate it with data from the request (binding)"""
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('loan-books'))

    else:
        proposed_renewal_date = datetime.date.today()+datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

    context = {
        'form': form,
        'book_instance':book_instance,
    }
    return render(request, 'book_renew_librarian.html',context=context)


#For author
from catalog.models import Author,Book
from django.urls import reverse_lazy


class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"
    initial = {"date_of_death":'05/01/2019'}
    template_name = 'author/author_form.html'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    template_name = 'author/author_form.html'


class AuthorDelete(DeleteView):
    model = Author
    template_name = 'author/author_confirm_delete.html'
    #as class base view , so we use reverse_lazy , otherwise we use reverse(function base view)
    success_url = reverse_lazy('authors')

#for Book challenge


class BookCreate(CreateView):
    model = Book
    fields = "__all__"
    template_name = 'book/book_form.html'


class BookUpdate(UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']
    template_name = 'book/book_form.html'


class BookDelete(DeleteView):
    model = Book
    template_name = 'book/book_confirm_delete.html'
    #as class base view , so we use reverse_lazy , otherwise we use reverse(function base view)
    success_url = reverse_lazy('books')
