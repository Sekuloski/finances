from django.db import models


class CurrentState(models.Model):
    _singleton = models.BooleanField(default=True, editable=False, unique=True)
    amountInBank = models.IntegerField(default=0)
    amountInCash = models.IntegerField(default=0)
    currentAmount = models.IntegerField(default=0, editable=False)
    salary = models.IntegerField(default=29500, name='Current Salary')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentAmount = self.amountInBank + self.amountInCash

    def __str__(self):
        return 'Current State'