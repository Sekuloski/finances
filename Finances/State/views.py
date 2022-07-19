import datetime
from sre_parse import State
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from.models import CurrentState, Payment, SixMonthPayment, ThreeMonthPayment, Subscription
import calendar
import math


class Index(TemplateView):
    template_name = 'index.html'

    def get(self, request, **kwargs):
        updatePayments()
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

    def get_context_data(self):
        if 'eur' in self.request.GET:
            months = GetMonths(True)    
        else:
            months = GetMonths(False)
              
        context = {
            'state': CurrentState.objects.get(id=1),
            'payments': Payment.objects.all(),
            'months': months
        }
        return context


class AddFunds(TemplateView):
    template_name = 'addFunds.html'
    
    def post(self, request, **kwargs):
        print(request.POST)
        amount = int(request.POST['amount'])
        name = request.POST['name']
        bank = False
        if 'bank' in request.POST:
            bank = True
        payment = Payment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1))
        payment.save()
        Add(amount, bank)

        return redirect('/')

    def get_context_data(self):
        context = {'state': CurrentState.objects.get(id=1).currentAmount}
        return context


class MakePayment(TemplateView):
    template_name = 'payment.html'

    def post(self, request, **kwargs):
        amount = -int(request.POST['payment'])
        name = request.POST['name']
        bank = False
        if 'bank' in request.POST:
            bank = True
        duration = request.POST['duration']
        if duration == '1':
            payment = Payment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1))
            Pay(-amount, bank)
        elif duration == '2':
            payment = SixMonthPayment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1))
            Pay(-amount/6, bank)
        else:
            payment = ThreeMonthPayment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1))
            Pay(-amount/3, bank)

        payment.save()

        return redirect('/')

    def get_context_data(self):
        context = {'state': CurrentState.objects.get(id=1).currentAmount}
        return context


class History(ListView):
    template_name = 'history.html'
    model = Payment
    paginate_by = 100

    def get_context_data(self, **kwargs):
        if 'query' in self.request.GET:
            context = {'payments': Payment.objects.order_by('-date').filter(name__icontains=self.request.GET['query'])}
        else:
            context = {'payments': Payment.objects.order_by('-date')}
        return context


class Subscribe(TemplateView):
    template_name = 'subscription.html'

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

    def post(self, request, **kwargs):
        amount = request.POST['subscribe']
        name = request.POST['name']
        payment = Subscription(amount=amount, name=name)
        payment.save()
        CurrentState.objects.get(id=1).updateSubscriptions()
        return redirect('/')

    def get_context_data(self):
        context = {'state': CurrentState.objects.get(id=1).currentAmount}
        return context


class Change(TemplateView):
    template_name = 'change.html'

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return super(TemplateView, self).render_to_response(context)

    def post(self, request, **kwargs):
        bank = request.POST['bank']
        cash = request.POST['cash']
        state = CurrentState.objects.get(id=1)
        state.amountInBank = bank
        state.amountInCash = cash
        state.save()
        return redirect('/')

    def get_context_data(self):
        context = {'state': CurrentState.objects.get(id=1)}
        return context


def GetMonths(eur):
    counter = 0
    months = {}
    now = int(datetime.datetime.now().month) + 1
    sixMonthPayments = SixMonthPayment.objects.all()
    threeMonthPayments = ThreeMonthPayment.objects.all()
    state = CurrentState.objects.get(id=1)
    lastMonth = state.currentAmount
    salary = state.salary
    subscriptions = state.totalSubscriptions
    for i in range(now, now+12):
        if i > 12:
            months[calendar.month_name[i-12]] = calculateMonthSum(counter, sixMonthPayments, threeMonthPayments, lastMonth, salary, subscriptions, eur)
            lastMonth = months[calendar.month_name[i-12]]
        else:
            months[calendar.month_name[i]] = calculateMonthSum(counter, sixMonthPayments, threeMonthPayments, lastMonth, salary, subscriptions, eur)
            lastMonth = months[calendar.month_name[i]]
            
        counter += 1
    return months


def calculateMonthSum(counter, six, three, state, salary, subscriptions, eur):
    finalSum = state +  salary - subscriptions
    negSum = 0
    for payment in six:
        if payment.monthsLeft - counter > 0:
            negSum += math.ceil(payment.amount / 6 )
    for payment in three:
        if payment.monthsLeft - counter > 0:
            negSum += math.ceil(payment.amount / 3 )
    if eur:
        return math.ceil((finalSum + negSum)*0.016)
    return finalSum + negSum


def updatePayments():
    currentDay = datetime.datetime.now().day
    currentMonth = datetime.datetime.now().month
    for payment in SixMonthPayment.objects.all():
        month = int(str(payment.date).split('-')[1])
        day = payment.dayOfTheMonth
        if currentMonth > month and currentDay < day and payment.updated:
            payment.updated = False
            payment.save()
        if currentMonth > month and currentDay > day and not payment.updated and payment.monthsLeft > 0:
            payment.updated = True
            payment.monthsLeft -= 1
            payment.save()
    for payment in ThreeMonthPayment.objects.all():
        month = int(str(payment.date).split('-')[1])
        day = payment.dayOfTheMonth
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