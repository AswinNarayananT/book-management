from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['pdf_url', 'thumbnail_url']