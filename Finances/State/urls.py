from django.urls import path
from .views import Index, MakePayment, Pay, History

urlpatterns = [
    path('', Index.as_view(), name='Home'),
    path('pay', Index.as_view(), name="Pay"),
    path('history', History.as_view(), name="History"),
    path('payment', MakePayment.as_view(), name="Payment"),
]