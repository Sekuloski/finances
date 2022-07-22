from django.urls import path
from .views import Index, Payments, MakePayment, History, Subscribe, Change, AddFunds, MakeTestPayment, UpdatePayment, delete_view, addSalary

urlpatterns = [
    path('', Index.as_view(), name='Home'),
    path('history', History.as_view(), name="History"),
    path('add', AddFunds.as_view(), name="Add Funds"),
    path('pay', MakePayment.as_view(), name="Payment"),
    path('subscribe', Subscribe.as_view(), name="Subscription"),
    path('change', Change.as_view(), name="Change"),
    path('test-payment', MakeTestPayment.as_view(), name="Test Payment"),
    path('payments', Payments.as_view(), name="Payments"),
    path('payments/<int:pk>', UpdatePayment.as_view(), name="Update Payment"),
    path('payments/delete/<int:id>', delete_view, name="Delete Payment"),
    path('addSalary', addSalary, name="Add Salary"),

]