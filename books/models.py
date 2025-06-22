from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_date = models.DateField()
    description = models.TextField(blank=True)

    pdf_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class ReadingList(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ReadingListItem(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    position = models.PositiveIntegerField(db_index=True)

    class Meta:
        ordering = ['position']
        unique_together = ['reading_list', 'book']  
