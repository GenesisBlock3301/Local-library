from rest_framework import generics,permissions,status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import renderers
from django.http import Http404


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


# class AuthorCreateView(generics.CreateAPIView):
#     serializer_class = AuthorsSerializer
#     queryset = Author.objects.all()

class AuthorCreateView(APIView,renderers.BrowsableAPIRenderer):
    permission_classes = (permissions.AllowAny,)
    # media_type = 'text/html'
    # renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer, renderers.HTMLFormRenderer)

    def get(self,request,format=None):
        authors = Author.objects.all()
        serializer = AuthorsSerializer(authors,many=True)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",serializer)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>",serializer.data)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = AuthorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        author = self.get_object(pk)
        serializer = AuthorsSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AuthorsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        authors = self.get_object(pk)
        serializer = AuthorsSerializer(authors)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

