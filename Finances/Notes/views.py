from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from .models import Note

# Create your views here.
class NotesView(ListView):
    model = Note
    template_name = 'notes.html'

    def post(self, request, **kwargs):
        text = request.POST['textArea']
        note = Note(text=text)
        note.save()

        return redirect('/notes')


class UpdateNote(UpdateView):
    template_name = 'form.html'
    model = Note
    fields = ['text', 'date']
    success_url = reverse_lazy('Notes')


class DeleteNote(DeleteView):
    model = Note
    template_name = "note_confirm_delete.html"

    success_url = reverse_lazy('Notes')
