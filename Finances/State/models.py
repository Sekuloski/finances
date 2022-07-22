import datetime
from django.db import models
import math


class CurrentState(models.Model):
    _singleton = models.BooleanField(default=True, editable=False, unique=True)
    amountInBank = models.IntegerField(default=0)
    amountInCash = models.IntegerField(default=0)
    currentAmount = models.IntegerField(default=0, editable=False)
    salary = models.IntegerField(default=29500)
    totalSubscriptions = models.IntegerField(default=0)
    lastSalary = models.DateField()

    def makePayment(self, amount, bank):
        if(bank):
            self.amountInBank -= amount
            self.updateAmount()
        else:
            self.amountInCash -= amount
            self.updateAmount()

    def addFunds(self, amount, bank):
        if(bank):
            self.amountInBank += amount
            self.updateAmount()
        else:
            self.amountInCash += amount
            self.updateAmount()

    def updateAmount(self):
        self.currentAmount = self.amountInBank + self.amountInCash
        self.save()

    def updateSubscriptions(self):
        self.totalSubscriptions = 0
        for payment in Subscription.objects.all():
            if payment.active:
                self.totalSubscriptions += payment.amount
        self.save()

    def totalMonthlyPayments(self):
        total = 0
        for payment in SixMonthPayment.objects.all():
            if payment.monthsLeft in range(1,6):
                total += math.ceil(payment.amount/6)
        
        for payment in ThreeMonthPayment.objects.all():
            if payment.monthsLeft in range(1,3):
                total += math.ceil(payment.amount/3)

        return -total

    def salaryNotReceived(self):
        return self.lastSalary.month != datetime.datetime.now().month

    def addSalary(self):
        self.amountInBank += self.salary
        self.lastSalary = datetime.datetime.now()
        self.save()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentAmount = self.amountInBank + self.amountInCash
        self.updateSubscriptions()
        self.save()

    def __str__(self):
        return 'Current State'


class Subscription(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=255)
    bank = models.BooleanField()
    date = models.DateTimeField()
    state = models.ForeignKey(CurrentState, on_delete=models.CASCADE)
    dayOfTheMonth = models.IntegerField(editable=False, default=1)
    updated = models.BooleanField(default=True)
    fullPayment = models.BooleanField(default=True)
    testPayment = models.BooleanField(default=False)
    sixMonths = models.BooleanField(default=False)
    threeMonths = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        day = int(str(self.date).split('-')[2].split(' ')[0])
        if day > 28:
            self.dayOfTheMonth = 28
        else:
            self.dayOfTheMonth = day
        self.save()


    def __str__(self):
        return self.name + ' ' + str(self.amount) + ' ' + ('Bank ' if self.bank else 'Cash ') + str(self.date.strftime("%d-%m-%y %H:%M")) + ' ' + ('Full' if self.fullPayment else 'Monthly')


class SixMonthPayment(Payment):
    monthsLeft = models.IntegerField(default=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ThreeMonthPayment(Payment):
    monthsLeft = models.IntegerField(default=3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)