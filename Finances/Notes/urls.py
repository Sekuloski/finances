from django.urls import path
from .views import NotesView, UpdateNote, DeleteNote

urlpatterns = [
    path('', NotesView.as_view(), name="Notes"),
    path('<int:pk>', UpdateNote.as_view(), name="Update Note"),
    path('delete/<int:pk>', DeleteNote.as_view(), name="Delete Note"),
    
]