from rest_framework import serializers
from .models import *


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializers(serializers.ModelSerializer):
    # author = serializers.RelatedField(source='author', read_only=True)
    class Meta:
        model = Book
        fields = "__all__"


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def create(self, validated_data):
        return Author.objects.create(**validated_data)


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = "__all__"

