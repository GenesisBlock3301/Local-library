from django.urls import path
from .api_views import *

urlpatterns = [
    path('books/', BooksViews.as_view()),
    path('book/<id>/', BookDetailViews.as_view()),
    path('authors/', AuthorListView.as_view()),
    path('author/<id>/', AuthorDetailViews.as_view()),
    path('mybooks/', UserBooksLoan.as_view()),
    path('loanbooks/', WhoLoanBookView.as_view()),
    path('book/<uuid:pk>/renew/', BookRenewView.as_view()),
    path('author-create/',AuthorCreateView.as_view()),
    path('author/<int:pk>/update/',AuthorUpdateView.as_view()),
    path('author/<int:pk>/delete/',AuthorDeleteView.as_view()),
]
