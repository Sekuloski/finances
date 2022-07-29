import datetime
from sre_parse import State
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
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
            months = GetMonths(eur=True)    
        else:
            months = GetMonths(eur=False)
              
        context = {
            'state': CurrentState.objects.get(id=1),
            'payments': Payment.objects.all(),
            'months': months
        }
        return context


class Payments(ListView):
    template_name = 'payments.html'
    model = Payment
    ordering = ['-date']



class UpdatePayment(UpdateView):
    template_name = 'form.html'
    model = Payment
    fields = ['name', 'amount', 'date']
    success_url = reverse_lazy('Payments')


class Subscriptions(ListView):
    template_name = 'subscriptions.html'
    model = Subscription


class UpdateSubscription(UpdateView):
    template_name = 'form.html'
    model = Subscription
    fields = ['name', 'amount', 'active']
    success_url = reverse_lazy('Subscriptions')


class DeleteSubscription(DeleteView):
    model = Subscription
    template_name = "subscription_confirm_delete.html"

    success_url = reverse_lazy('Subscriptions')


def delete_view(request, id):
    context ={}
    payment = get_object_or_404(Payment, id = id)
    state = CurrentState.objects.get(id=1)
    if request.method =="POST":
        if payment.fullPayment and payment.date.month == datetime.datetime.now().month:
            state.addFunds(-payment.amount, payment.bank)
        elif payment.sixMonths and payment.date.month == datetime.datetime.now().month:
            state.addFunds(-payment.amount/6, payment.bank)
        elif payment.threeMonths and payment.date.month == datetime.datetime.now().month:
            state.addFunds(-payment.amount/3, payment.bank)
        payment.delete()
        return redirect("/payments")
 
    return render(request, "payment_confirm_delete.html", context)


def addSalary(request):
    CurrentState.objects.get(id=1).addSalary()
    return redirect('/')


class AddFunds(TemplateView):
    template_name = 'addFunds.html'
    
    def post(self, request, **kwargs):
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
            payment = SixMonthPayment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1), fullPayment=False, sixMonths=True)
            Pay(-amount/6, bank)
            payment.monthsLeft -= 1
        else:
            payment = ThreeMonthPayment(amount=amount, name=name, bank=bank, date=datetime.datetime.now(), state=CurrentState.objects.get(id=1), fullPayment=False, threeMonths=True)
            Pay(-amount/3, bank)
            payment.monthsLeft -= 1

        payment.save()

        return redirect('/')

    def get_context_data(self):
        context = {'state': CurrentState.objects.get(id=1).currentAmount}
        return context

class MakeTestPayment(TemplateView):
    template_name = 'test-payment.html'

    def post(self, request, **kwargs):
        if request.POST['date'] != '':
            date = request.POST['date']
        else:
            date = datetime.datetime.now()
        amount = -int(request.POST['payment'])
        name = request.POST['name']
        bank = False
        if 'bank' in request.POST:
            bank = True
        duration = request.POST['duration']

        if duration == '1':
            payment = Payment(amount=amount, name=name, bank=bank, date=date, state=CurrentState.objects.get(id=1), testPayment=True)
            if request.POST['date'] == '':
                Pay(-amount, bank)
        elif duration == '2':
            payment = SixMonthPayment(amount=amount, name=name, bank=bank, date=date, state=CurrentState.objects.get(id=1), fullPayment=False, testPayment=True, sixMonths=True)
            if request.POST['date'] == '':
                Pay(-amount/6, bank)
                payment.monthsLeft -= 1
        else:
            payment = ThreeMonthPayment(amount=amount, name=name, bank=bank, date=date, state=CurrentState.objects.get(id=1), fullPayment=False, testPayment=True, threeMonths=True)
            if request.POST['date'] == '':
                Pay(-amount/3, bank)
                payment.monthsLeft -= 1

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
    months = {}
    now = int(datetime.datetime.now().month) + 1
    sixMonthPayments = SixMonthPayment.objects.all()
    threeMonthPayments = ThreeMonthPayment.objects.all()
    fullPayments = Payment.objects.all()
    for payment in sixMonthPayments:
        fullPayments = fullPayments.exclude(name=payment.name)
    for payment in threeMonthPayments:
        fullPayments = fullPayments.exclude(name=payment.name)
    state = CurrentState.objects.get(id=1)
    lastMonth = state.currentAmount
    salary = state.salary
    subscriptions = state.totalSubscriptions
    for i in range(now, now+12):
        if i > 12:
            months[calendar.month_name[i-12]] = calculateMonthSum(i, fullPayments, sixMonthPayments, threeMonthPayments, lastMonth, salary, subscriptions, eur)
            lastMonth = months[calendar.month_name[i-12]]
        else:
            months[calendar.month_name[i]] = calculateMonthSum(i, fullPayments, sixMonthPayments, threeMonthPayments, lastMonth, salary, subscriptions, eur)
            lastMonth = months[calendar.month_name[i]]
            
    return months


def calculateMonthSum(month, full, six, three, state, salary, subscriptions, eur):
    now = datetime.datetime.now()
    if eur and month > now.month + 1:
        finalSum = state/0.016 + salary - subscriptions
    else:
        finalSum = state + salary - subscriptions
    negSum = 0
    for payment in full:
        if month > 12:
            if payment.date.year > now.year: # 'NEXT YEAR ON PURCHASE, NEXT YEAR ON COUNTER'
                if payment.date.month == (month - 12):
                    negSum += math.ceil(payment.amount)
        else:
            if payment.date.year == now.year: # 'CURRENT YEAR ON PURCHASE, CURRENT ON COUNTER'
                if payment.date.month == (month):
                    negSum += math.ceil(payment.amount)

    for payment in six:
        if month <= 12:
            if payment.date.year > now.year: # 01-23 -> 12
                continue
            if month - payment.date.month in range(6): # 09-22 -> 12
                negSum += math.ceil(payment.amount / 6) 
        else:
            if payment.date.year == now.year: # 09-22 -> 13-12 = 1   12 - 9 = 3
                if (12 - payment.date.month) + (month - 12) in range(6):
                    negSum += math.ceil(payment.amount / 6)
            elif payment.date.year > now.year: # 01-23 -> 13
                if (month - 12) - payment.date.month in range(6):
                    negSum += math.ceil(payment.amount / 6)

    for payment in three:
        if month <= 12:
            if payment.date.year > now.year: 
                continue
            if month - payment.date.month in range(3): 
                negSum += math.ceil(payment.amount / 3) 
        else:
            if payment.date.year == now.year: 
                if (12 - payment.date.month) + (month - 12) in range(3):
                    negSum += math.ceil(payment.amount / 3)
            elif payment.date.year > now.year: 
                if (month - 12) - payment.date.month in range(3):
                    negSum += math.ceil(payment.amount / 3)
    finalSum += negSum
    if eur:
        return math.ceil(finalSum*0.016)
    return finalSum


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