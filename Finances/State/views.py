import datetime
from sre_parse import State
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from.models import CurrentState, Payment, SixMonthPayment, ThreeMonthPayment
import calendar
import math


class Index(TemplateView):
    template_name = 'index.html'

    def get(self, request, **kwargs):
        updatePayments()
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
    
    def get_context_data(self):
        context = {'state': CurrentState.objects.get(id=1).currentAmount}
        return context


class History(ListView):
    template_name = 'history.html'
    model = Payment
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = {'payments': Payment.objects.order_by('-date')}
        return context


def GetMonths():
    counter = 0
    months = {}
    now = int(datetime.datetime.now().month)
    sixMonthPayments = SixMonthPayment.objects.all()
    threeMonthPayments = ThreeMonthPayment.objects.all()
    state = CurrentState.objects.get(id=1)
    for i in range(now, now+12):
        if i > 12:
            months[calendar.month_name[i-12]] = calculateMonthSum(counter, sixMonthPayments, threeMonthPayments, state)
        else:
            months[calendar.month_name[i]] = calculateMonthSum(counter, sixMonthPayments, threeMonthPayments, state)
        counter += 1
    return months


def calculateMonthSum(counter, six, three, state):
    finalSum = state.currentAmount + counter * state.salary
    negSum = 0
    for payment in six:
        if payment.monthsLeft - counter > 0:
            negSum += math.ceil(payment.amount / 6 )
    for payment in three:
        if payment.monthsLeft - counter > 0:
            negSum += math.ceil(payment.amount / 3 )
    return finalSum - negSum


def updatePayments():
    currentDay = datetime.datetime.now().day
    currentMonth = datetime.datetime.now().month
    for payment in SixMonthPayment.objects.all():
        month = int(str(payment.date).split('-')[1])
        day = payment.dayOfTheMonth
        print(payment.monthsLeft)
        if currentMonth > month and currentDay < day and payment.updated:
            payment.updated = False
            payment.save()
        if currentMonth > month and currentDay > day and not payment.updated and payment.monthsLeft > 0:
            payment.updated = True
            payment.monthsLeft -= 1
            payment.save()


def Pay(amount, bank):
    state = CurrentState.objects.get(id=1)
    state.makePayment(amount, bank)
    return redirect('/')


def Add(amount, bank):
    state = CurrentState.objects.get(id=1)
    state.addFunds(amount, bank)
    return redirect('/')