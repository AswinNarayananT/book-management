from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
import cloudinary.uploader

from .models import Book
from .serializers import BookSerializer
# Create your views here.
from rest_framework.parsers import MultiPartParser, FormParser

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

        # Validate PDF
        if pdf_file:
            if not pdf_file.name.endswith('.pdf') or pdf_file.content_type != 'application/pdf':
                raise ValidationError({"pdf_file": "Only .pdf files are allowed."})

        # Validate Image
        if thumbnail:
            valid_types = ['image/jpeg', 'image/jpg', 'image/png']
            if thumbnail.content_type not in valid_types:
                raise ValidationError({"thumbnail_image": "Only .jpeg and .png images are allowed."})

        # Upload to Cloudinary
        pdf_url = None
        thumbnail_url = None

        if pdf_file:
            uploaded_pdf = cloudinary.uploader.upload_large(pdf_file, resource_type='raw', folder='books/pdfs')
            pdf_url = uploaded_pdf.get('secure_url')

        if thumbnail:
            uploaded_image = cloudinary.uploader.upload(thumbnail, folder='books/thumbnails')
            thumbnail_url = uploaded_image.get('secure_url')

        # ✅ Just pass request.data — DRF handles files automatically
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

    def put(self, request, pk):
        book = self.get_object(pk)
        if book.owner != request.user:
            raise PermissionDenied("You do not have permission to update this book.")

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        book = self.get_object(pk)
        if book.owner != request.user:
            raise PermissionDenied("You do not have permission to update this book.")

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