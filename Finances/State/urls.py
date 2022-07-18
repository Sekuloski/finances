from django.urls import path
from .views import Index, MakePayment, History, Subscribe, Change, AddFunds

urlpatterns = [
    path('', Index.as_view(), name='Home'),
    path('history', History.as_view(), name="History"),
    path('add', AddFunds.as_view(), name="Add Funds"),
    path('pay', MakePayment.as_view(), name="Payment"),
    path('subscribe', Subscribe.as_view(), name="Subscription"),
    path('change', Change.as_view(), name="Change"),
    
]