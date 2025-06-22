from django.urls import path
from .views import BookListCreateView, BookDetailView, ReadingListView, ReadingListDetailView, AddReadingListItem, RemoveReadingListItem, ReorderReadingListItem

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list-create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('reading-lists/', ReadingListView.as_view()),
    path('reading-lists/<int:pk>/', ReadingListDetailView.as_view()),
    path('reading-lists/<int:list_id>/add/', AddReadingListItem.as_view()),
    path('reading-lists/<int:list_id>/remove/<int:item_id>/', RemoveReadingListItem.as_view()),
    path('reading-lists/<int:list_id>/reorder/<int:item_id>/', ReorderReadingListItem.as_view()),
]
