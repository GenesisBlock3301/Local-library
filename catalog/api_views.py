from rest_framework import generics,permissions
from .serializers import *
from .models import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class BooksViews(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class BookDetailViews(generics.ListAPIView):
    serializer_class = BookSerializers

    def get_queryset(self):
        id = self.kwargs['id']
        return Book.objects.filter(id=id)


class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorsSerializer
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailViews(generics.ListAPIView):
    serializer_class = AuthorsSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return Author.objects.filter(id=id)


class UserBooksLoan(generics.ListAPIView):
    serializer_class = BookInstanceSerializer

    def get_queryset(self):
        return BookInstance.objects.all()


class WhoLoanBookView(generics.ListAPIView):
    serializer_class = BookInstanceSerializer

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='0').order_by('due_back')


class BookRenewView(generics.RetrieveUpdateAPIView):
    serializer_class = BookInstanceSerializer
    queryset = BookInstance.objects.all()


class AuthorCreateView(generics.CreateAPIView):
    serializer_class = AuthorsSerializer
    queryset = Author.objects.all()


