from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Note

# Create your views here.
class NotesView(ListView):
    model = Note
    template_name = 'notes.html'

    def post(self, request, **kwargs):
        text = request.POST['text']
        note = Note(text=text)
        note.save()

        return redirect('/notes')