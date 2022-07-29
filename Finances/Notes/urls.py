from django.urls import path
from .templates.Notes.templates.views import NotesView, UpdateNote, DeleteNote, AddNote

urlpatterns = [
    path('', NotesView.as_view(), name="Notes"),
    path('<int:pk>', UpdateNote.as_view(), name="Update Note"),
    path('delete/<int:pk>', DeleteNote.as_view(), name="Delete Note"),
    path('addnote', AddNote.as_view(), name="Add Note"),

]
