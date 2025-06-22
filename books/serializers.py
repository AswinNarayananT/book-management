from rest_framework import serializers
from .models import Book, ReadingList, ReadingListItem


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = Book
        fields = '__all__'


class ReadingListItemSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = ReadingListItem
        fields = ['id', 'book', 'book_title', 'position']

class ReadingListSerializer(serializers.ModelSerializer):
    items = ReadingListItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingList
        fields = ['id', 'name', 'created_at', 'owner', 'items']
        read_only_fields = ['owner']
