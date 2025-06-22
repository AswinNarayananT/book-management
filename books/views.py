from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookSerializer, ReadingListSerializer, ReadingListItemSerializer
from rest_framework import status
import cloudinary.uploader
from .models import Book, ReadingList, ReadingListItem
from django.db.models import F


# Create your views here.

class BookListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser] 

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        pdf_file = request.FILES.get('pdf_file')
        thumbnail = request.FILES.get('thumbnail_image')

        if pdf_file:
            if not pdf_file.name.endswith('.pdf') or pdf_file.content_type != 'application/pdf':
                raise ValidationError({"pdf_file": "Only .pdf files are allowed."})

        if thumbnail:
            valid_types = ['image/jpeg', 'image/jpg', 'image/png']
            if thumbnail.content_type not in valid_types:
                raise ValidationError({"thumbnail_image": "Only .jpeg and .png images are allowed."})
            
        pdf_url = None
        thumbnail_url = None

        if pdf_file:
            uploaded_pdf = cloudinary.uploader.upload_large(pdf_file, resource_type='raw', folder='books/pdfs')
            pdf_url = uploaded_pdf.get('secure_url')

        if thumbnail:
            uploaded_image = cloudinary.uploader.upload(thumbnail, folder='books/thumbnails')
            thumbnail_url = uploaded_image.get('secure_url')
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user, pdf_url=pdf_url, thumbnail_url=thumbnail_url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class BookDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def patch(self, request, pk):
        book = self.get_object(pk)
        if book.owner != request.user:
            raise PermissionDenied("You do not have permission to update this book.")

        pdf_file = request.FILES.get('pdf_file')
        thumbnail = request.FILES.get('thumbnail_image')

        if pdf_file:
            if not pdf_file.name.endswith('.pdf') or pdf_file.content_type != 'application/pdf':
                raise ValidationError({"pdf_file": "Only .pdf files are allowed."})

        if thumbnail:
            print("it coming bro")
            valid_types = ['image/jpeg', 'image/jpg', 'image/png']
            if thumbnail.content_type not in valid_types:
                raise ValidationError({"thumbnail_image": "Only .jpeg and .png images are allowed."})

        if pdf_file:
            uploaded_pdf = cloudinary.uploader.upload_large(pdf_file, resource_type='raw', folder='books/pdfs')
            request.data['pdf_url'] = uploaded_pdf.get('secure_url')

        if thumbnail:
            uploaded_image = cloudinary.uploader.upload(thumbnail, folder='books/thumbnails')
            request.data['thumbnail_url'] = uploaded_image.get('secure_url')

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        if book.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReadingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lists = ReadingList.objects.filter(owner=request.user)
        serializer = ReadingListSerializer(lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReadingListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReadingListDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        list_ = get_object_or_404(ReadingList, pk=pk)
        if list_.owner != user:
            raise PermissionDenied("Not your reading list.")
        return list_

    def get(self, request, pk):
        list_ = self.get_object(pk, request.user)
        serializer = ReadingListSerializer(list_)
        return Response(serializer.data)

    def delete(self, request, pk):
        list_ = self.get_object(pk, request.user)
        list_.delete()
        return Response(status=204)    
    


class  AddReadingListItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, list_id):
        reading_list = get_object_or_404(ReadingList, pk=list_id, owner=request.user)
        book_id = request.data.get("book")

        if not book_id:
            return Response({"error": "Book ID is required."}, status=400)
        
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": f"Book with id {book_id} does not exist."}, status=404)

        if ReadingListItem.objects.filter(reading_list=reading_list, book_id=book_id).exists():
            return Response({"error": "Book already in reading list."}, status=400)

        last_position = ReadingListItem.objects.filter(reading_list=reading_list).count()
        item = ReadingListItem.objects.create(
            reading_list=reading_list,
            book_id=book_id,
            position=last_position + 1
        )
        serializer = ReadingListItemSerializer(item)
        return Response(serializer.data, status=201)


class RemoveReadingListItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, list_id, item_id):
        reading_list = get_object_or_404(ReadingList, pk=list_id, owner=request.user)
        item = get_object_or_404(ReadingListItem, pk=item_id, reading_list=reading_list)
        deleted_position = item.position
        item.delete()

        ReadingListItem.objects.filter(
            reading_list=reading_list,
            position__gt=deleted_position
        ).update(position=F('position') - 1)

        return Response(status=204)


class ReorderReadingListItem(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, list_id, item_id):
        reading_list = get_object_or_404(ReadingList, pk=list_id, owner=request.user)
        item = get_object_or_404(ReadingListItem, pk=item_id, reading_list=reading_list)
        new_position = request.data.get("position")

        if new_position is None:
            return Response({"error": "New position is required."}, status=400)

        try:
            new_position = int(new_position)
        except:
            return Response({"error": "Invalid position format."}, status=400)

        total_items = ReadingListItem.objects.filter(reading_list=reading_list).count()
        if new_position < 1 or new_position > total_items:
            return Response({"error": "Position out of range."}, status=400)

        current_position = item.position
        if new_position == current_position:
            return Response({"message": "No change needed."})

        if new_position < current_position:
            ReadingListItem.objects.filter(
                reading_list=reading_list,
                position__gte=new_position,
                position__lt=current_position
            ).update(position=F('position') + 1)
        else:
            ReadingListItem.objects.filter(
                reading_list=reading_list,
                position__gt=current_position,
                position__lte=new_position
            ).update(position=F('position') - 1)

        item.position = new_position
        item.save()
        return Response({"message": "Position updated."})
