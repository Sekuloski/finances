import datetime
from sre_parse import State
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from.models import CurrentState, Payment, SixMonthPayment, ThreeMonthPayment
import calendar

class Index(TemplateView):
    template_name = 'index.html'

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

    def post(self, request, **kwargs):
        amount = int(request.POST['payment'])
        name = request.POST['name']
        bank = True if request.POST['bank'] == 'on' else False
        duration = request.POST['duration']
        if duration == '1':
            payment = Payment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1))
        elif duration == '2':
            payment = SixMonthPayment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1))
        else:
            payment = ThreeMonthPayment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1))
        payment.save()
        if amount > 0:
            Add(amount, True)
        else:
            Pay(-amount, True)

        context = self.get_context_data()
        context['test'] = (amount, name, bank)
        return super(TemplateView, self).render_to_response(context)

    def get_context_data(self):
        months = GetMonths()
        context = {
            'state': CurrentState.objects.get(id=1).currentAmount,
            'payments': Payment.objects.all(),
            'months': months
        }
        return context


class MakePayment(TemplateView):
    template_name = 'payment.html'


class History(ListView):
    template_name = 'history.html'
    model = Payment
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = {'payments': Payment.objects.order_by('-date')}
        return context


def GetMonths():
    months = {}
    now = int(datetime.datetime.now().month)
    for i in range(now, now+12):
        if i > 12:
            months[calendar.month_name[i-12]] = '2'
        else:
            months[calendar.month_name[i]] = '2'
    return months


def Pay(amount, bank):
    state = CurrentState.objects.get(id=1)
    state.makePayment(amount, bank)
    return redirect('/')


def Add(amount, bank):
    state = CurrentState.objects.get(id=1)
    state.addFunds(amount, bank)
    return redirect('/')