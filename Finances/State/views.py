from sre_parse import State
from django.shortcuts import render
from django.views.generic import TemplateView
from.models import CurrentState

# Create your views here.
class Index(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        state = CurrentState.objects.get(id=1)
        context = {
            'state': state
        }
        return context